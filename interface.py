import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely.geometry import Point

class DeliverySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Entregas")

        # Cargar datos y preparar el grafo
        self.nodes = gpd.read_file("nodes_callao.geojson")
        self.edges = gpd.read_file("edges_callao.geojson")
        self.almacen = gpd.read_file("filtered_mercados_callao.geojson")
        self.nodes.crs = 'epsg:4326'
        self.edges.crs = 'epsg:4326'
        self.almacen.crs = 'epsg:4326'
        self.G = nx.from_pandas_edgelist(self.edges, 'u', 'v', edge_attr=True, create_using=nx.DiGraph())
        for idx, node in self.nodes.iterrows():
            self.G.nodes[node['osmid']].update({'y': node.geometry.y, 'x': node.geometry.x})

        # Interfaz de usuario
        self.start_label = tk.Label(root, text="Seleccionar Almacén de Inicio:")
        self.start_label.pack(pady=5)

        self.start_combobox = ttk.Combobox(root, state="readonly", values=list(self.almacen['name']))
        self.start_combobox.pack(pady=5)

        self.end_label = tk.Label(root, text="Seleccionar Almacén de Destino:")
        self.end_label.pack(pady=5)

        self.end_combobox = ttk.Combobox(root, state="readonly", values=list(self.almacen['name']))
        self.end_combobox.pack(pady=5)

        self.find_route_button = tk.Button(root, text="Encontrar Ruta", command=self.find_route)
        self.find_route_button.pack(pady=10)

    def find_route(self):
        if 'closest_node' not in self.almacen.columns:
            print("Error: La columna 'closest_node' no existe en el DataFrame .")
            return
        nombre_inicio = self.start_combobox.get()
        nombre_final = self.end_combobox.get()
        nodo_inicio = self.almacen[self.almacen['name'] == nombre_inicio]['closest_node'].values[0]
        nodo_final = self.almacen[self.almacen['name'] == nombre_final]['closest_node'].values[0]
        path = nx.shortest_path(self.G, source=nodo_inicio, target=nodo_final, weight='length')
        self.visualize_route(path)

    def visualize_route(self, path):
       
        fig, ax = plt.subplots()
        self.edges.plot(ax=ax, linewidth=0.5, edgecolor='black')
        self.nodes.plot(ax=ax, markersize=5, color='red')
        route_nodes = self.nodes[self.nodes['osmid'].isin(path)]
        route_nodes.plot(ax=ax, markersize=10, color='blue')
        mercado_nodes = self.nodes[self.nodes['osmid'].isin(self.almacen['closest_node'])]
        mercado_nodes.plot(ax=ax, markersize=30, color='green', marker='^')
        for idx, row in self.almacen.iterrows():
            plt.text(row.geometry.x, row.geometry.y, s=row['name'], fontsize=12, ha='right')
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = DeliverySystemApp(root)
    root.mainloop()