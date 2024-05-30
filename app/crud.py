# app/crud.py
from bson import ObjectId
from fastapi import HTTPException, status
from .models import Node, NodeResponse

def node_helper(node) -> NodeResponse:
    return NodeResponse(
        id=str(node["_id"]),
        title=node["title"],
        description=node.get("description"),
        condition=node.get("condition"),
        links=node["links"]
    )

async def create_node(node: Node, db):
    new_node = await db["nodes"].insert_one(node.model_dump())
    created_node = await db["nodes"].find_one({"_id": new_node.inserted_id})
    return node_helper(created_node)

async def read_nodes(db):
    nodes = await db["nodes"].find().to_list(100)
    return [node_helper(node) for node in nodes]

async def read_node(node_id: str, db):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    return node_helper(node)

async def update_node(node_id: str, update: Node, db):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    updated_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if len(updated_data) >= 1:
        update_result = await db["nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": updated_data})
        if update_result.modified_count == 1:
            updated_node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
            return node_helper(updated_node)
    existing_node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    if existing_node is not None:
        return node_helper(existing_node)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")

async def delete_node(node_id: str, db):
    if not ObjectId.is_valid(node_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    delete_result = await db["nodes"].delete_one({"_id": ObjectId(node_id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Node {node_id} successfully deleted."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")

async def add_link(node_id: str, target_node_id: str, db):
    if node_id == target_node_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot link node to itself")
    if not ObjectId.is_valid(node_id) or not ObjectId.is_valid(target_node_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")
    if target_node_id not in node['links']:
        node['links'].append(target_node_id)
        await db["nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": {"links": node['links']}})
    updated_node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    return node_helper(updated_node)

async def remove_link(node_id: str, target_node_id: str, db):
    if not ObjectId.is_valid(node_id) or not ObjectId.is_valid(target_node_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")
    if target_node_id in node['links']:
        node['links'].remove(target_node_id)
        await db["nodes"].update_one({"_id": ObjectId(node_id)}, {"$set": {"links": node['links']}})
    updated_node = await db["nodes"].find_one({"_id": ObjectId(node_id)})
    return node_helper(updated_node)

async def search_nodes(query: str, db):
    nodes = await db["nodes"].find({"condition": {"$regex": query, "$options": "i"}}).to_list(100)
    return [node_helper(node) for node in nodes]
