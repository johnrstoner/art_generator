import json
from pathlib import Path

import pytest
import requests

DATA_DIR = Path(__file__).parent / "data"

class FakeResponse:
    def __init__(self, payload=None, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")

    def json(self):
        return self.payload

@pytest.fixture
def make_response():
    def _make(payload, status_code):
        return FakeResponse(payload, status_code)
    return _make

@pytest.fixture
def object_id():
    return 1

@pytest.fixture
def mock_ids_payload():
    return {"objectIDs": [1, 2, 3]}

@pytest.fixture
def search_query():
    return "sunflowers"

@pytest.fixture
def sample_object(object_id):
    with open(DATA_DIR / f"object_{object_id}.json") as f:
        return json.load(f)
