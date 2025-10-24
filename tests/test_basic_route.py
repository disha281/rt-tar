# Note: For a true microservices test, this would use a client like httpx
# to make a request to the running service. For a simple unit test,
# we can use FastAPI's TestClient.
from fastapi.testclient import TestClient
from api_gateway.main import app

client = TestClient(app)

def test_read_root():
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "RT-TAR API Gateway is running."}

def test_get_dummy_route():
    """Test that the dummy route endpoint returns a valid response."""
    response = client.post("/v1/route")
    assert response.status_code == 200
    data = response.json()
    assert "agent_id" in data
    assert "path" in data
    assert isinstance(data["path"], list)
    assert data["status"] == "DUMMY_ROUTE_SUCCESS"
