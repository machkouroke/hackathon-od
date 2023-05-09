from pymongo import MongoClient
from pymongo.database import Database

from config.Setting import get_settings


async def get_db() -> Database:
    settings = get_settings()
    uri = f"mongodb+srv://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}" \
          f"@examen-mongo-db.gl2kput.mongodb.net/?retryWrites=true&w=majority"
    return MongoClient(uri)[settings.DB_NAME]
