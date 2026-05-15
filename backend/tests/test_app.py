from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_is_accessible():
    response = client.get('/api/v1/auth/status')
    assert response.status_code == 200
    assert response.json()['success'] is True

def test_projects_endpoint_exists():
    response = client.get('/api/v1/projects')
    assert response.status_code in (200, 500)
