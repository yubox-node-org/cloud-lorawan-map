import logging
import json
from threading import Thread
from time import sleep
from flask import Flask, render_template
from scripts.logger import MyHandler
from scripts.YuboxInfluxDb import YuboxInfluxDb
from scripts.YuboxChirpStack import getGatewayChirpStack
from scripts.YuboxMapLora import createHtmlMapLora

# Configuro el logger
log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(MyHandler())
app = Flask(__name__)

@app.route("/")
def home_map():
    return render_template("mapa.html")

def ThreadUpdateMap(InfluxDb,gateways):
    while(True):
        print("Actualizando Mapa")
        createHtmlMapLora(InfluxDb, gateways)
        sleep(60)

if __name__ == "__main__":
    # Cargo el archivo Json
    jsonConfig = json.load(open("scripts/setup.json"))

    # Creo la base de Datos
    jsonInfluxDb = jsonConfig["InfluxDb"]

    urlInfluxDb = jsonInfluxDb["url"]
    tokenInfluxDb = jsonInfluxDb["token"]

    InfluxDb = YuboxInfluxDb(url=urlInfluxDb, jsonToken = tokenInfluxDb)

    # Obtengo los gateways
    jsonChirpStack = jsonConfig["ChirpStack"]

    urlChirpStack = jsonChirpStack["url"]
    tokenChirpStack = jsonChirpStack["token"]

    gateways = getGatewayChirpStack(url = urlChirpStack, token = tokenChirpStack)
    Thread(target=ThreadUpdateMap, daemon=True, args=(InfluxDb,gateways,)).start()

    # Inicio el APP
    app.run()








