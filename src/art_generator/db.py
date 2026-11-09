import sqlite3

"""
Database for the MET tool. 
Supports the following functions:
1) Starts a connection to the database
2) Creates the database if it doesn't currently exist
3) Allows for creation, reading, update, and deletion of records
"""

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
    insert_statement = f"""INSERT OR REPLACE INTO artworks
    VALUES (
        {object['objectID']},
        "{object['title']}",
        {object['isPublicDomain']},
        "{object['objectName']}",
        "{object['medium']}",
        "{object['culture']}",
        "{object['period']}",
        "{object['dynasty']}",
        "{object['classification']}",
        "{object['department']}",
        "{object['objectDate']}",
        "{object['artistDisplayName']}",
        "{object['artistGender']}",
        "{object['artistNationality']}",
        "{object['primaryImage']}"
    );
    """

    cur = conn.cursor()
    cur.execute(insert_statement)
    conn.commit()
