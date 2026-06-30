from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

_mongo_client = None

def _get_db():
    global _mongo_client
    if _mongo_client is None:
        try:
            _mongo_client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        except Exception:
            _mongo_client = None
    if _mongo_client:
        try:
            return _mongo_client.get_default_database()
        except Exception:
            return None
    return None
