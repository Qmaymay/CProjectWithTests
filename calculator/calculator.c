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

int cube(int x) {
    return x * x * x;
}

double sqrt(double x) {
    if (x < 0) {
        return -1.0; // 错误处理：负数没有实数平方根
    }
    return sqrt(x); // 使用 math.h 的 sqrt 函数
}