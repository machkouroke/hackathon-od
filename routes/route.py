from fastapi import APIRouter

import osmnx as ox
import networkx as nx

from model.entity.Incident import Incident

router = APIRouter()


@router.post("/urgences")
async def root(inc: Incident):
    G = ox.graph_from_place('Khouribga, Maroc', network_type='drive')
    end = (inc.longitude, inc.latitude)
    start = (-6.91775606376365, 32.894653162718036)
    start_node = ox.distance.nearest_nodes(G, X=[start[0]], Y=[start[1]])[0]
    end_node = ox.distance.nearest_nodes(G, X=[end[0]], Y=[end[1]])[0]
    shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
    ox.plot_graph_route(G, shortest_path)
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
