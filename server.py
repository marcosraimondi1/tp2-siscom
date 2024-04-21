import ctypes
import numpy as np
import requests
import matplotlib.pyplot as plt


API_URL = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

def run_server():

    data = get_data()
    country = input("Enter country: ")
    
    filtered = filter_by_country(data[1], country)

    values,fechas = get_values_and_dates(filtered)   # Lista de flotantes 

    results = process_values(values)

    plt.figure()
    plt.plot(fechas[::-1], values[::-1], marker="x")
    plt.plot(fechas[::-1], results[::-1], marker="o")
    plt.grid()
    plt.title(f"{country.upper()}'s Gene Index Evolution")
    plt.ylabel("gene index")
    plt.xlabel("years")
    plt.legend(["original", "procesado"])
    plt.savefig(f"./results/{country}_gene_index.png")

    
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

def get_data():
    response = requests.get(API_URL)

    if response.status_code != 200:
        print("Failed fetching data from API", response)
        return [] 

    data = response.json()

    return data

def filter_by_country(country_data, country):
    filtered = []
    for elemento in country_data:
        if elemento["country"]["value"].lower() == country.lower():
            filtered.append(elemento)

    return filtered

def get_values_and_dates(filtered_data):
    values = np.array([],dtype = np.float32)
    fechas = []
    for data in filtered_data:
        if data["value"] is not None:
            values = np.append(values, data["value"])
            fechas.append(data["date"])
    return (values, fechas)


if __name__ == "__main__":
    run_server()
   
