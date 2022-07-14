import folium
import os
from time import sleep

def CreatePoint(LoraMap, gateways, zip_gps)->folium.Map:
    incidents = folium.map.FeatureGroup()
    # Procedo a graficar todos los puntos en el mapa
    for lati, lon, gateway in zip_gps:
        try:
            lati = float(lati)
            lon = float(lon)
            color = gateways[gateway]["color"]
            incidents.add_child(
                folium.CircleMarker(
                    [lati, lon],
                    radius=5,  # define how big you want the circle markers to be
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.6
                )
            )
        except:
            pass
                    
    # Dibujo odos los puntos en el mapa
    LoraMap.add_child(incidents)

    return LoraMap


def CreateMapFolium(latitude, longitude, gateways)->folium.Map:
    #Creo el mapa
    LoraMap = folium.Map(location=[latitude, longitude], zoom_start=12)# display the map of Guayaquil

    # Procedo a dibujar en el mapa los gateway
    for gateway in gateways.values():
        latitud = gateway["latitud"]
        longitud = gateway["longitud"]
        color = gateway["color"]
        folium.Marker(location=[latitud, longitud],
                        popup=gateway["name"],
                        icon=folium.Icon(color=color, icon="fa-solid fa-wifi", prefix='fa')).add_to(LoraMap)

    return LoraMap


def createHtmlMapLora(YuboxInfluxDb, gateways):
    # Guayaquil latitude and longitude values
    latitude = -2.18333
    longitude = -79.8833
    
    # Creo el Folium Mapa
    LoraMap = CreateMapFolium(latitude=latitude, longitude=longitude, gateways=gateways)

    # Agrego los puntos
    query="""
    from(bucket: "samples")
    |> range(start: -800d, stop:now())
    |> filter(fn: (r) => r["devid"] == "7cdfa1061f5a0000")
    |> filter(fn: (r) => r["_measurement"] == "latitude" or r["_measurement"] == "longitude")
    |> timeShift(duration: -5h, columns: ["_start", "_stop", "_time"])
    |> truncateTimeColumn(unit: 1s)
    |> pivot(rowKey: ["_time"], columnKey: ["_measurement"], valueColumn: "_value")
    """

    df_GpsMap = YuboxInfluxDb.query_data(org = "yubox", query = query)
    point_gps = zip(df_GpsMap["latitude"],df_GpsMap["longitude"],df_GpsMap["gwid"])

    # Creo los mapa
    LoraMap = CreatePoint(LoraMap=LoraMap, zip_gps=point_gps, gateways=gateways)

    direccion = "templates/mapa.html"

    # Verifico si existe
    if (os.path.isfile(direccion)):
        os.remove(direccion)
        sleep(0.5)


    #Guardo el HTML
    LoraMap.save(direccion)