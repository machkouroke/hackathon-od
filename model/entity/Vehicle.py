import math

import numpy as np
from pymongo.database import Database

from model.entity.Incident import Incident
from model.entity.Model import Model
from model.enum.AlertKind import AlertKind
from model.enum.VehicleKind import VehicleKind


class Vehicle(Model):
    name: str
    latitude: float
    longitude: float
    kind: VehicleKind
    capacity: int
    alert: list[AlertKind]

    def save(self, database) -> None:
        database.Vehicle.insert_one(self.to_bson())

    @staticmethod
    def all(database: Database) -> list["Vehicle"]:
        return [Vehicle(**vehicle) for vehicle in database.Vehicle.find()]

    def can_support(self, incident) -> bool:
        return incident in self.alert

    def haversine(self, incident: Incident) -> float:
        return (
                6367
                * 2
                * np.arcsin(
            np.sqrt(
                np.sin(
                    (
                            np.radians(self.latitude)
                            - math.radians(incident.latitude)
                    )
                    / 2
                )
                ** 2
                + math.cos(math.radians(incident.latitude))
                * np.cos(
                    np.radians(self.latitude)
                    * np.sin(
                        (
                                np.radians(self.longitude)
                                - math.radians(-incident.longitude)
                        )
                        / 2
                    )
                    ** 2
                )
            )
        )
        )

    @staticmethod
    def filtre_type_incident(vehicle: list["Vehicle"], alert: AlertKind) -> list["Vehicle"]:
        return [vehicle for vehicle in vehicle if vehicle.can_support(alert)]


