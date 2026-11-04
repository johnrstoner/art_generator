import requests

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"
REQUEST_TIMEOUT = 10 # in seconds
# MAX_REQUESTS_PER_SECOND = 80  # Met API limit is 80 requests/second; not enforced yet. See https://metmuseum.github.io/


def get_object_ids() -> list[int]:
    # Fetches a list of all object ids in the museum's database
    response = requests.get(f"{BASE_URL}/objects", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()["objectIDs"]
    

