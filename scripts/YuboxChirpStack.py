import logging
import re
import requests
import random

# Sistema de Log
log = logging.getLogger('InfluxDb')

def getGatewayChirpStack(url:str, token:str):
    # Inicio la seccion
    seccion = requests.Session()
    seccion.headers.update({"Authorization": "Bearer " + token})

    # Realizo la peticion a la API
    getUrl = url+"/api/gateways"
    data = {
        "limit":10
    }
    
    # Peticion
    gateways = seccion.get(getUrl, params= data)

    if gateways.reason == "OK":
        log.debug("Peticion ChirpstackAPI correcta")
        dictGateways = gateways.json()

        # Creo el diccionario donde guardare la informacion
        dic = {}

        # Recorro los resultados
        for gateway in dictGateways["result"]:
            # Obtengo informacion del gateway
            id = gateway["id"]
            name = gateway["name"]

            latitude = gateway["location"]["latitude"]
            longitude = gateway["location"]["longitude"]

            color = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]

            # Agrego las id al dict
            dic[id] = {
                "name": name,
                "color": color[0],
                "latitud": latitude,
                "longitud": longitude
            }
        return dic

    else:
        log.error(gateways.text)
        return []