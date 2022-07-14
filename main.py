import imp
from scripts.YuboxInfluxDb import YuboxInfluxDb
from scripts.logger import MyHandler
import logging
import json

# Configuro el logger
log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(MyHandler())

# Creo la base de Datos
jsonToken = json.load(open("scripts/YuboxInfluxDbToken.json"))
InfluxDb = YuboxInfluxDb(url="", jsonToken = jsonToken)

