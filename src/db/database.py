import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.database = db.client[settings.DATABASE_NAME]
    logger.info("Connected to MongoDB successfully")

async def close_mongo_connection():
    """Close database connection"""
    logger.info("Closing connection to MongoDB...")
    db.client.close()
    logger.info("Disconnected from MongoDB")

async def get_database() -> AsyncIOMotorDatabase:
    return db.database