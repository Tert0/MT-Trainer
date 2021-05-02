from fastapi.testclient import TestClient
from app.main import app
import random

client = TestClient(app)

def test_register(username, password, username2, password2):
    response = client.post("/register", params={
        "username": username,
        "password": password
    })
    assert response.status_code == 201
    assert response.text == 'Created User.'
    response = client.post("/register", params={
        "username": username2,
        "password": password2
    })
    assert response.status_code == 201
    assert response.text == 'Created User.'

def test_register_username_exists(username, password):
    response = client.post("/register", params={
        "username": username,
        "password": password
    })
    assert response.status_code == 409
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Username already exists'



def test_token(username, password):
    response = client.post('/token', params={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
    assert response.json()['token_type'] == 'bearer'

def test_not_authenicated():
    response = client.get('/authenticated')

    assert response.status_code == 403

def test_authenticated(user_headers):
    print(user_headers)
    response = client.get('/authenticated', headers=user_headers)

    assert response.status_code == 200

