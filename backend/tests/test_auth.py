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

# registration test
@pytest.mark.asyncio
async def test_register(client):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com" # 고유 이메일

    response = await client.post("/api/register", json={
        "email": unique_email,
        "password": "testpassplz999",
        "check_password": "testpassplz999"
    })
    assert response.status_code == 200
    assert "email" in response.json()

# login test
@pytest.mark.asyncio
async def test_login(client):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    # registration
    await client.post("/api/register", json={
        "email": unique_email,
        "password": "testpassplz123",
        "check_password": "testpassplz123"
    })

    # login (form 방식)
    response = await client.post("/api/login", data={
        "username": unique_email,
        "password": "testpassplz123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# wrong password test
@pytest.mark.asyncio
async def test_login_wrong_password(client):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"

    # registration
    await client.post("/api/register", json={
        "email": unique_email,
        "password": "testpassplz123",
        "check_password": "testpassplz123"
    })

    # wrong password
    response = await client.post("/api/login", data={
        "username": unique_email,
        "password": "wrongpassword123"
    })
    assert response.status_code == 401