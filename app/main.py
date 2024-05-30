# app/main.py
from fastapi import FastAPI
from .routers.node_router import node_router
from .db import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(node_router, prefix="/nodes")


