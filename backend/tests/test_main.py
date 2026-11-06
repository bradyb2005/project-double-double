from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestHealthCheck:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}