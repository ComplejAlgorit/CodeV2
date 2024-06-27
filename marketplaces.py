import requests
import json

# Definir el bounding box para el distrito de Callao
bbox = {
    "south": -12.109,
    "west": -77.182,
    "north": -11.928,
    "east": -77.051
}

# query de overpass
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = f"""
[out:json];
node
  ["amenity"="marketplace"]
  ({bbox['south']},{bbox['west']},{bbox['north']},{bbox['east']});
out body;
"""

# obtención de datos
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

# se guardan en un GeoJSON
with open('mercados_callao.geojson', 'w') as outfile:
    json.dump(data, outfile, indent=2)

print("se han guardado mercados_callao.geojson")

# filtrado dentro del bbox
filtered_features = [
    feature for feature in data['elements']
    if bbox['south'] <= feature['lat'] <= bbox['north'] and bbox['west'] <= feature['lon'] <= bbox['east']
]

#  estructura de GeoJSON filtrada
filtered_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [feature['lon'], feature['lat']]
            },
            "properties": feature['tags']
        }
        for feature in filtered_features
    ]
}

# se guardan la filtración en un GeoJSON
with open('filtered_mercados_callao.geojson', 'w') as outfile:
    json.dump(filtered_data, outfile, indent=2)

print("se han guardado filtered_almacenes_callao.geojson")
