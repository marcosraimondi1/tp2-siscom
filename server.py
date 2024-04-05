import ctypes
import numpy as np
import requests
import matplotlib.pyplot as plt


API_URL = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

def run_server():

    data = get_data()

    filtered = filter_country(data[1])

    values,fechas = get_values(filtered)   # Lista de flotantes 
    values_int = [1 for x in values]

    # Cargar la biblioteca compartida
    libgini = ctypes.CDLL('./libgini_calc.so')

    # Definir los tipos de argumentos y el tipo de retorno de la función en C
    libgini.float_array_to_int_array.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    
    # Convertir la lista de Python a un arreglo de C
    data_array = (ctypes.c_float * len(values))(*values)

    result_array = (ctypes.c_int * len(values))(*values_int)
    
    # Llamar a la función de C
    libgini.float_array_to_int_array(data_array, len(values), result_array)

    results = np.fromiter(result_array, dtype=np.int32, count=len(values))

    graficar(results[::-1],fechas[::-1])

def graficar(dataY, dataX):
    plt.plot(dataX, dataY, marker="o")
    plt.grid()
    plt.ylabel("gene index")
    plt.xlabel("years")
    plt.title("Argentina Gene Index Evolution")
    plt.savefig("gene.png")

    


def get_data():
    response = requests.get(API_URL)

    if response.status_code != 200:
        print("Failed fetching data from API", response)

    data = response.json()

    return data

def filter_country(country_data):
    filtered = []
    for elemento in country_data:
        if elemento["country"]["value"] == "Argentina":
            filtered.append(elemento)

    return filtered

def get_values(filtered_data):
    values = np.array([],dtype = np.float32)
    fechas = []
    for data in filtered_data:
        if data["value"] is not None:
            values = np.append(values, data["value"])
            fechas.append(data["date"])
    return (values, fechas)


if __name__ == "__main__":
    run_server()
   
