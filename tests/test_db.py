import sqlite3

from art_generator import db


def test_init_db_creates_artworks_table(conn: sqlite3.Connection):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='artworks'"
    ).fetchone()
    assert row is not None


def test_object_id_is_primary_key(conn: sqlite3.Connection):
    columns = conn.execute("PRAGMA table_info(artworks)").fetchall()
    # each row: (cid, name, type, notnull, default, pk)
    pk_columns = [col[1] for col in columns if col[5]]
    assert pk_columns == ["object_id"]


def test_init_db_is_safe_to_run_twice(tmp_path):
    path = tmp_path / "test.db"
    db.init_db(path).close()
    db.init_db(path).close()  # IF NOT EXISTS: should not raise

def test_add_artwork_adds_row(conn: sqlite3.Connection, sample_object: dict):
    db.add_artwork(conn, sample_object)
    rows = conn.execute("SELECT * FROM artworks").fetchall()
    assert len(rows) == 1
    assert rows[0][0] == sample_object["objectID"]
    assert rows[0][1] == sample_object["title"]

def test_add_artwork_twice_keeps_one_row(conn: sqlite3.Connection, sample_object: dict):
    db.add_artwork(conn, sample_object)
    db.add_artwork(conn, sample_object)

    count = conn.execute("SELECT COUNT(*) FROM artworks").fetchone()[0]
    assert count == 1

def test_list_artworks_returns_artworks(conn: sqlite3.Connection, sample_object_list: dict):
    insert_statement = (
            f"INSERT OR REPLACE INTO artworks ({', '.join(db.COLUMNS)}) "
            f"VALUES ({', '.join('?' * len(db.COLUMNS))})"
        )

    cur = conn.cursor()
    for sample_object in sample_object_list:
        values = tuple(sample_object.get(db.FIELD_MAP[col]) for col in db.COLUMNS)
        cur.execute(insert_statement, values)

    rows = db.list_artworks(conn)
    assert len(rows) == 3
    """
    object_id
    title
    is_public_domain
    object_date
    artist_display_name
    primary_image
    """
    assert rows[0][0] == 1
    assert rows[0][1] == "One-dollar Liberty Head Coin"
    assert rows[0][2] == False
    assert rows[0][10] == "1853"
    assert rows[0][11] == "James Barton Longacre"
    assert rows[0][14] == ""

    assert rows[1][0] == 2
    assert rows[1][1] == "Ten-dollar Liberty Head Coin"
    assert rows[1][2] == False
    assert rows[1][10] == "1901"
    assert rows[1][11] == "Christian Gobrecht"
    assert rows[0][14] == ""

    assert rows[2][0] == 3
    assert rows[2][1] == "Two-and-a-Half Dollar Coin"
    assert rows[2][2] == False
    assert rows[2][10] == "1909\u201327"
    assert rows[2][11] == ""
    assert rows[0][14] == ""
    
