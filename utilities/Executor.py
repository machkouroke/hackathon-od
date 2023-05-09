import networkx as nx
import osmnx as ox
from pymongo.database import Database

from model.entity.Incident import Incident
from model.entity.Vehicle import Vehicle
from model.enum.AlertKind import AlertKind
from model.enum.VehicleKind import VehicleKind


class Executor:

    @staticmethod
    def filtre_type_incident(vehicle: list["Vehicle"], alert: AlertKind) -> list["Vehicle"]:
        return [vehicle for vehicle in vehicle if vehicle.can_support(alert)]

    @staticmethod
    def get_final_fleet(vehicles: list[Vehicle], incident: Incident) -> list[Vehicle]:
        total_cap = 0
        fleet = []

        for vehicle in vehicles:
            if vehicle.capacity >= incident.level:
                fleet = [vehicle]
                break
            else:
                total_cap += vehicle.capacity
                fleet.append(vehicle)
                if total_cap >= incident.level:
                    break
        return fleet

    @staticmethod
    def run(incident: Incident, database: Database, maps: nx.MultiDiGraph):
        liste_vehicles = Vehicle.all(database)
        filtered_v_liste: list[Vehicle] = sorted(Vehicle.filtre_type_incident(liste_vehicles, incident.kind),
                                                 key=lambda x: x.haversine(incident))

        flotte_v = Executor.get_final_fleet(filtered_v_liste, incident)
        end = (incident.longitude, incident.latitude)
        data = []
        for vehicle in flotte_v:
            start = (vehicle.longitude, vehicle.latitude)
            start_node = ox.distance.nearest_nodes(maps, X=[start[0]], Y=[start[1]])[
                0]
            end_node = ox.distance.nearest_nodes(maps, X=[end[0]], Y=[end[1]])[0]
            shortest_path = nx.shortest_path(maps, start_node, end_node, weight='length')
            path = [{"latitude": maps.nodes[node]['y'], "longitude": maps.nodes[node]["x"]} for node in shortest_path]
            data += [{"typeVehicle": vehicle.kind, "typeIncident": incident.kind, "path": path}]

        return data
