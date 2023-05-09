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
    def run(incident: Incident, database: Database):
        liste_vehicules = Vehicle.all(database)
        filtered_v_liste: list[Vehicle] = sorted(Vehicle.filtre_type_incident(liste_vehicules, incident.kind),
                                                 key=lambda x: x.haversine(incident))

        flotte_v = Executor.get_final_fleet(filtered_v_liste, incident)
        G = ox.graph_from_place('Khouribga, Maroc', network_type='drive')
        end = (incident.longitude, incident.latitude)
        data = []
        for vehicule in flotte_v:
            start = (vehicule.longitude, vehicule.latitude)
            start_node = ox.distance.nearest_nodes(G, X=[start[0]], Y=[start[1]])[
                0]
            end_node = ox.distance.nearest_nodes(G, X=[end[0]], Y=[end[1]])[0]
            shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
            path = [{"latitude": G.nodes[node]['y'], "longitude": G.nodes[node]["x"]} for node in shortest_path]
            data += [{"typeVehicle": vehicule.kind, "typeIncident": incident.kind, "path": path}]

        return data
