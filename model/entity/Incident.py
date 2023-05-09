from pymongo.database import Database

from model.entity.Model import Model


class Incident(Model):
    name: str
    description: str = ""
    latitude: float
    longitude: float
    level: int

    def save(self, database: Database):
        database.Incidents.insert_one(self.to_bson())

    @staticmethod
    def all(database: Database):
        return [Incident(**incident) for incident in database.Incidents.find()]

