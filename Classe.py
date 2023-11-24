import pyodbc
import logging
import time
from sqlalchemy import create_engine

class db_conection():
    def __init__(self):
        self.connection = None

    def conexion(self):
        try:
            self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=192.168.116.190;DATABASE=DB_UN34;UID=aplicaciones1;PWD=aplicaciones$')
        except ConnectionError:
            logging.info('Falla de conexion a DB,reintentando en 5s')
            time.sleep(5)
            self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=192.168.116.190;DATABASE=DB_UN34;UID=aplicaciones1;PWD=aplicaciones$')
            logging.info('Falla de conexion a DB,reintentando en 5s')
        finally:
            cadena_conexion = 'mssql+pyodbc://aplicaciones1:aplicaciones$@192.168.116.190/DB_UN34?driver=ODBC+Driver+13+for+SQL+Server'
            self.engine = create_engine(cadena_conexion)
            self.connection = self.engine.connect() 


