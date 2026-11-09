import sqlite3

import pytest

from art_generator import db


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
    