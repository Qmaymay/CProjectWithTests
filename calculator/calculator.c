#define CALCULATOR_EXPORTS
#include "calculator.h"
#include <stdio.h>

int add(int a, int b) { return a + b; }

int subtract(int a, int b) { return a - b; }

int multiply(int a, int b) { return a * b; }

double divide(int a, int b) { 
    if (b == 0) { 
        printf("Error: Division by zero!\n"); 
        return 0; 
    } 
    return (double)a / b; 
}

int square(int x) { return x * x; }
