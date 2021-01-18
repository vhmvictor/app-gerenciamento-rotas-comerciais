import folium, os
from db import connection_db

route_bounds = []
client_coord = []

# Route bounds
cur = connection_db.cur
query = "SELECT * from rota where data_deletacao is null"
cur.execute(query)
route_result = cur.fetchall()

# Client coordenate
cur = connection_db.cur
query = "SELECT * from cliente where data_deletacao is null"
cur.execute(query)
client_result = cur.fetchall()
    
for row in route_result:
    route_bounds.append(
        {
            "type": "Feature",
            "properties": {"name": row[2]},
            "geometry": {
                "type": "Polygon",
                "coordinates": [row[1]]
            }
        })

for row in client_result:
    client_coord.append(
        {
            "type": "Feature",
            "properties": {"name": row[1]},
            "geometry": {
                "type": "Point",
                "coordinates": row[2]
            }
        })

# Map config
m = folium.Map(location=[-16.712164696208113, -49.28449630737305], zoom_start=14)

for row in route_bounds:
    folium.GeoJson(row, tooltip=row.get('properties').get('name')).add_to(m)

for row in client_coord:
    folium.GeoJson(row, tooltip=row.get('properties').get('name')).add_to(m)

m.save("map.html")
