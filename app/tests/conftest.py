from fastapi.testclient import TestClient
import pytest
from app.main import app
from os import getenv

client = TestClient(app)


@pytest.fixture
def username():
    return getenv('TEST_USERNAME')


@pytest.fixture
def password():
    return getenv('TEST_PASSWORD')


@pytest.fixture
def username2():
    return getenv('TEST_USERNAME2')


@pytest.fixture
def password2():
    return getenv('TEST_PASSWORD2')


@pytest.fixture
def admin_username():
    return getenv('TEST_ADMIN_USERNAME')


@pytest.fixture
def admin_password():
    return getenv('TEST_ADMIN_PASSWORD')


@pytest.fixture
def user_headers(username, password):
    response = client.post('/token', params={
        "username": username,
        "password": password
    })
    return  {"Authorization": f"Bearer {response.json()['access_token']}"}

