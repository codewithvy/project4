import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/register', json={'username': 'test', 'password': '12345'})
    assert response.status_code == 200
    assert response.json == {"message": "User registered successfully!"}

def test_login_user(client):
    client.post('/register', json={'username': 'test', 'password': '12345'})
    response = client.post('/login', json={'username': 'test', 'password': '12345'})
    assert response.status_code == 200
    assert response.json == {"message": "Login successful!"}
