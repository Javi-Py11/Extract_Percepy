import logging
from zipfile import ZipFile 
import os
import datetime
import glob
import convert as convertir
from shutil import rmtree

def extract(mod_date):
    #?__________ Declaramos ruta de carpeta compartida __________#
    carpeta = r"//192.168.24.37//scanningdata"
    patron="*.txt"
    #?__________ Iteramos para ir archivo por archivo  __________#
    for archivo in os.listdir(carpeta):
        #?__________ Extreamos la ruta especifica del archivo __________#
        ruta_archivo = os.path.join(carpeta, archivo)
        #?__________  Verifica si es un archivo (no un directorio) __________#
        if os.path.isfile(ruta_archivo):
            #?__________Obtiene la fecha de la última modificación del archivo __________#
            fecha_modificacion = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
            #?__________  Formateamos la fecha para poder compararla con el primer archivo __________#
            fecha_formateada = fecha_modificacion.strftime("%Y-%m-%d %H:%M")
            #?__________ Nombramos la carpeta donde se almacenaran los archivos __________#?
            img_directory = 'imagenes/'
            #?__________ Creamos la carpeta onde almacenaremos las imagenes __________#?
            if not os.path.exists(img_directory):
                logging.info('Creando directorio para almacenar imagenes')
                os.makedirs(img_directory)
            text_arch=len(archivo)
            #?__________ Si es igual la fecha del archivo entra __________#
            if fecha_formateada ==mod_date and text_arch >33:
                logging.info('Archivo encontrado')
                try:
                    #?__________ Entramos al archivo Zip __________#
                    with ZipFile(carpeta+'//'+archivo,'r') as zObject:                
                        #?__________ Extraemos todos los archivos __________#
                        zObject.extractall(path=img_directory)
                        logging.info('Extrayendo archivos de zip')
                    zObject.close()
                except:
                    #?__________ Exception __________#
                    logging.info('Error al extraer los archivos de %s'%archivo)
                #?__________ Buscamos archivos con el patron especifico __________#
                imag=glob.glob(os.path.join(img_directory,patron))
                #?__________ Iteramos para retirar archivos excepto imagenes __________#
                for i in range(len(imag)):
                    os.remove(imag[i])             
            else:
                continue                         
    logging.info('Extraccion terminada')
    logging.info('Convirtiendo imagenes')
    convertir.img_to_png()
    logging.info('Imagenes en DB terminada')
    rmtree(img_directory)
    logging.info('Carpeta eliminada')