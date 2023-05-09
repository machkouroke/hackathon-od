from fastapi import APIRouter, Depends

import osmnx as ox
import networkx as nx

from dependances.dependance import get_db
from model.entity.Incident import Incident
from utilities.Executor import Executor

router = APIRouter()


@router.post("/urgences")
async def root(incident: Incident, database=Depends(get_db)):
    return {
        "success": True,
        "data": Executor.run(incident, database)}
