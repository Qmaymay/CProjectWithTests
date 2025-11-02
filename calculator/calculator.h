#ifndef CALCULATOR_H
#define CALCULATOR_H

#include "error_handling.h"  // 包含错误处理头文件

// 版本信息
//const char* get_version(void);
//const char* get_last_error(void);

// 基本运算
int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);
double divide(int a, int b, CalcErrorCode* error);

// 高级运算
int square(int x);
int cube(int x);
double sqrt_calc(double x, CalcErrorCode* error);
double power(double base, double exponent, CalcErrorCode* error);


// 三角运算
double trig_calc(double input, const char* angle_mode, const char* func,
                 CalcErrorCode* error);

#endif
