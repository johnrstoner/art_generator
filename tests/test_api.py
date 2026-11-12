import requests
import pytest
import art_generator.api as api


def test_get_object_ids_returns_ids(monkeypatch):
    mock_ids = [1, 2, 3]

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"total": 3, "objectIDs": mock_ids}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    assert api.get_object_ids() == mock_ids

def test_get_object_ids_raises_on_http_error(monkeypatch):
    class ErrorResponse:
        def raise_for_status(self):
            raise requests.HTTPError("HTTP Error")

    def mock_get(*args, **kwargs):
        return ErrorResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.get_object_ids()

def test_get_object_returns_object(monkeypatch, sample_object: dict, object_id: int):

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return sample_object

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    obj = api.get_object(object_id)
    assert obj["objectID"] == 1
    assert obj["isPublicDomain"] == False
    assert obj["primaryImage"] == ""
    assert obj["title"] == "One-dollar Liberty Head Coin"
    assert obj["artistDisplayName"] == "James Barton Longacre"
    assert obj["objectDate"] == "1853"

def test_get_object_raises_on_http_error(monkeypatch, object_id: int):
    class ErrorResponse:
            def raise_for_status(self):
                raise requests.HTTPError("HTTP Error")
    
    def mock_get(*args, **kwargs):
        return ErrorResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.get_object(object_id)

def test_search_returns_ids(monkeypatch, search_query: str):
    mock_ids = [1, 2, 3]
    
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"total": 3, "objectIDs": mock_ids}

    def mock_get(*args, **kwargs):
            return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert api.search(search_query) == [1, 2, 3]

def test_search_raises_on_http_error(monkeypatch, search_query: str):
    class ErrorResponse:
            def raise_for_status(self):
                raise requests.HTTPError("HTTP Error")
    
    def mock_get(*args, **kwargs):
        return ErrorResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.search(search_query)
