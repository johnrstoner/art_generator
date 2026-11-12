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
def object_id():
    return 1

@pytest.fixture
def search_query():
    return "sunflowers"

@pytest.fixture
def sample_object(object_id):
    with open(DATA_DIR / f"object_{object_id}.json") as f:
        return json.load(f)
