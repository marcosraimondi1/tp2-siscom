// Función para calcular el promedio índice GINI
#include <stdlib.h>
float calculate_gini(float *data, int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += data[i];
  }
  return sum / size;
}

void float_array_to_int_array(float *data, int size, int *result) {
  int *new_array = malloc(sizeof(int) * size);
  for (int i = 0; i < size; i++) {
    result[i] = (int)(data[i] + 1);
  }
}
