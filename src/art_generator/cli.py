import sqlite3
import art_generator.api as api
import art_generator.db as db

DEFAULT_DB = "artwork.db"

def fetch_artworks(conn: sqlite3.Connection, q: str):
    artwork_ids = api.search(q)[:50] # limit to 50 for now
    artwork_objects = []
    for artwork_id in artwork_ids:
        try:
            artwork_object = api.get_object(artwork_id)
            artwork_objects.append(artwork_object)
            print(f"Artwork with id {artwork_id} found: {artwork_object['title']}")
        except api.ArtworkNotFound as e:
            print(f"Artwork with id {e.object_id} not found")

    for artwork_object in artwork_objects:
        db.add_artwork(conn, artwork_object)

    return conn

    
def main():
    query = "sunflowers"
    conn = db.init_db(DEFAULT_DB)
    conn = fetch_artworks(conn, query)
    rows = db.list_artworks(conn)
    print(rows)
    conn.close()
    
