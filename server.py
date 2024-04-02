import ctypes
import numpy as np
import requests


API_URL = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

def run_server():

    data = get_data()

    total = data[0]["total"]

    filtered = filter_country(data[1])

    values = get_values(filtered)   # Lista de flotantes 

    print(values[3])

    # Cargar la biblioteca compartida
    libgini = ctypes.CDLL('./libgini_calc.so')

    # Definir los tipos de argumentos y el tipo de retorno de la función en C
    libgini.calculate_gini.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int]
    libgini.calculate_gini.restype = ctypes.c_float
    
    # Convertir la lista de Python a un arreglo de C
    data_array = (ctypes.c_float * len(values))(*values)
    
    # Llamar a la función de C
    result = libgini.calculate_gini(data_array, len(data))

    print("El índice GINI calculado es:", result)



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
    for data in filtered_data:
        if data["value"] is not None:
            values = np.append(values, data["value"])
    return values


if __name__ == "__main__":
    run_server()
   
