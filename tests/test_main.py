import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.main import app
from httpx import ASGITransport



@pytest.mark.asyncio
async def test_create_node():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/nodes/", json={"title": "Node1", "description": "First node", "condition": "$A AND $B", "links": []})
            assert response.status_code == 201

@pytest.mark.asyncio
async def test_read_nodes():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/nodes/")
            assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_node():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            create_response = await ac.post("/nodes/", json={"title": "Node1", "description": "First node", "condition": "$A AND $B", "links": []})
            assert create_response.status_code == 201
            node_id = create_response.json()["id"]
            response = await ac.get(f"/nodes/{node_id}")
            assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_node():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            create_response = await ac.post("/nodes/", json={"title": "Node1", "description": "First node", "condition": "$A AND $B", "links": []})
            assert create_response.status_code == 201
            node_id = create_response.json()["id"]
            response = await ac.put(f"/nodes/{node_id}", json={"title": "Updated Node1", "description": "Updated node", "condition": "$A AND $B", "links": []})
            assert response.status_code == 200



@pytest.mark.asyncio
async def test_detect_cycles():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/nodes/", json={"title": "NodeA", "description": "Node A", "condition": "$A", "links": []})
            assert response.status_code == 201
            response = await ac.get("/nodes/cycles/")
            assert response.status_code == 200
