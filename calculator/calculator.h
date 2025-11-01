#ifndef CALCULATOR_H
#define CALCULATOR_H



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
// 函数声明 - 3个参数，明确无歧义
double trig_calc(double input, const char* angle_mode, const char* func);




#endif