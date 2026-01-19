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
    unique_email = f"jobs_{uuid.uuid4().hex[:8]}@test.com"

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

# train task create test
@pytest.mark.asyncio
async def test_create_job(client):
    token = await get_token(client)

    response = await client.post(
        "/api/jobs",
        json={"epochs": 10, "batch_size": 16},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["epochs"] == 10
    assert response.json()["batch_size"] == 16
    assert response.json()["status"] == "pending"

# train task list look up test
@pytest.mark.asyncio
async def test_get_jobs(client):
    token = await get_token(client)

    response = await client.get(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# unauthorization access test
@pytest.mark.asyncio
async def test_jobs_unauthorized(client):
    response = await client.get("/api/jobs")
    assert response.status_code == 401