"""
Application health and root-route tests.

Description:
    This module verifies the publicly available application health endpoint.
"""

from fastapi.testclient import TestClient

from ..main import app
from starlette import status

client = TestClient(app)

def test_health_check():

    """
    Verify health check behavior.
    """
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'Status': 'Healthy'}
