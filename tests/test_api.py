import pytest
import requests
import art_generator.api as api


def test_first_call_does_not_sleep(clock, limited):
    limited()
    assert clock.sleeps == []


def test_immediate_second_call_sleeps_one_interval(clock, limited):
    limited()
    limited()
    assert clock.sleeps == [pytest.approx(api.MIN_INTERVAL)]


def test_call_after_interval_does_not_sleep(clock, limited):
    limited()
    clock.now += api.MIN_INTERVAL * 2
    limited()
    assert clock.sleeps == []


def test_partial_wait_sleeps_only_the_remainder(clock, limited):
    limited()
    clock.now += api.MIN_INTERVAL / 2
    limited()
    assert clock.sleeps == [pytest.approx(api.MIN_INTERVAL / 2)]


def test_wrapper_passes_arguments_and_return_value(clock, limited):
    assert limited(42) == 42

def test_get_object_ids_returns_ids(monkeypatch, mock_ids_payload, make_response):
    def mock_get(*args, **kwargs):
        return make_response(mock_ids_payload, 200)

    monkeypatch.setattr(requests, "get", mock_get)

    assert api.get_object_ids() == mock_ids_payload["objectIDs"]

def test_get_object_ids_raises_on_http_error(monkeypatch, make_response):
    def mock_get(*args, **kwargs):
        return make_response(None, 500)

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.get_object_ids()

def test_get_object_returns_object(monkeypatch, make_response, sample_object, object_id: int):

    def mock_get(*args, **kwargs):
        return make_response(sample_object, 200)

    monkeypatch.setattr(requests, "get", mock_get)

    obj = api.get_object(object_id)
    assert obj["objectID"] == 1
    assert obj["isPublicDomain"] == False
    assert obj["primaryImage"] == ""
    assert obj["title"] == "One-dollar Liberty Head Coin"
    assert obj["artistDisplayName"] == "James Barton Longacre"
    assert obj["objectDate"] == "1853"

def test_get_object_raises_artwork_not_found_error(monkeypatch, make_response, object_id):

    def mock_get(*args, **kwargs):
        return make_response(None, 404)
    
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(api.ArtworkNotFound):
        api.get_object(object_id) 


def test_get_object_raises_on_http_error(monkeypatch, make_response, object_id: int):
    
    def mock_get(*args, **kwargs):
        return make_response(None, 500)

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.get_object(object_id)

def test_search_returns_ids(monkeypatch, make_response, mock_ids_payload, search_query: str):

    def mock_get(*args, **kwargs):
            return make_response(mock_ids_payload, 200)

    monkeypatch.setattr(requests, "get", mock_get)
    assert api.search(search_query) == mock_ids_payload["objectIDs"]

def test_search_raises_on_http_error(monkeypatch, make_response, search_query: str):
    
    def mock_get(*args, **kwargs):
        return make_response(None, 500)

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.search(search_query)
