/**
 * @file gini_calc.c
 * @brief funcion para calcular el promedio del indice GINI
 * 
 * @param data indices Gini sin procesar
 * @param size cantidad de indices enviados
 * 
 * @return promedio de indices gini pasados
 */
#include <stdlib.h>
float calculate_gini(float *data, int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += data[i];
  }
  return sum / size;
}

/**
 * @brief funcion para castear a entero y sumarle uno a los indices Gini
 * 
 * @param data indices Gini sin procesar
 * @param size cantidad de indices enviados
 * @param result indices casteados e incrementados en una unidad
 */
void float_array_to_int_array(float *data, int size, int *result) {
  int *new_array = malloc(sizeof(int) * size);
  for (int i = 0; i < size; i++) {
    result[i] = (int)(data[i] + 1);
  }
}
