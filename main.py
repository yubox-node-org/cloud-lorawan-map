from scripts.YuboxInfluxDb import YuboxInfluxDb
from scripts.YuboxChirpStack import getGatewayChirpStack
from scripts.logger import MyHandler
import logging
import json

# Configuro el logger
log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(MyHandler())

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
print(gateways)