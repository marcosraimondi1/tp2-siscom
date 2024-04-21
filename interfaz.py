import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
from server import get_values_and_dates, process_values, get_data, filter_by_country

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

    def mostrar_grafico(self):
        pais_seleccionado = self.combo_paises.get()
        if pais_seleccionado != "" and pais_seleccionado in self.paises:
            print("Se ha seleccionado el país:", pais_seleccionado)

            # procesar peticion
            data = get_data()
            filtered = filter_by_country(data[1], pais_seleccionado)
            values, fechas = get_values_and_dates(filtered)
            results = process_values(values)
            
            # mostrar resultados
            plt.figure()
            plt.plot(fechas[::-1], values[::-1], marker="x")
            plt.plot(fechas[::-1], results[::-1], marker="o")
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

