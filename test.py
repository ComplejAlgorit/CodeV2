import math as m
import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Clase Graph
class Graph():
    def __init__(self):
        self.edges = defaultdict(set)
        self.weights = {}

    def add_edge(self, s, e, w):
        self.edges[s].add(e)
        self.edges[e].add(s)
        self.weights[(s, e)] = w
        self.weights[(e, s)] = w

    def add_directed_edge(self, s, e, w):
        self.edges[s].add(e)
        self.weights[(s, e)] = w

# Función para calcular el peso de las aristas
def weight(long1, lat1, long2, lat2, vm, h):
    mc = [1.0, 1.25, 1.5]
    d_lat = lat2 - lat1
    d_long = long2 - long1
    a = m.sin(d_lat / 2) ** 2 + m.cos(lat1) * m.cos(lat2) * m.sin(d_long / 2) ** 2
    c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))
    d = 6378 * c * 1000
    vm = vm / 3.6
    t = d / vm

    if (6 <= h <= 9) or (16 <= h <= 18):
        t *= np.random.choice(mc, 1, p=[0.70, 0.20, 0.10])
    if 16 <= h <= 18:
        t *= np.random.choice(mc, 1, p=[0.10, 0.70, 0.20])
    if (13 <= h <= 15) or (19 <= h <= 22):
        t *= np.random.choice(mc, 1, p=[0.10, 0.20, 0.70])

    return round(float(t / 60), 5)

# Algoritmo de Dijkstra
def dijkstra(graph, initial, end):
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Ruta no posible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    path = path[::-1]
    return path

# Datos de los nodos y aristas del Grafo de las tiendas y almacenes de Canta
nodes = {
    'A': (0, 0),
    'B': (1, 1),
    'C': (2, 1),
    'D': (3, 0),
    'E': (4, 1),
    'F': (5, 0),
    'G': (6, 0),
    'H': (7, 1),
    '1': (0, 1),
    '2': (1, 2),
    '3': (2, 2),
    '4': (3, 2),
    '5': (4, 2),
    '6': (5, 2),
    '7': (6, 2),
    '8': (7, 2),
}

edges = [
    ('A', 'B', 1),
    ('A', 'F', 5),
    ('A', 'E', 9),
    ('B', 'C', 2),
    ('B', 'F', 8),
    ('B', 'G', 3),
    ('C', 'D', 4),
    ('C', 'E', 4),
    ('D', 'G', 6),
    ('E', 'F', 7),
    ('E', 'G', 5),
    ('F', 'G', 3),
    ('G', 'H', 7),
    ('1', 'A', 3),
    ('1', 'B', 3),
    ('1', 'C', 4),
    ('1', 'D', 6),
    ('2', 'A', 2),
    ('2', 'E', 11),
    ('3', 'A', 4),
    ('3', 'H', 6),
    ('4', 'E', 7),
    ('4', 'H', 9),
    ('5', 'C', 3),
    ('5', 'E', 5),
    ('6', 'B', 5),
    ('6', 'C', 2),
    ('7', 'D', 9),
    ('7', 'F', 5),
    ('8', 'D', 3),
    ('8', 'F', 4),
]

# Solicitar entradas del usuario
hour = int(input("Ingrese la hora de inicio (0-23): "))
start_node = input("Ingrese el nodo de salida: ")
end_node = input("Ingrese el nodo final: ")

# Construir el grafo manualmente
G = Graph()
for s, e, w in edges:
    G.add_edge(s, e, w)

# Encontrar el camino más corto usando el algoritmo de Dijkstra
shortest_path = dijkstra(G, start_node, end_node)

# Mostrar el resultado
print("El camino más corto desde el nodo", start_node, "hasta el nodo", end_node, "es:", shortest_path)

# Graficar el grafo
G_nx = nx.Graph()
for s, e, w in edges:
    G_nx.add_edge(s, e, weight=w)

pos = nx.spring_layout(G_nx)
labels = {node: node for node in G_nx.nodes()}
edge_labels = {(s, e): f'{G.weights[(s, e)]:.2f}' for s, e in G_nx.edges()}

plt.figure(figsize=(12, 8))
nx.draw(G_nx, pos, with_labels=True, labels=labels, node_size=400, node_color='green', font_size=15, font_weight='bold')
nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=edge_labels, font_color='black')
plt.title('Grafo de las tiendas y almacenes de Canta')
plt.show()