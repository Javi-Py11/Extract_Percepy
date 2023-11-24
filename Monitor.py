from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from Extract_Perceptron import filled
import threading
import time
import tkinter as tk
from tkinter import scrolledtext ,ttk
import logging
import os
import datetime

#?__________ Config. Logger __________#?
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class Monitor(FileSystemEventHandler):
    
    def __init__(self, log_widget):
        #?__________ Establecemos el metodo del componente visual __________#?
        self.log_widget = log_widget
    
    def on_created(self, event):
        #?__________ Extraemos el nombre del archivo en la ruta __________#?
        archivo = event.src_path
        #?__________ Cargamos la ruta en la variable __________#?
        ruta_archivo = os.path.join(archivo)
        #?__________ Verifica si es un archivo (no un directorio) 
        if os.path.isfile(ruta_archivo):
            #?__________ Obtiene la fecha de la última modificación del archivo #?__________
            fecha_modificacion = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
        #?__________  Formateamos la fecha __________#
        fecha_formateada = fecha_modificacion.strftime("%Y-%m-%d %H:%M")
        #?__________ Llamamos la funcion para la extraccion __________#?
        filled(archivo,fecha_formateada)
        #?__________ Movemos el archivo a la  ruta espec. __________#?
        shutil.move(archivo, "//192.168.24.37//resultados//Prueba")
        #?__________ Creamos msj para mostrar al usuario __________#?
        mensaje = str(archivo) + ' Creado'
        #?__________ Cargamos el msj con salto de linea __________#?
        self.log_widget.insert(tk.END, mensaje + "\n")
        #?__________ Establecemos hasta la parte final __________#?
        self.log_widget.see(tk.END)
        logging.info(mensaje)

class Hilo_Principal:
    
    def __init__(self, log_widget):
        self.detener = None  
        self.hilo = None
        self.log_widget = log_widget
    
    def ejecutar_hilo(self):
        #?__________  Crear un nuevo objeto de Event __________#?
        self.detener = threading.Event()  
          #?__________  Mientras el evento detener no sea verdadero se ejecuta __________#?
        while not self.detener.is_set():
            #?__________  Cargamos el metodo Observer __________#?
            self.observer = Observer()
            #?__________  Cargamos el metodo Monitor pasandole como parametro el componente visual __________#?
            self.mi_evento = Monitor(self.log_widget)
            #?__________  Config de evento observer __________#?
            self.observer.schedule(self.mi_evento, "//192.168.24.37//resultados/", recursive=False)
            #?__________  Iniciamos metodo __________#?
            self.observer.start()
            #?__________  Creamos msj para mostrar __________#?
            mensaje = "Servidor Run...."
            #?__________ Cargamos el msj con salto de linea __________#?
            self.log_widget.insert(tk.END, mensaje + "\n")
            #?__________ Establecemos hasta la parte final __________#?
            self.log_widget.see(tk.END)
            logging.info(mensaje)
            #?__________ Intervalo de espera __________#?
            time.sleep(2)
            #?__________ Detenemos el observer y esperamos a que se detenga __________#?
            self.observer.stop()
            self.observer.join()
            
    def iniciar(self):
        #?__________ Si el Hilo no se inicio ya y no esta activo  __________#?
        if self.hilo is None or not self.hilo.is_alive():
            #?__________ Config de hilo __________#?
            self.hilo = threading.Thread(target=self.ejecutar_hilo)
            self.hilo.start()
            
    def detener_hilo(self):
        #?__________ Si el metodo detener no esta en None __________#?
        if self.detener is not None:
            self.detener.set()
        #?__________ Si el metodo observer esta activo detenemos __________#?
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        #?__________ Si el hilo no esta en None y esta activo espero a que termine __________#?
        if self.hilo is not None and self.hilo.is_alive():
            self.hilo.join()

        mensaje = "Servidor Stop"
        self.log_widget.insert(tk.END, mensaje + "\n")
        self.log_widget.see(tk.END)
        logging.info(mensaje)

def iniciar_hilo():
    #?__________ Llamamos la funcion y deshabilitamos el boton presionado __________#?
    mi_hilo.iniciar()
    boton_iniciar["state"] = "disabled"
    boton_detener["state"] = "active"

def detener_hilo():
    #?__________ Llamamos la funcion y deshabilitamos el boton presionado __________#?
    mi_hilo.detener_hilo()
    boton_iniciar["state"] = "active"
    boton_detener["state"] = "disabled"

#?_______PENDIENTE AGREGAR FUNCIONAMIENTO _______?#
def selection_changed(event):
    selection=combo.get()
    print(selection)

#?__________ Crear la ventana de la interfaz gráfica__________#?
ventana = tk.Tk()
ventana.resizable(0,0)
ventana.title("Perceptron")
ventana.iconbitmap('ojo.ico')
#?__________ Crear botones de inicio y parada __________#?
titulo_txt=tk.Label(text='Linea',font='Arial')
titulo_txt.pack()
combo = ttk.Combobox(state='readonly',values=['Front Creadle'])
combo.bind("<<ComboboxSelected>>", selection_changed)
combo.pack()
#?__________ Crear botones de inicio y parada __________#?
boton_iniciar = tk.Button(ventana, text="Run Server", command=iniciar_hilo)
boton_iniciar.pack()
boton_detener = tk.Button(ventana, text="Stop Server", command=detener_hilo, state="disabled")
boton_detener.pack()
#?__________  Crear una ventana de registro __________#?
log_widget = scrolledtext.ScrolledText(ventana, state="normal")
log_widget.pack()
#?__________  Llama a la clase del hilo __________#?
mi_hilo = Hilo_Principal(log_widget)
#?__________  Iniciar el bucle principal de la interfaz gráfica __________#?
ventana.mainloop()
