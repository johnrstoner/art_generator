import json
from pathlib import Path

import pytest
import requests

DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def error_response():
    class ErrorResponse:
        def raise_for_status(self):
            raise requests.HTTPError("HTTP Error")
    return ErrorResponse

@pytest.fixture
def mock_response_list_ids():

    class MockResponse:
        mock_ids = [1, 2, 3]

        def raise_for_status(self):
            pass

        def json(self):
            return {"total": len(MockResponse.mock_ids), "objectIDs": MockResponse.mock_ids}
    return MockResponse

@pytest.fixture
def mock_response_sample_object(sample_object):
    
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return sample_object
    return MockResponse

@pytest.fixture
def object_id():
    return 1

@pytest.fixture
def search_query():
    return "sunflowers"

@pytest.fixture
def sample_object(object_id):
    with open(DATA_DIR / f"object_{object_id}.json") as f:
        return json.load(f)
