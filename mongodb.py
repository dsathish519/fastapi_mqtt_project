from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_mongo_db_client():
    client = await create_mongo_client()
    if client:
        return client
    else:
        raise ConnectionError("Could not connect to MongoDB")

# connecting to mongo client
async def create_mongo_client():
    try:
        mongo_url = os.getenv('MONGO_URL')
        client = AsyncIOMotorClient(mongo_url, 27017)
        logger.info('Connected to the mongo database successfully')
        return client
    except ConnectionFailure as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")

