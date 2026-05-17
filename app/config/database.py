from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from app.config.indexes import create_database_indexes
from app.config.settings import get_mongodb_url, get_settings


class MongoConnection:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongo = MongoConnection()


def get_database_name() -> str:
    return get_settings().database_name


async def connect_to_mongo() -> None:
    mongo_url = get_mongodb_url()
    database_name = get_database_name()
    client = AsyncIOMotorClient(
        mongo_url,
        serverSelectionTimeoutMS=5000,
        tz_aware=True,
    )

    try:
        await client.admin.command("ping")
    except Exception:
        client.close()
        raise

    mongo.client = client
    mongo.database = client[database_name]
    await create_database_indexes(mongo.database)


async def close_mongo_connection() -> None:
    if mongo.client is not None:
        mongo.client.close()

    mongo.client = None
    mongo.database = None


def get_database() -> AsyncIOMotorDatabase:
    if mongo.database is None:
        raise RuntimeError("Database connection has not been initialized.")

    return mongo.database


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return get_database()[collection_name]
