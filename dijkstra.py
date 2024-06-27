import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Cargar los archivos GeoJSON
nodes = gpd.read_file("nodes_callao.geojson")
edges = gpd.read_file("edges_callao.geojson")
mercados = gpd.read_file("filtered_mercados_callao.geojson")

# Asegurar que el CRS está correctamente establecido
nodes.crs = 'epsg:4326'
edges.crs = 'epsg:4326'
mercados.crs = 'epsg:4326'

# Convertir los GeoDataFrames a un grafo de NetworkX
G = nx.from_pandas_edgelist(edges, 'u', 'v', edge_attr=True, create_using=nx.DiGraph())

# Añadir los atributos de posición a los nodos en el grafo
for idx, node in nodes.iterrows():
    G.nodes[node['osmid']].update({'y': node.geometry.y, 'x': node.geometry.x})

# Función para obtener el nodo más cercano a un punto utilizando GeoPandas
def obtener_id_nodo_mas_cercano(graph, point):
    # Convertir el punto a un GeoDataFrame
    point_gdf = gpd.GeoDataFrame([{'geometry': Point(point.x, point.y)}], crs='epsg:4326')
    # Proyectar el punto y los nodos a un CRS proyectado
    point_gdf_projected = point_gdf.to_crs('EPSG:32718')  # Asegúrate de elegir un CRS adecuado para tu área de interés
    nodes_projected = nodes.to_crs('EPSG:32718')  # Usar el mismo CRS para los nodos
    # Calcular la distancia a todos los nodos en el CRS proyectado
    distances = nodes_projected.geometry.apply(lambda x: point_gdf_projected.distance(x).min())
    # Encontrar el ID del nodo más cercano
    closest_node = distances.idxmin()
    return nodes.iloc[closest_node]['osmid']

# Calcular los nodos más cercanos para cada mercado
mercados['closest_node'] = mercados.geometry.apply(lambda x: obtener_id_nodo_mas_cercano(G, x))

# Nodo de inicio y fin (ajustar según necesidad)
start_node = mercados.iloc[0]['closest_node']
end_node = mercados.iloc[1]['closest_node']

# Ejecutar el algoritmo de Dijkstra
path = nx.shortest_path(G, source=start_node, target=end_node, weight='length')
distances = nx.shortest_path_length(G, source=start_node, target=end_node, weight='length')

# Visualizar la ruta en el grafo
fig, ax = plt.subplots()
edges.plot(ax=ax, linewidth=0.5, edgecolor='black')
nodes.plot(ax=ax, markersize=5, color='red')

# Filtrar los nodos de la ruta y visualizarlos en azul
route_nodes = nodes[nodes['osmid'].isin(path)]
route_nodes.plot(ax=ax, markersize=10, color='blue')
plt.show()