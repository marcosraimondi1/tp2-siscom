#include <stdio.h>

// Función para calcular el índice GINI
float calculate_gini(float* data, int size) {
    float sum = 0;
    for (int i = 0; i < size; i++) {
        sum += data[i];
    }
    return sum / size;
}
