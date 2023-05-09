from fastapi import APIRouter, Depends

from dependances.dependance import get_db, get_maps
from model.entity.Incident import Incident
from utilities.Executor import Executor

router = APIRouter()


@router.post("/urgences")
async def root(incident: Incident, database=Depends(get_db), maps=Depends(get_maps)):
    return {
        "success": True,
        "data": Executor.run(incident, database, maps)}
