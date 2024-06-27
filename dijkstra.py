import osmnx as ox
import networkx as nx
import geopandas as gpd
import heapq
import matplotlib.pyplot as plt

# Cargar los archivos GeoJSON
nodes = gpd.read_file("nodes_callao.geojson")
edges = gpd.read_file("edges_callao.geojson")
mercados = gpd.read_file("filtered_mercados_callao.geojson")

# Convertir los GeoDataFrames a un grafo de NetworkX
G = nx.from_pandas_edgelist(edges, 'u', 'v', edge_attr=True)

# Añadir los atributos de posición a los nodos en el grafo
for idx, node in nodes.iterrows():
    G.nodes[node['osmid']].update(node)

# Definir la función Dijkstra con condiciones de tráfico
def dijkstra_with_traffic(graph, start_node, end_node, traffic_conditions):
    queue = []
    heapq.heappush(queue, (0, start_node))
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start_node] = 0
    shortest_path = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph[current_node]:
            weight = graph[current_node][neighbor].get('length', 1)
            traffic_delay = traffic_conditions.get((current_node, neighbor), 0)
            distance = current_distance + weight + traffic_delay

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_node

    path = []
    while end_node:
        path.append(end_node)
        end_node = shortest_path.get(end_node)

    return path[::-1], distances

# Función para obtener el id del nodo más cercano
def obtener_id_nodo_mas_cercano(G, point):
    return ox.nearest_nodes(G, point.x, point.y)

# Añadir ids de nodos más cercanos a los mercados
mercados['closest_node'] = mercados.geometry.apply(lambda x: obtener_id_nodo_mas_cercano(G, x))

# Definir nodos de inicio y fin (ajustar según los mercados)
start_node = mercados.iloc[0]['closest_node']
end_node = mercados.iloc[1]['closest_node']

# Suponiendo que tenemos un diccionario con datos de tráfico
traffic_conditions = {
    (u, v): 5 for (u, v, data) in G.edges(data=True)  # Ajusta según sea necesario
}

# Ejecutar el algoritmo con condiciones de tráfico
path, distances = dijkstra_with_traffic(G, start_node, end_node, traffic_conditions)

# Visualizar la ruta en el grafo
fig, ax = plt.subplots()
edges.plot(ax=ax, linewidth=0.5, edgecolor='black')
nodes.plot(ax=ax, markersize=5, color='red')

# Filtrar los nodos de la ruta y visualizarlos en azul
route_nodes = nodes[nodes['osmid'].isin(path)]
route_nodes.plot(ax=ax, markersize=10, color='blue')
plt.show()
