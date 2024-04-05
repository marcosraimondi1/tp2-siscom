# TP1
## Enunciado y condiciones de aprobación

Para aprobar el TP#1 se debe diseñar e implementar una interfaz que muestre el índice GINI. La capa superior recuperará la información del banco mundial https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22. Se recomienda el uso de API Rest y Python. Los datos de consulta realizados deben ser entregados a un programa en C (capa intermedia) que convocará rutinas en ensamblador para que hagan los cálculos de conversión de float a enteros y devuelva el índice de un país como Argentina u otro sumando uno (+1). Luego el programa en C o python mostrará los datos obtenidos.-

Se debe utilizar el stack para convocar, enviar parámetros y devolver resultados. O sea utilizar las convenciones de llamadas de lenguajes de alto nivel a bajo nivel.- 

En una primera iteración resolverán todo el trabajo práctico usando c con python sin ensamblador. En la siguiente iteración usarán los conocimientos de ensamblador para completar el tp.

**IMPORTANTE**: en esta segunda iteración deberan mostrar los resultados con gdb, para ello pueden usar un programa de C puro. Cuando depuren muestran el estado del área de memoria que contiene el stack antes, durante y después de la función. 

Casos de prueba, diagramas de bloques, diagrama de secuencia, pruebas de performance para comparar c y python son bienvenidos, profiling de la app de c es un plus.

# Implemetación

## Compilación codigo C para crear biblioteca compartida

- gcc -shared -W -o libgini_calc.so gini_calc.c

## Ejecutar codigo en Python con librerias en C
- python server.py
- python3 server.py

# Resultados primera parte
![image](./gene.png)



