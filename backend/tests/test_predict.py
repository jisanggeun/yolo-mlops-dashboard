import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app

# test용 client
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# login 후 token return
async def get_token(client):
    unique_email = f"predict_{uuid.uuid4().hex[:8]}@test.com"

    # registration
    await client.post("/api/register", json={
        "email": unique_email,
        "password": "testpassplz123",
        "check_password": "testpassplz123"
    })

    # login
    response = await client.post("/api/login", data={
        "username": unique_email,
        "password": "testpassplz123"
    })
    return response.json()["access_token"]

# model list look up
@pytest.mark.asyncio
async def test_get_models(client):
    token = await get_token(client)

    response = await client.get(
        "/api/predict/models",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# predict history look up test
@pytest.mark.asyncio
async def test_get_predict_history(client):
    token = await get_token(client)

    response = await client.get(
        "/api/predict/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# unauthorized access test
@pytest.mark.asyncio
async def test_predict_unauthorized(client):
    response = await client.get("/api/predict/models")
    assert response.status_code == 401