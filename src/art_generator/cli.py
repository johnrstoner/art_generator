import art_generator.api as api

DEFAULT_DB = "artwork.db"

def fetch_artworks(q: str):
    artwork_ids = api.search(q)[:50] # limit to 50 for now
    artwork_objects = []
    for artwork_id in artwork_ids:
        try:
            artwork_objects.append(api.get_object(artwork_id))
        except api.ArtworkNotFound as e:
            print(f"Artwork with id {e.object_id} not found")
    return artwork_objects
    
def main():
    pass   
