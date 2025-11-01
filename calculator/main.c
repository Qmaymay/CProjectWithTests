/*
 * TODO calculator_app 下点绿色三角 运行,
 * CLion 有两种运行模式：CMake 模式：通过 CMakeLists.txt，
 * 正确链接所有依单文件模式：快速测试单个文件，但无法处理复杂依赖
 * 与测试python代码共享动态库时，main.c 下点绿色三角只会编译main.c
 * */
#include "calculator.h"
#include "version.h"
#include <stdio.h>


int main() {
    printf("Calculator Version:\n");
    printf("简单计算器\n");
    printf("==========\n");
    int a = 20, b = 10;

    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d - %d = %d\n", a, b, subtract(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    printf("%d / %d = %.2f\n", a, b, divide(a, b));
    printf("%d ^ 2 = %d\n", a, square(a));
    printf("%d ^ 3 "
           "= %d\n", a, cube(a));
    printf("%.2f ^ 2 = %.2f\n", (double)a, sqrt((double)a));
    printf("%d ^ %d = %.2f\n", a, b, power(a,b));

    return 0;
}