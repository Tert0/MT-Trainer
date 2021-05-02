from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate(user_headers):
    response = client.get("/exercise/generate", headers=user_headers)
    assert response.status_code == 200
    assert 'factor1' in response.json()
    assert 'factor2' in response.json()

def test_get_exercise(user_headers):
    response = client.get('/exercise/get', headers=user_headers)
    assert response.status_code == 200
    assert 'exercise' in response.json()
    assert 'factor1' in response.json()['exercise']
    assert 'factor2' in response.json()['exercise']


def test_check_right(user_headers):
    response = client.get('/exercise/get', headers=user_headers)
    assert response.status_code == 200
    assert 'exercise' in response.json()
    assert 'factor1' in response.json()['exercise']
    assert 'factor2' in response.json()['exercise']
    factor1, factor2 = response.json()['exercise'].values()
    response = client.post('/exercise/check', headers=user_headers, params={
        "user_result": factor1 * factor2
    })
    assert response.status_code == 200
    assert 'result' in response.json()
    assert response.json()['result'] == True
    
def test_check_wrong(user_headers):
    response = client.get('/exercise/get', headers=user_headers)
    assert response.status_code == 200
    assert 'exercise' in response.json()
    assert 'factor1' in response.json()['exercise']
    assert 'factor2' in response.json()['exercise']
    factor1, factor2 = response.json()['exercise'].values()
    response = client.post('/exercise/check', headers=user_headers, params={
        "user_result": factor1 * factor2 + 1
    })

    assert response.status_code == 200
    assert 'result' in response.json()
    assert response.json()['result'] == False


