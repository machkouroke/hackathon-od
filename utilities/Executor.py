import networkx as nx
import osmnx as ox
from pymongo.database import Database

from model.entity.Incident import Incident
from model.entity.Vehicle import Vehicle
from model.enum.AlertKind import AlertKind
from model.enum.VehicleKind import VehicleKind

v1 = Vehicle(name="v1",
             latitude=32.894653162718036,
             longitude=-6.91775606376365,
             kind=VehicleKind.FIRE_TRUCK,
             capacity=2,
             alert=[AlertKind.Aggression, AlertKind.ACCIDENT])
v2 = Vehicle(name="v2",
             latitude=33.894653162718036,
             longitude=-7.91775606376365,
             kind=VehicleKind.FIRE_TRUCK,
             capacity=2,
             alert=[AlertKind.Aggression, AlertKind.INCENDIE])


class Executor:

    @staticmethod
    def filtre_type_incident(vehicle: list["Vehicle"], alert: AlertKind) -> list["Vehicle"]:
        return [vehicle for vehicle in vehicle if vehicle.can_support(alert)]

    @staticmethod
    def get_final_fleet(vehicles: list[Vehicle], incident: Incident):
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
    def run(incident: Incident,database:Database):
        liste_vehicules =Vehicle.all(database)
        l_v = Vehicle.filtre_type_incident(liste_vehicules, AlertKind.ACCIDENT)
        L = []
        for v in l_v:
            L.append(v.haversine(incident))
        d = []
        d=[(l_v[i],L[i])  for i in range(len(l_v))]
        sorted_liste_tuples = sorted(d, key=lambda x: x[1])
        voitures_=[x[0] for x in sorted_liste_tuples]
        flotte_v = Executor.get_final_fleet(voitures_, incident)
        print(flotte_v)
        G = ox.graph_from_place('Khouribga, Maroc', network_type='drive')
        for f in flotte_v:
            end = (incident.longitude, incident.latitude)
            start = (f.latitude, f.longitude)
            print(start)
            start_node = ox.distance.nearest_nodes(G, X=[start[0]], Y=[start[1]])[
                0]
            end_node = ox.distance.nearest_nodes(G, X=[end[0]], Y=[end[1]])[0]
            shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
            #ox.plot_graph_route(G, shortest_path)
            path = [{"latitude": G.nodes[node]['y'], "longitude": G.nodes[node]["x"]} for node in shortest_path]
            return {
                "success": True,
                "data": [
                    {
                        "typeVehicle": "",
                        "typeIncident": "",
                        "path": path

                    }
                ]}
