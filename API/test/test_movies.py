from fastapi.testclient import TestClient

from ..main import app

responseClint = TestClient(app)

def test_create_movie():
    response = responseClint.post("/create_movie",
    json = {
        "image_url": "https://i.pinimg.com/736x/0c/c8/a7/0cc8a75bcdb94101557f8259c03ef1e9--il-padrino-godfather-movie.jpg",
        "image_url_type": "absolute",
        "director": "string",
        "imdb_score": 9.9,
        "timestamp": "2022-07-11T18:54:10.191199",
        "popularity": 9.9,
        "caption": "drama",
        "name": "God Father",
        "creator_id": 1
    })
    print(response.json())
    assert response.status_code == 201
