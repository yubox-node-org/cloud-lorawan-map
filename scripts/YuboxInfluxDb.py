"""
Autor: Adrian Vidal Bazurto Onofre
Dowload: https://drive.google.com/file/d/1xoCaiCErqYGzbaWUhiyx9EQrbvnpsi_5/view?usp=sharing
Herramienta basada en la libreria 'influxdb-client-python' para lectura y escritura de InfluxDb utilizada en Yubox
"""

from pandas.core.frame import DataFrame
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import json
import logging
from datetime import datetime

#Sistema de Log
log = logging.getLogger('InfluxDb')

class YuboxInfluxDb:
  def __init__(self, url:str, jsonToken:dict)-> None:
    # Informacion del Servidor
    self.url    = url

    # Obtenemos el Token
    self.token = jsonToken

    # Datos para despues
    self.client = None
    self.query_api = None
    self.write_api = None


  def _connect(self,mode,org) -> bool:
    """ Funcion interna que realiza la conexion con InfluxDb
    :return:
    """
    # Obtengo el token necesario
    if (org not in self.token):
        log.error(f"No se recibio ningun token para la organizacion '{org}'")
        return False
    else:
        if (mode == "w"):
            mode_text = "write"
        elif (mode == "r"):
            mode_text = "read"

        # Valido si exite el token
        if pd.isna(self.token[org][mode_text]):
            log.error(f"La organizacion '{org}' no tiene ningun token para el modo '{mode_text}'")
            return False

        else:
            token = self.token[org][mode_text]

    try:
    # Creo el objeto client
        self.client = InfluxDBClient(url=self.url, token=token, org=org)
        self.query_api = self.client.query_api()
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        log.info(f"Conectado a InfluxDb, a la organizacion {org}")
        return True

    except OSError as err:
        log.error("OS error: {0}".format(err))
        return False

    except BaseException as err:
        log.error(f"{err}")
        return False


  def _disconect(self) -> None:
    """ Funcion interna que realiza la desconexion con InfluxDb
    :return:
    """
    self.client.close()


  def query_data(self, org, query) -> DataFrame:
    # Me conecto
    if not(self._connect("r", org)):
        log.error("Se cancela la consulta")
        return pd.DataFrame([])

    try:
        #Obtengo el csv del query
        log.debug(f"Intentando realizar consulta\n {query}\n a la organzacion '{org}'")
        csv_result = self.query_api.query_csv(query=query)
        list_result = list(csv_result)
        #Valido los datos 
        if(len(list_result)>1):
            column = list_result[3]
            data = list_result[4:-1]
            df = pd.DataFrame(data,columns=column)
        else:
            df = pd.DataFrame([])

        log.info("Consulta satisfatoria")

    except OSError as err:
        log.error("OS error: {0}".format(err))
        df = pd.DataFrame([])

    except BaseException as err:
        log.error(f"{err}")
        df = pd.DataFrame([])

    self._disconect()
    return df

  def write_data(self,org,_measurement,MAC,JsonData,gwid,version,bucket="samples"):
    try:
        if (self.token[org]["write"]!= None):
            #Procedo a conectarme 
            self._connect("w", org)

            #Valido que la mac este completa, caso contrario la completamos
            if len(MAC)<16:
                mac = MAC+"0000"
            else:
                mac = MAC

            #Tomo el tiempo actual
            now = datetime.utcnow()

            #Recorro los datos
            for dato, valor in JsonData.items():
                #Debo validar si el valor es Float
                if(isinstance(valor,float) or isinstance(valor,int)):
                    #Creo el Punto a utilizar
                    p = Point(_measurement).tag("firmware_variant", version).tag("devid",mac.lower()).tag("gwid",gwid).field(dato,float(valor)).time(now.strftime("%Y-%m-%dT%H:%M:%SZ"))
                    self.write_api.write(bucket=bucket, org=org, record=p,  time_precision='ms')

        
            self._disconect()

    except OSError as err:
        log.error("OS error: {0}".format(err))

    except BaseException as err:
        log.error(f"{err}")

