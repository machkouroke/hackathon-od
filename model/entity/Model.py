import inspect
from typing import Optional, Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from dependances.dependance import get_db
from model.entity.objectId import PydanticObjectId


class Model(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    database: Optional[Any] = None

    def dict(self, *args, **kwargs):
        return super().dict( exclude={"database"})

    def to_json(self, to_exclude: set = None) -> dict:
        if to_exclude is None:
            to_exclude = set()
        to_exclude.add("database")
        properties = [prop_name for prop_name, prop in inspect.getmembers(self.__class__) if isinstance(prop, property)]
        for prop in properties:
            getattr(self, prop)
        return jsonable_encoder(self, exclude=to_exclude)

    def to_bson(self, to_exclude=None):
        if to_exclude is None:
            to_exclude = set()
        to_exclude.add("database")
        data = self.dict(by_alias=True, exclude=to_exclude)
        if "_id" in data and data["_id"] is None:
            data.pop("_id")
        return data
