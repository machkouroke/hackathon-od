from model.entity.Model import Model


class Incident(Model):
    name: str
    description: str = ""
    latitude: float
    longitude: float
    level: int
