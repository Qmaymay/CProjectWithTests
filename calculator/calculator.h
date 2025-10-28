#ifndef CALCULATOR_H
#define CALCULATOR_H

// 添加 Windows DLL 导出宏
#ifdef _WIN32
#ifdef CALCULATOR_EXPORTS
#define CALCULATOR_API __declspec(dllexport)
#else
#define CALCULATOR_API __declspec(dllimport)
#endif
#else
#define CALCULATOR_API
#endif


CALCULATOR_API int add(int a, int b);
CALCULATOR_API int subtract(int a, int b);
CALCULATOR_API int multiply(int a, int b);
CALCULATOR_API double divide(int a, int b);
CALCULATOR_API int square(int x);

// 新函数
int cube(int x);
double sqrt(double x);


#endif
