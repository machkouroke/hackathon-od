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

    def save(self, database):
        database.Vehicle.insert_one(self.to_bson())

    @staticmethod
    def all(database: Database):
        return database.Vehicle.find()

    def can_support(self, incident):
        return incident in self.alert

    def haversine(self, incident: Incident):
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
    def filtre_type_incident(all: list, alert: AlertKind):
        for vehicle in all:
            if not vehicle.can_support(alert):
                all.remove(vehicle)
        return all


def tri_distances(vehicules: list[Vehicle], incident: Incident):
    dict_trie = {}
    L = [v.haversine(incident) for v in vehicules]
    d = {vehicules[i]: L[i] for i in range(len(L))}
    dist_triees = sorted(L)
    for value in dist_triees:
        for key, val in d.items():
            if val == value:
                dict_trie[key] = value
    return dict_trie
