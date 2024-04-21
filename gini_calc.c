#include <assert.h>
#include <stdio.h>

/**
 * @brief Convierte a entero el input y lo suma en uno
 * Funcion Implementada en assembler "./sum_array.asm"
 *
 * @param input array de flotantes
 * @param size tamano de array input y output
 * @param output array de enteros de resultado
 * */
extern void _sum_array(float *input, int size, int *output);

/**
 * @brief funcion para castear a entero y sumarle uno a los indices Gini
 *
 * @param data indices Gini sin procesar
 * @param size cantidad de indices enviados
 * @param result indices casteados e incrementados en una unidad
 */
void float_array_to_int_array(float *data, int size, int *result) {
  _sum_array(data, size, result);
}

// para testing
int main(int argc, char *argv[]) {
  float input[3] = {12.2, 5.45, 12.8};
  int output[3] = {0, 0, 0};
  int expected[3] = {13, 6, 14};

  _sum_array(input, 3, output);

  for (int i = 0; i < 3; i++) {
    printf("in %f, out %i, exp %i\n", input[i], output[i], expected[i]);
    assert(output[i] == expected[i]);
  }

  return 0;
}
