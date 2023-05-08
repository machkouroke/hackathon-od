from model.entity.Model import Model
from model.enum.VehicleKind import VehicleKind


class Vehicle(Model):
    name: str
    latitude: float
    longitude: float
    kind: VehicleKind
    capacity: int
    alert: list = []

    def save(self):
        self.database.save_vehicle(self)

    def can_support(self, incident):
        return incident in self.alert
