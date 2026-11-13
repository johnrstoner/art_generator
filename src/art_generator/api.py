import requests

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"
REQUEST_TIMEOUT = 10 # in seconds
# MAX_REQUESTS_PER_SECOND = 80  # Met API limit is 80 requests/second; not enforced yet. See https://metmuseum.github.io/

class ArtworkNotFound(Exception):
    def __init__(self, object_id):
        self.object_id = object_id
        super().__init__(f"Artwork {object_id} not found")

def get_object_ids() -> list[int]:
    # Fetches a list of all object ids of publicly available works in the museum's database
    response = requests.get(f"{BASE_URL}/objects", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()["objectIDs"]

def get_object(object_id: int) -> dict:
    # Fetches a work based on its id. Can fetch non-publicly available artwork, check the 'isPublicDomain' (bool) field of the returned dictionary
    response = requests.get(f"{BASE_URL}/objects/{id}", timeout=REQUEST_TIMEOUT)
    if response.status_code == 404:
        raise ArtworkNotFound(object_id)
    response.raise_for_status()
    return response.json()

def search(q: str) -> list[int]:
    # Searches using the query passed
    response = requests.get(f"{BASE_URL}.1/search?q={q}")
    response.raise_for_status()
    return response.json()["objectIDs"]
