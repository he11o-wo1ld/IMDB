from fastapi.testclient import TestClient

from main import app

responseClint = TestClient(app)

data = {
        "image_url": "https://i.pinimg.com/736x/0c/c8/a7/0cc8a75bcdb94101557f8259c03ef1e9--il-padrino-godfather-movie.jpg",
        "image_url_type": "absolute",
        "director": "Director",
        "imdb_score": 9.9,
        "timestamp": "2022-07-11T18:54:10.191199",
        "popularity": 9.9,
        "caption": "drama",
        "name": "God Father",
        "creator_id": 1
    }

def test_create_movie():
    response = responseClint.post("post/create_movie", json = data)
    print(response.json())
    assert response.status_code == 200


def test_create_movie_with_invalid_json():
    response = responseClint.post("/post/create_movie", 
    json = {
        "image_url": "https://i.pinimg.com/736x/0c/c8/a7/0cc8a75bcdb94101557f8259c03ef1e9--il-padrino-godfather-movie.jpg",
        "image_url_type": "absolute",
        "imdb_score": 9.9,
        "timesmp": "2022-07-11T18:54:10.191199",
        "popularity": 9.9,
        "capon": "drama",
        "name": "God Father",
        "creator_id": 1
    })
    assert response.status_code == 422

def test_get_all_movies():
    response = responseClint.get("/post/all")
    assert response.status_code == 200


def test_get_movie_by_id():
    response = responseClint.get("/post/get_movie/1")
    assert response.status_code == 200


def test_get_movie_by_invalid_id():
    response = responseClint.get("/post/get_movie/1001")
    assert response.status_code == 404


# def test_delete_movie_by_id():
#     response = responseClint.post("/post/delete/1")
#     assert response.status_code == 405

# def test_delete_movie_with_invalid_id():
#     response = responseClint.post("/post/delete/1006")
#     assert response.status_code == 405


def get_movie_by_caption():
    response = responseClint.get("/post/movie/drama")
    assert response.status_code == 200

def get_movie_by_caption():
    response = responseClint.get("/post/movie/fcvjhblk")
    assert response.status_code == 404
