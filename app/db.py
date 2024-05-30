# app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/graphdb")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.mongodb = app.mongodb_client["graphdb"]
    logger.info("Connected to MongoDB")
    yield
    app.mongodb_client.close()
    logger.info("Disconnected from MongoDB")

async def get_database():
    from .main import app  # Import here to avoid circular import issues
    return app.mongodb

async def create_indexes():
    from .main import app  # Import here to avoid circular import issues
    db = app.mongodb
    await db["nodes"].create_index("condition")
