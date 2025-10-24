from fastapi import FastAPI
from typing import List, Dict, Any

# Initialize the FastAPI app
app = FastAPI(
    title="RT-TAR API Gateway",
    description="Manages and routes requests to the RT-TAR microservices.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "RT-TAR API Gateway is running."}

@app.post("/v1/route")
def get_dummy_route() -> Dict[str, Any]:
    """
    Returns a dummy route for initial testing.
    This endpoint simulates a route calculation request and returns a static path.
    """
    return {
        "agent_id": "dummy_agent_007",
        "path": ["node_A", "node_B", "node_C"],
        "waypoints": [
            {"lat": 34.0522, "lon": -118.2437},
            {"lat": 34.0525, "lon": -118.2440},
            {"lat": 34.0528, "lon": -118.2443}
        ],
        "estimated_time_seconds": 120,
        "status": "DUMMY_ROUTE_SUCCESS"
    }
