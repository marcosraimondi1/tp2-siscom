import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import numpy as np
import ctypes
import time
import matplotlib.pyplot as plt

class Interfaz:
    def __init__(self, master):
        self.master = master
        master.title("TPN° 2 - Sistema de Computación")
        master.geometry("800x600")                              # Establecer el tamaño inicial de la ventana

        # Configurar imagen de fondo
        image = Image.open("fondo.png")
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear un frame para contener los widgets
        self.frame = ttk.Frame(master, style="Custom.TFrame")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Estilo para el frame
        style = ttk.Style()
        style.configure("Custom.TFrame", background="azure2")  

        # Título de la ventana 
        self.titulo = tk.Label(master, text="Las neuronas de bajo consumo", font=("Impact", 30, "bold"), bg="azure2")
        self.titulo.place(relx=0.5, rely=-0.5, anchor="center")  # Inicialmente fuera de la ventana

        # Animación del título
        self.animate_title()

        # Box de paises
        self.etiqueta_paises = ttk.Label(self.frame, text="Seleccione un país:", font=("Arial", 14))
        self.etiqueta_paises.grid(row=0, column=0, padx=(0, 10))

        # Combo box con los países
        self.paises = ["", "Argentina", "Canada", "Finland", "Austria", "Brasil", "Chile", "Colombia", "Peru", "Mexico", "Spain"]
        self.paises.sort()  # Ordenar alfabéticamente
        self.combo_paises = ttk.Combobox(self.frame, values=self.paises, font=("Arial", 14), state="normal")
        self.combo_paises.current(0)
        self.combo_paises.grid(row=0, column=1)

        # Botón para mostrar el gráfico con estilo diferente
        self.boton_mostrar = ttk.Button(self.frame, text="Mostrar Gráfico", command=self.mostrar_grafico, style="Accent.TButton", state="disabled")
        self.boton_mostrar.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        # Estilo para el botón
        style.configure("Accent.TButton", background="white", foreground="black", font=("Arial", 14, "bold"))

        # Vincular la función 'habilitar_boton' al evento '<<ComboboxSelected>>' del combo box
        self.combo_paises.bind("<<ComboboxSelected>>", self.habilitar_boton)

        # Vincular la función 'habilitar_boton' al evento '<KeyRelease>' del combo box
        self.combo_paises.bind("<KeyRelease>", self.filtrar_paises)

    def animate_title(self):
        time.sleep(0.1)
        for i in range(1, 18):                                      # Iterar sobre un rango de valores para simular la animación
            y_pos = 0.1 + 0.01 * i                                  # Incrementar la posición y
            self.titulo.place(relx=0.5, rely=y_pos, anchor="center")
            self.master.update()                                    # Actualizar la ventana
            time.sleep(0.03)                                        # Agregar un pequeño retraso para una animación más suave

    def get_data(self, country):
        API_URL = f"https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22{country}%22"
        response = requests.get(API_URL)
        if response.status_code != 200:
            print("Failed fetching data from API", response)
            exit()
        data = response.json()
        return data

    def filter_by_country(self, country_data, country):
        filtered = []
        for element in country_data:
            if element["country"]["value"].lower() == country.lower():
                filtered.append(element)
        return filtered

    def get_values(self, filtered_data):
        values = np.array([], dtype=np.float32)
        fechas = []
        for data in filtered_data:
            if data["value"] is not None:
                values = np.append(values, data["value"])
                fechas.append(data["date"])
        return values, fechas

    def mostrar_grafico(self):
        pais_seleccionado = self.combo_paises.get()
        if pais_seleccionado != "" and pais_seleccionado in self.paises:
            print("Se ha seleccionado el país:", pais_seleccionado)

            data = self.get_data(pais_seleccionado)

            filtered = self.filter_by_country(data[1], pais_seleccionado)

            values, fechas = self.get_values(filtered)

            #results = process_values(values)
            
            plt.figure()
            plt.plot(fechas[::-1], values[::-1], marker="x")
            plt.plot(fechas[::-1], values[::-1], marker="o")
            plt.grid()
            plt.title(f"{pais_seleccionado.upper()}'s Gene Index Evolution")
            plt.ylabel("gene index")
            plt.xlabel("years")
            plt.legend(["original", "procesado"])
            plt.savefig(f"./results/{pais_seleccionado}_gene_index.png")
            plt.show()

        else:
            print("Por favor, seleccione un país válido antes de mostrar el gráfico.")



    def habilitar_boton(self, event=None):
        if self.combo_paises.get() != "" and self.combo_paises.get() in self.paises:
            self.boton_mostrar.config(state="normal")
        else:
            self.boton_mostrar.config(state="disabled")

    def filtrar_paises(self, event=None):
        # Obtener el texto ingresado en el combo box
        texto = self.combo_paises.get().lower()

        # Filtrar los países que contienen el texto ingresado
        opciones_filtradas = [pais for pais in self.paises if pais.lower().startswith(texto)]

        # Mostrar las opciones filtradas en el combo box
        if opciones_filtradas:
            self.combo_paises["values"] = opciones_filtradas
            self.combo_paises.set(texto)                    # Restablecer el texto ingresado
            self.combo_paises.icursor(len(texto))           # Mover cursor al final del texto ingresado
            self.combo_paises.config(foreground="black")    # Restaurar color de texto
            self.habilitar_boton()                          # Habilitar o deshabilitar el botón según corresponda
            self.combo_paises.event_generate("<Down>")      # Desplega las opciones
        else:
            self.combo_paises.set(texto)
            opciones_filtradas.append("(país no encontrado)")
            self.combo_paises["values"] = opciones_filtradas
            self.combo_paises.event_generate("<Down>")
            self.combo_paises.icursor(len(texto))           # Mover cursor al final del texto ingresado
            self.combo_paises.config(foreground="gray")     # Cambiar color de texto a gris
            self.boton_mostrar.config(state="disabled")     # Deshabilitar botón

def process_values(values):

    # Cargar la biblioteca compartida
    libgini = ctypes.CDLL('./libgini_calc.so')

    # Definir los tipos de argumentos y el tipo de retorno de la función en C
    libgini.float_array_to_int_array.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    
    # Convertir la lista de Python a un arreglo de C
    data_array = (ctypes.c_float * len(values))(*values)

    output = np.zeros(len(values), dtype=np.int32)
    result_array = (ctypes.c_int * len(values))(*output)
    
    # Llamar a la función de C
    libgini.float_array_to_int_array(data_array, len(values), result_array)

    return np.fromiter(result_array, dtype=np.int32, count=len(values))

def main():
    ventana = tk.Tk()
    app = Interfaz(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
