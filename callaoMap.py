import osmnx as ox
import geopandas as gpd

# la red vial del distrito de Callao
place_name = "Callao, Lima"
G = ox.graph_from_address('Callao, Lima', network_type='drive', simplify=True, dist=2000)

num_nodes = len(G.nodes)
print(f"numero de nodos {num_nodes}")

# conversión GeoDataFrame
nodes, edges = ox.graph_to_gdfs(G)

# guarda los datos del grafo en archivos GeoJSON
nodes.to_file("nodes_callao.geojson", driver='GeoJSON')
edges.to_file("edges_callao.geojson", driver='GeoJSON')

print("se han guardado nodes_callao.geojson y edges_callao.geojson")
