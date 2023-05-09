from model.entity.Model import Model
from model.enum.AlertKind import AlertKind
from model.enum.VehicleKind import VehicleKind


class Vehicle(Model):
    name: str
    latitude: float
    longitude: float
    kind: VehicleKind
    capacity: int
    alert: list = [AlertKind.INCENDIE]

    def save(self):
        self.database.save_vehicle(self)

    def can_support(self, incident: AlertKind):
        return incident in self.alert
