import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

# cargando los archivos de los nodos/aristas
mercados_gdf = gpd.read_file('filtered_mercados_callao.geojson')
nodes = gpd.read_file("nodes_callao.geojson")
edges = gpd.read_file("edges_callao.geojson")

mercados_gdf.crs = 'epsg:4326'
nodes.crs = 'epsg:4326'
edges.crs = 'epsg:4326'

# figura con la biblioteca Matplotlib
fig, ax = plt.subplots(figsize=(10, 10))

# representación de las calles del Callao
edges.plot(ax=ax, linewidth=0.5, color='gray')

# nodos de las calles del Callao
nodes.plot(ax=ax, color='blue', markersize=50, label='Nodos')

# nodos de los mercados
mercados_gdf.plot(ax=ax, color='red', markersize=50, marker='o', label='Mercados')

#leyenda
ax.legend()

plt.show()
