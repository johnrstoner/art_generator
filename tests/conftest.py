import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def object_id():
    return 1

@pytest.fixture
def sample_object(object_id):
    with open(DATA_DIR / f"object_{object_id}.json") as f:
        return json.load(f)
