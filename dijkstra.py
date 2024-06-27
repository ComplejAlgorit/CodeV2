import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Cargar datos
nodes = gpd.read_file("nodes_callao.geojson")
edges = gpd.read_file("edges_callao.geojson")
mercados = gpd.read_file("filtered_mercados_callao.geojson")

# Establecer sistema de referencia de coordenadas
nodes.crs = 'epsg:4326'
edges.crs = 'epsg:4326'
mercados.crs = 'epsg:4326'

# Crear grafo
G = nx.from_pandas_edgelist(edges, 'u', 'v', edge_attr=True, create_using=nx.DiGraph())

# Actualizar atributos de los nodos
for idx, node in nodes.iterrows():
    G.nodes[node['osmid']].update({'y': node.geometry.y, 'x': node.geometry.x})

# Función para obtener el nodo más cercano a un punto
def obtener_id_nodo_mas_cercano(graph, point):
    point_gdf = gpd.GeoDataFrame([{'geometry': Point(point.x, point.y)}], crs='epsg:4326')
    point_gdf_projected = point_gdf.to_crs('EPSG:32718')
    nodes_projected = nodes.to_crs('EPSG:32718')
    distances = nodes_projected.geometry.apply(lambda x: point_gdf_projected.distance(x).min())
    closest_node = distances.idxmin()
    return nodes.iloc[closest_node]['osmid']

# Asignar el nodo más cercano a cada mercado
mercados['closest_node'] = mercados.geometry.apply(lambda x: obtener_id_nodo_mas_cercano(G, x))

# Solicitar nombres de los mercados para el inicio y el final
nombre_inicio = input("Ingrese el nombre del mercado de inicio: ")
nombre_final = input("Ingrese el nombre del mercado final: ")

# Encontrar los nodos más cercanos para los mercados seleccionados
nodo_inicio = mercados[mercados['name'] == nombre_inicio]['closest_node'].values[0]
nodo_final = mercados[mercados['name'] == nombre_final]['closest_node'].values[0]

# Calcular la ruta más corta
path = nx.shortest_path(G, source=nodo_inicio, target=nodo_final, weight='length')

# Visualización
fig, ax = plt.subplots()
edges.plot(ax=ax, linewidth=0.5, edgecolor='black')
nodes.plot(ax=ax, markersize=5, color='red')
route_nodes = nodes[nodes['osmid'].isin(path)]
route_nodes.plot(ax=ax, markersize=10, color='blue')
mercado_nodes = nodes[nodes['osmid'].isin(mercados['closest_node'])]
mercado_nodes.plot(ax=ax, markersize=30, color='green', marker='^')

for idx, row in mercados.iterrows():
    plt.text(row.geometry.x, row.geometry.y, s=row['name'], fontsize=12, ha='right')

plt.show()