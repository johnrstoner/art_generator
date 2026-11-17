import time
from functools import wraps
import requests

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"
REQUEST_TIMEOUT = 10 # in seconds
MAX_REQUESTS_PER_SECOND = 80  # Met API limit is 80 requests/second; See https://metmuseum.github.io/
MIN_INTERVAL = 60 / MAX_REQUESTS_PER_SECOND
_last_call = 0.0

def rate_limited(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global _last_call
        wait = MIN_INTERVAL - (time.monotonic() - _last_call)
        if wait > 0:
            time.sleep(wait)
        _last_call = time.monotonic()
        return func(*args, **kwargs)
    return wrapper

class ArtworkNotFound(Exception):
    def __init__(self, object_id):
        self.object_id = object_id
        super().__init__(f"Artwork {object_id} not found")

@rate_limited
def get_object_ids() -> list[int]:
    # Fetches a list of all object ids of publicly available works in the museum's database
    response = requests.get(f"{BASE_URL}/objects", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()["objectIDs"]

@rate_limited
def get_object(object_id: int) -> dict:
    # Fetches a work based on its id. Can fetch non-publicly available artwork, check the 'isPublicDomain' (bool) field of the returned dictionary
    response = requests.get(f"{BASE_URL}/objects/{object_id}", timeout=REQUEST_TIMEOUT)
    if response.status_code == 404:
        raise ArtworkNotFound(object_id)
    response.raise_for_status()
    return response.json()

@rate_limited
def search(q: str) -> list[int]:
    # Searches using the query passed
    response = requests.get(f"{BASE_URL}.1/search?q={q}")
    response.raise_for_status()
    return response.json()["objectIDs"]
