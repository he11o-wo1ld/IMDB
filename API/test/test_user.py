from fastapi.testclient import TestClient

from main import app

responseClint = TestClient(app)


data = {
    "username": "User",
    "email": "user@gmail.com",
    "password": "password"
}


def test_create_user():
    response = responseClint.post("/user", json=data)
    assert response.status_code == 200

def test_create_user_with_invalid_json():
    response = responseClint.post("/user", 
    json = {
        "urname": "User",
        "ema": "user@gmail.com",
        "paword": "password"
    })
    assert response.status_code == 422


