from fastapi import APIRouter, Depends

import osmnx as ox
import networkx as nx

from model.entity.Incident import Incident
from model.entity.Vehicle import Vehicle
from model.enum.AlertKind import AlertKind


class Executor:
    all:list[Vehicle]
    alert:AlertKind
    def filtre_type_incident(self):

        for vehicle in self.all:
            if not vehicle.can_support(self.alert):
                self.all.remove(vehicle)
        return self.all

    def get_final_fleet(vehicles: list[Vehicle], incident: Incident):
        total_cap = 0
        fleet = []

        for vehicle in vehicles:
            if vehicle.cap >= incident.level:
                fleet = [vehicle]
                break
            else:
                total_cap += vehicle.cap
                fleet.append(vehicle)
                if total_cap >= incident.level:
                    break
        return fleet

    def run(self,incident:Incident):
        l_v=self.filtre_type_incident()
        L = []
        for v in l_v:
            L.append(v.haversine(incident))
        d = {}
        for i in range(len(l_v)):
            d[l_v[i]] = L[i]
        sorted_dict = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        flotte_v=self.get_final_fleet(list(sorted_dict.keys()),incident)
        G = ox.graph_from_place('Khouribga, Maroc', network_type='drive')
        end = (incident.longitude, incident.latitude)
        start = [(v.latitude,  v.longitude) for v in self.all]
        start_node = ox.distance.nearest_nodes(G, X=[start[0] for start in start], Y=[start[1] for start in start])[0]
        end_node = ox.distance.nearest_nodes(G, X=[end[0]], Y=[end[1]])[0]
        shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
        ox.plot_graph_route(G, shortest_path)
        path = [{"latitude": G.nodes[node]['y'], "longitude": G.nodes[node]["x"]} for node in shortest_path]

        return {
            "success": True,
            "data": [
                {
                    "typeVehicle": "",
                    "typeIncident": self.alert.value,
                    "path": path

                }
            ]}

