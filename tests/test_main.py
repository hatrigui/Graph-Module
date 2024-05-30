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

#@pytest.mark.asyncio
#async def test_detect_cycles():
   # async with LifespanManager(app):
        #async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            #response = await ac.post("/nodes/", json={"title": "NodeA", "description": "Node A", "condition": "$A", "links": []})
            #assert response.status_code == 201
            #response = await ac.get("/nodes/cycles/")
            #assert response.status_code == 200

@pytest.mark.asyncio
async def test_add_links_between_nodes():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # Create two nodes
            response_a = await ac.post("/nodes/", json={"title": "NodeA", "description": "Node A", "condition": "$A", "links": []})
            assert response_a.status_code == 201
            node_a_id = response_a.json()["id"]

            response_b = await ac.post("/nodes/", json={"title": "NodeB", "description": "Node B", "condition": "$B", "links": []})
            assert response_b.status_code == 201
            node_b_id = response_b.json()["id"]

            # Add link between NodeA and NodeB
            response_link = await ac.patch(f"/nodes/{node_a_id}/link/{node_b_id}")
            assert response_link.status_code == 200

@pytest.mark.asyncio
async def test_detect_shortest_path():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # Create three nodes
            response_a = await ac.post("/nodes/", json={"title": "NodeA", "description": "Node A", "condition": "$A", "links": []})
            assert response_a.status_code == 201
            node_a_id = response_a.json()["id"]

            response_b = await ac.post("/nodes/", json={"title": "NodeB", "description": "Node B", "condition": "$B", "links": []})
            assert response_b.status_code == 201
            node_b_id = response_b.json()["id"]

            response_c = await ac.post("/nodes/", json={"title": "NodeC", "description": "Node C", "condition": "$C", "links": []})
            assert response_c.status_code == 201
            node_c_id = response_c.json()["id"]

            # Add links to form a path NodeA -> NodeB -> NodeC
            await ac.patch(f"/nodes/{node_a_id}/link/{node_b_id}")
            await ac.patch(f"/nodes/{node_b_id}/link/{node_c_id}")

            # Detect shortest path from NodeA to NodeC
            response_path = await ac.get(f"/nodes/shortest_path/?start_id={node_a_id}&end_id={node_c_id}")
            assert response_path.status_code == 200
            path = response_path.json()
            assert path == [node_a_id, node_b_id, node_c_id]
