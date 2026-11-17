import art_generator.api as api
import art_generator.cli as cli


def test_fetch_artworks_returns_objects(monkeypatch, conn, search_query, object_ids_list, get_sample_object):
    def mock_search(q: str):
        return object_ids_list
    def mock_get_object(object_id: int):
        return get_sample_object(object_id)

    monkeypatch.setattr(api, "search", mock_search)
    monkeypatch.setattr(api, "get_object", mock_get_object)

    conn = cli.fetch_artworks(conn, search_query)

    rows = conn.execute("SELECT * FROM artworks").fetchall()
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
