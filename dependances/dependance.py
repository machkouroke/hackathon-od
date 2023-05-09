from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database
import osmnx as ox
import networkx as nx
from config.Setting import get_settings


async def get_db() -> Database:
    settings = get_settings()
    uri = f"mongodb+srv://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}" \
          f"@examen-mongo-db.gl2kput.mongodb.net/?retryWrites=true&w=majority"
    return MongoClient(uri)[settings.DB_NAME]


async def get_maps() -> nx.MultiDiGraph:
    return ox.graph_from_place('Khouribga, Maroc', network_type='drive')
