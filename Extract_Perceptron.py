import pandas as pd
import logging
from Classe  import db_conection
from Extract_Perceptron_Img import extract
import xmltodict
import os

def filled(path,fecha):
    #?__________ Declaramos variables __________#
    lista_medidas=[]
    lista_limites=[]
    nombre=[]
    Punto=[]
    #?__________ Creamos la instancia a la funcion DB __________#?
    db=db_conection()
    #?__________ Creamos la conexion a la DB __________#?
    db.conexion() 
    #?__________ Leemos el archivo xml __________#?
    with open(path,'r') as xml_archivo:
        data_dict=xmltodict.parse(xml_archivo.read())
        logging.info('Extrayendo archivo....')
    #?__________ Convertimos a DataFrame __________#?
    df=pd.DataFrame.from_dict(data_dict)
    #?__________ Extraemos del DF el PSN de la lectura __________#?
    PSN=df['dot']['cycle']['partid'][1]['value']
    #?__________ Creamos un DF apartir de una columna __________#?
    inspections=pd.DataFrame(df['dot']['inspectionpoint'])       
    #?__________ Iteramos para extraer caracteristicas del DF __________#?
    for j in range(len(inspections)):
        for k in range(len(inspections['characteristic'][j])):
            #?__________ Almacenamos cada una en listas __________#?
            try:
                nombre.append(inspections['characteristic'][j][k]['aliasname'])
            except KeyError:
                nombre.append(inspections['characteristic'][j]['aliasname'])
            try:
                Punto.append(inspections['name'][j])
                lista_medidas.append(inspections['characteristic'][j][k]['measurement'])
            except KeyError:
                lista_medidas.append(inspections['characteristic'][j]['measurement'])
            try:
                #?__________ Llenamos el diccionario para los limites __________#?
                dic_lista=inspections['characteristic'][j][k]['limit'][1]
                #?__________ Agregamos columna con el nombre correjido __________#?
                dic_lista['type']=dic_lista['@type']
                #?__________ Eliminamos la columna que no nos sirve __________#?
                del dic_lista['@type']
                #?__________ agregamos el diccionario a la lista __________#?
                lista_limites.append(dic_lista)
            #?__________ si tiene error, rellena con vacio __________#?    
            except KeyError:
                lista_limites.append({'upper': '0', 'lower': '0', 'type': 'Na'})    
    logging.info('Archivo estructurandose....')
    #?__________ Creamos un DF con una de las listas __________#?
    list_df_medidas=pd.DataFrame(lista_medidas)
    #?__________ Insertamos la lista de nombres como columna __________#?
    list_df_medidas.insert(0, "Feature", nombre, allow_duplicates=False)
    #?__________ Creamos un DF con la lista restante __________#?
    list_df_limites=pd.DataFrame(lista_limites)
    #?__________ Concatenamos los dos DF __________#?
    DF_final=pd.concat([list_df_medidas,list_df_limites], axis=1)    
    #?__________ Insertamos la lista Punto como columna __________#?
    DF_final.insert(0,'Punto',Punto,allow_duplicates=False)
    #?__________ Insertamos la lista PSN como columna __________#?
    DF_final.insert(0,'PSN',PSN,allow_duplicates=False)
    #?__________ Renombramos columnas __________#?
    DF_final.rename(columns={'deviation':'Desviation','nominal':'Nominal','absolute':'Absolut','type':'Type_lim','type':'Type_lim',
                                    'lower':'LO_TOL','upper':'HI_TOL'},inplace=True)
    #?__________ Establecemos el nombre de columnas __________#?
    DF_final.columns
    #?__________ Establecemos el orden de columnas __________#?
    DF_final = DF_final.reindex(columns=['PSN','Punto','Feature','Desviation','Nominal','Absolut','Type_lim','LO_TOL','HI_TOL'])
    logging.info('Resultado....'+DF_final)
    #?__________ Subimos los datos a la DB __________#?
    DF_final.to_sql('Part_Data_Perceptron_FC', db.engine, if_exists='append',index=False)
    #?__________ Nombramos la carpeta donde se almacenaran los archivos __________#?
    #csv_directory = 'archivos_csv/'
    #nombre_arch=path[28:].replace('.xml','')
    #?__________ Creamos la carpeta onde almacenaremos los archivos csv __________#?
    #if not os.path.exists(csv_directory):
    #    logging.info('Creando directorio para almacenar archivos CSV')
    #    os.makedirs(csv_directory)
    #?__________ Creamos el nombre del archivo __________#?
    #nom_h = f'Perceptron_%s.csv' % nombre_arch
    #?__________ insertamos la informacion en le archivo __________#?
    #csv_file = os.path.join(csv_directory, nom_h)
    #logging.info('Creando archivo CSV')
   #?__________ Lo generamos en el csv con pandas __________#?
    #DF_final.to_csv(csv_file, index=True)
    #logging.info('Datos en CSV')
    #?_____________Cerramos la conexion a la DB y el motor_____________?#
    db.engine.dispose()
    extract(fecha)