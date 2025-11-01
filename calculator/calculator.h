#ifndef CALCULATOR_H
#define CALCULATOR_H

#include "version.h"

const char* get_version(void);
// 最简单的函数声明（不要用 __declspec 等）
int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);
double divide(int a, int b);
int square(int x);
int cube(int x);
double sqrt(double x);
double power(double base, double exponent);  // 支持浮点指数



#endif