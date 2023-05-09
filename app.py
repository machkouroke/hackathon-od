import learn as learn
import uvicorn
from fastapi import FastAPI
import osmnx as ox
import networkx as nx
from model.entity.Incident import Incident

app = FastAPI()
@app.post("/")
async def root(inc: Incident):
    G = ox.graph_from_place('Khouribga, Maroc', network_type='drive')
    end = (inc.longitude, inc.latitude)
    start = (-6.91775606376365, 32.894653162718036)
    start_node = ox.distance.nearest_nodes(G, X=[start[0]], Y=[start[1]])[0]
    end_node = ox.distance.nearest_nodes(G, X=[end[0]], Y=[end[1]])[0]
    shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
    ox.plot_graph_route(G, shortest_path)
    path=[{"latitude": G.nodes[node]['y'], "longitude": G.nodes[node]["x"]} for node in shortest_path]

    return {
       "sucess": True,
       "data":  [{"typeVehicle":"", "typeIncident": "" ,"path":path
     }]}

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
