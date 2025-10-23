import pytest
from api.index import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_health(client):
    rv = client.get('/api/health')
    assert rv.status_code == 200
    assert rv.get_json() == {'ok': True}

def test_import_app():
    assert app is not None
    from flask import Flask
    assert isinstance(app, Flask)
