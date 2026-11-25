import sqlite3

"""
Database for the MET tool. 
Supports the following functions:
1) Starts a connection to the database
2) Creates the database if it doesn't currently exist
3) Allows for creation, reading, update, and deletion of records
"""

COLUMNS = (
    "object_id", "title", "is_public_domain", "object_name", "medium",
    "culture", "period", "dynasty", "classification", "department",
    "object_date", "artist_display_name", "artist_gender",
    "artist_nationality", "primary_image",
)

FIELD_MAP = {
    "object_id": "objectID",
    "title": "title",
    "is_public_domain": "isPublicDomain",
    "object_name": "objectName",
    "medium": "medium",
    "culture": "culture",
    "period": "period",
    "dynasty": "dynasty",
    "classification": "classification",
    "department": "department",
    "object_date": "objectDate",
    "artist_display_name": "artistDisplayName",
    "artist_gender": "artistGender",
    "artist_nationality": "artistNationality",
    "primary_image": "primaryImage"    
}

def init_db(db_path: str) -> sqlite3.Connection:
    creation_statement = """CREATE TABLE IF NOT EXISTS artworks (
        object_id INTEGER PRIMARY KEY,
        title TEXT,
        is_public_domain BOOLEAN,
        object_name TEXT,
        medium TEXT,
        culture TEXT,
        period TEXT,
        dynasty TEXT,
        classification TEXT,
        department TEXT,
        object_date TEXT,
        artist_display_name TEXT,
        artist_gender TEXT,
        artist_nationality TEXT,
        primary_image TEXT
    );"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(creation_statement)
    conn.commit()
    return conn

def add_artwork(conn: sqlite3.Connection, object: dict) -> None:

    insert_statement = (
        f"INSERT OR REPLACE INTO artworks ({', '.join(COLUMNS)}) "
        f"VALUES ({', '.join('?' * len(COLUMNS))})"
    )

    values = tuple(object.get(FIELD_MAP[col]) for col in COLUMNS)

    cur = conn.cursor()
    cur.execute(insert_statement, values)
    conn.commit()

def list_artworks(conn: sqlite3.Connection):
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM artworks").fetchall()
    return rows
