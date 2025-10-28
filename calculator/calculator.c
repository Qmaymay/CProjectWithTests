#define CALCULATOR_EXPORTS
#include "calculator.h"
#include <stdio.h>
#include <math.h>

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

int cube(int x) {
    return x * x * x;
}

int cube(int x) {
    return x * x * x;
}

double sqrt(double x) {
    if (x < 0) {
        return -1.0; // 错误处理
    }
    if (x == 0.0) {
        return 0.0;
    }

    // 牛顿迭代法
    double result = x;
    for (int i = 0; i < 20; i++) {
        result = 0.5 * (result + x / result);
    }
    return result;
}