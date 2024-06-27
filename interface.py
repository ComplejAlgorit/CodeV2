import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class DeliverySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Entregas")

  
        self.start_label = tk.Label(root, text="Seleccionar Almacén de Inicio:")
        self.start_label.pack(pady=5)

        self.start_combobox = ttk.Combobox(root, state="readonly")
        self.start_combobox.pack(pady=5)

        self.end_label = tk.Label(root, text="Seleccionar Tienda de Destino:")
        self.end_label.pack(pady=5)

        self.end_combobox = ttk.Combobox(root, state="readonly")
        self.end_combobox.pack(pady=5)

        self.find_route_button = tk.Button(root, text="Encontrar Ruta", command=self.find_route)
        self.find_route_button.pack(pady=10)

        self.graph = None
        self.nodes = None
        self.edges = None

    def find_route(self):
        start_node = self.start_combobox.get()
        end_node = self.end_combobox.get()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = DeliverySystemApp(root)
    root.mainloop()
