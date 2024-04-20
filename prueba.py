import ctypes
import numpy as np
import requests

def run_server():

    values = [1.5, 2.75, 3.9]

    values_results = np.zeros(3, dtype=np.int32)

    # Cargar la biblioteca compartida
    libgini = ctypes.CDLL('./libgini_calc.so')

    # Definir los tipos de argumentos y el tipo de retorno de la función en C
    libgini.float_array_to_int_array.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    
    # Convertir la lista de Python a un arreglo de C

    data_array = (ctypes.c_float * len(values))(*values)

    result_array = (ctypes.c_int * len(values))(*values_results)
    
    # Llamar a la función de C
    libgini.float_array_to_int_array(data_array, len(values), result_array)

    # Convertir el array de C a una lista de Python para imprimirlo de forma legible
    result_list = list(result_array)
    print(result_list)


if __name__ == "__main__":
    run_server()
   
