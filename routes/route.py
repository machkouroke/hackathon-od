from fastapi import APIRouter, Depends

import osmnx as ox
import networkx as nx

from dependances.dependance import get_db
from model.entity.Incident import Incident
from utilities.Executor import Executor

router = APIRouter()


@router.post("/urgences")
async def root(inc: Incident, database=Depends(get_db)):
    print(inc.longitude)
    return {
"sucess": True,
"data": Executor.run(inc,database)}



