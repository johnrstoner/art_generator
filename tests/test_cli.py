import art_generator.api as api
import art_generator.cli as cli

def test_main_doesnt_crash():
    cli.main()

def test_fetch_artworks_returns_objects(monkeypatch, search_query, object_ids_list, get_sample_object):
    def mock_search(q: str):
        return object_ids_list
    def mock_get_object(object_id: int):
        return get_sample_object(object_id)

    monkeypatch.setattr(api, "search", mock_search)
    monkeypatch.setattr(api, "get_object", mock_get_object)

    artwork_objects = cli.fetch_artworks(search_query)

    assert artwork_objects[0]["objectID"] == 1
    assert artwork_objects[0]["isPublicDomain"] == False
    assert artwork_objects[0]["primaryImage"] == ""
    assert artwork_objects[0]["title"] == "One-dollar Liberty Head Coin"
    assert artwork_objects[0]["artistDisplayName"] == "James Barton Longacre"
    assert artwork_objects[0]["objectDate"] == "1853"

    assert artwork_objects[1]["objectID"] == 2
    assert artwork_objects[1]["isPublicDomain"] == False
    assert artwork_objects[1]["primaryImage"] == ""
    assert artwork_objects[1]["title"] == "Ten-dollar Liberty Head Coin"
    assert artwork_objects[1]["artistDisplayName"] == "Christian Gobrecht"
    assert artwork_objects[1]["objectDate"] == "1901"

    assert artwork_objects[2]["objectID"] == 3
    assert artwork_objects[2]["isPublicDomain"] == False
    assert artwork_objects[2]["primaryImage"] == ""
    assert artwork_objects[2]["title"] == "Two-and-a-Half Dollar Coin"
    assert artwork_objects[2]["artistDisplayName"] == ""
    assert artwork_objects[2]["objectDate"] == "1909\u201327"
