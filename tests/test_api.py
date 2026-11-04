import json
from pathlib import Path
import requests
import pytest
import art_generator.api as api

DATA_DIR = Path(__file__).parent / "data"
OBJECT_ID = 1

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

def test_get_object_returns_object(monkeypatch):
    with open(DATA_DIR / f"object_{OBJECT_ID}.json") as file:
        mock_object = json.load(file)


    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return mock_object

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    obj = api.get_object(OBJECT_ID)
    assert obj["objectID"] == 1
    assert obj["isPublicDomain"] == False
    assert obj["primaryImage"] == ""
    assert obj["title"] == "One-dollar Liberty Head Coin"
    assert obj["artistDisplayName"] == "James Barton Longacre"
    assert obj["objectDate"] == "1853"

def test_get_object_raises_on_http_error(monkeypatch):
    class ErrorResponse:
            def raise_for_status(self):
                raise requests.HTTPError("HTTP Error")
    
    def mock_get(*args, **kwargs):
        return ErrorResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(requests.HTTPError):
        api.get_object(OBJECT_ID)
