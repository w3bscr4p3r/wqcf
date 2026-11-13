from fastapi.testclient import TestClient
from wqcf_api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_capabilities_fails_closed_when_provider_disabled(monkeypatch):
    monkeypatch.setenv("WQCF_PROVIDER", "disabled")
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    assert response.json()["status"] == "disabled"
