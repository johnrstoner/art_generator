import json
import sqlite3
from pathlib import Path

import pytest

from art_generator import db

DATA_DIR = Path(__file__).parent / "data"
OBJECT_ID = 1

@pytest.fixture
def conn():
    connection = db.init_db(":memory:")
    yield connection
    connection.close()


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

def test_add_artwork_adds_row(conn: sqlite3.Connection):
    with open(DATA_DIR / f"object_{OBJECT_ID}.json") as file:
        sample_object = json.load(file)

    db.add_artwork(conn, sample_object)
    rows = conn.execute("SELECT * FROM artworks").fetchall()
    assert len(rows) == 1
    assert rows[0][0] == sample_object["objectID"]
    assert rows[0][1] == sample_object["title"]

