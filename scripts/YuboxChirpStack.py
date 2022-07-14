import logging
import re
import requests
import random as rd

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

    # Colores
    "UserWarning: color argument of Icon should be one of: {'darkpurple', 'white', 'black', 'pink', 'lightred', 'lightgreen', 'orange', 'cadetblue', 'gray', 'lightgray', 'purple', 'darkgreen', 'red', 'darkred', 'darkblue', 'beige', 'lightblue', 'blue', 'green'}."
    listColor = ['darkgreen','darkblue', 'purple',  'darkred',  'lightgreen' ,'darkpurple']
    contador = 0

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

            color = listColor[contador]
            contador+=1


            # Agrego las id al dict
            dic[id] = {
                "name": name,
                "color": color,
                "latitud": latitude,
                "longitud": longitude
            }
        print(dic)

        return dic


    else:
        log.error(gateways.text)
        return []