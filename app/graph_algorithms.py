# app/graph_algorithms.py
from collections import deque
from fastapi import HTTPException, status
from bson import ObjectId

async def dfs(node_id, path, visited, rec_stack, db):
    visited.add(node_id)
    rec_stack.add(node_id)
    path.append(node_id)
    node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    if node:
        for neighbor_id in node["links"]:
            if neighbor_id not in visited:
                if await dfs(neighbor_id, path, visited, rec_stack, db):
                    return True
            elif neighbor_id in rec_stack:
                cycle_start_index = path.index(neighbor_id)
                path[:] = path[cycle_start_index:]
                return True
    rec_stack.remove(node_id)
    path.pop()
    return False

async def detect_cycles(db):
    nodes = await db["nodes"].find().to_list(1000)
    visited = set()
    rec_stack = set()
    path = []
    for node in nodes:
        if str(node["_id"]) not in visited:
            if await dfs(str(node["_id"]), path, visited, rec_stack, db):
                return path
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cycles found")

async def bfs_shortest_path(start_id, end_id, db):
    queue = deque([(start_id, [start_id])])
    visited = set()
    while queue:
        current_node, path = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        node = await db["nodes"].find_one({"_id": ObjectId(current_node)})
        if not node:
            continue
        if current_node == end_id:
            return path
        for neighbor_id in node["links"]:
            if neighbor_id not in visited:
                queue.append((neighbor_id, path + [neighbor_id]))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No path found between nodes")
