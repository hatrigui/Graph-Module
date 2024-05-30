# app/routers/node_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from bson import ObjectId
from ..models import Node, NodeResponse
from ..db import get_database
from ..crud import create_node, read_nodes, read_node, update_node, delete_node, add_link, remove_link, search_nodes
from ..graph_algorithms import detect_cycles, bfs_shortest_path

node_router = APIRouter()

@node_router.post("/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
async def create_node_route(node: Node, db=Depends(get_database)):
    return await create_node(node, db)

@node_router.get("/", response_model=List[NodeResponse])
async def read_nodes_route(db=Depends(get_database)):
    return await read_nodes(db)

@node_router.get("/{node_id}", response_model=NodeResponse)
async def read_node_route(node_id: str, db=Depends(get_database)):
    return await read_node(node_id, db)

@node_router.put("/{node_id}", response_model=NodeResponse)
async def update_node_route(node_id: str, update: Node, db=Depends(get_database)):
    return await update_node(node_id, update, db)

@node_router.delete("/{node_id}", response_model=dict)
async def delete_node_route(node_id: str, db=Depends(get_database)):
    return await delete_node(node_id, db)

@node_router.patch("/{node_id}/link/{target_node_id}", response_model=NodeResponse)
async def add_link_route(node_id: str, target_node_id: str, db=Depends(get_database)):
    return await add_link(node_id, target_node_id, db)

@node_router.patch("/{node_id}/unlink/{target_node_id}", response_model=NodeResponse)
async def remove_link_route(node_id: str, target_node_id: str, db=Depends(get_database)):
    return await remove_link(node_id, target_node_id, db)


@node_router.get("/cycles/", response_model=List[str])
async def detect_cycles_route(db=Depends(get_database)):
    return await detect_cycles(db)

@node_router.get("/shortest_path/", response_model=List[str])
async def find_shortest_path_route(start_id: str, end_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(start_id) or not ObjectId.is_valid(end_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    return await bfs_shortest_path(start_id, end_id, db)
