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