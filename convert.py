import os
from PIL import Image
import pyodbc
import time
import logging

def img_to_png():
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=192.168.116.190;DATABASE=DB_UN34;UID=aplicaciones1;PWD=aplicaciones$')
        logging.info('Conectando a DB para subir Imagenes')
    except ConnectionError:
        time.sleep(5)
        logging.info('Falla conexion en DB')
    yourpath = "imagenes/"
    for root, dirs, files in os.walk(yourpath, topdown=False):
        logging.info('Entrando al directorio')
        for name in files:
            logging.info('Buscando archivos')
            if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
                logging.info('Buscando archivos .tif')
                if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".png"):
                    logging.info('Imagen %s ya existe' %name)
                else:
                    logging.info('Imagen a convertir')
                    outfile = os.path.splitext(os.path.join(root, name))[0] + ".png"
                    try:
                        im = Image.open(os.path.join(root, name))
                        im.thumbnail(im.size)
                        im.save(outfile, "png", quality=100)
                        logging.info('Imagen creada a PNG')
                        with open(outfile,'rb') as imagen_binaria:
                            datos_imagen=imagen_binaria.read()
                            logging.info('Imagen binarizada')
                        consulta_insert=f"INSERT INTO Images (img,nombre) VALUES(?,'%s')"%outfile.replace('imagenes/','')
                        with cnxn.cursor() as cursor:
                            cursor.execute(consulta_insert,datos_imagen)
                            cnxn.commit()
                            logging.info('Imagen en DB')
                    except Exception as e:
                        logging.info(e)