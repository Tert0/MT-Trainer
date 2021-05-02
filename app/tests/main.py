from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_secret():
    response = client.get("/secret")
    assert response.status_code == 403

