/*
 * TODO calculator_app 下点绿色三角 运行,
 * CLion 有两种运行模式：CMake 模式：通过 CMakeLists.txt，
 * 正确链接所有依单文件模式：快速测试单个文件，但无法处理复杂依赖
 * 与测试python代码共享动态库时，main.c 下点绿色三角只会编译main.c
 * */
#include "calculator.h"
#include <stdio.h>


int main() {
    printf("Simple Calculator\n");
    printf("================\n");

    int a = 20, b = 10;

    printf("Basic Operations:\n");
    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d - %d = %d\n", a, b, subtract(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    printf("%d / %d = %.2f\n", a, b, divide(a, b));
    printf("%d ^ 2 = %d\n", a, square(a));
    printf("%d ^ 3 = %d\n", a, cube(a));
    printf("sqrt(%.2f) = %.2f\n", (double)a, sqrt((double)a));
    printf("%d ^ %d = %.2f\n", a, b, power(a,b));

    printf("\nTrigonometric Functions Test\n");
    printf("============================\n");

    // 角度制计算
    double degrees_sin = trig_calc(30.0, "degrees", "sin");
    printf("sin(30 degrees) = %.6f\n", degrees_sin);

    double degrees_cos = trig_calc(45.0, "degrees", "cos");
    printf("cos(45 degrees) = %.6f\n", degrees_cos);

    double degrees_tan = trig_calc(60.0, "degrees", "tan");
    printf("tan(60 degrees) = %.6f\n", degrees_tan);

    // 弧度制计算
    double radians_sin = trig_calc(1.047, "radians", "sin");
    printf("sin(1.047 radians) = %.6f\n", radians_sin);

    double radians_cos = trig_calc(0.785, "radians", "cos");
    printf("cos(0.785 radians) = %.6f\n", radians_cos);

    double radians_tan = trig_calc(1.047, "radians", "tan");
    printf("tan(1.047 radians) = %.6f\n", radians_tan);

    // 反三角函数
    double degrees_asin = trig_calc(0.5, "degrees", "asin");
    printf("asin(0.5) = %.6f degrees\n", degrees_asin);

    double degrees_acos = trig_calc(0.5, "degrees", "acos");
    printf("acos(0.5) = %.6f degrees\n", degrees_acos);

    double degrees_atan = trig_calc(1.0, "degrees", "atan");
    printf("atan(1.0) = %.6f degrees\n", degrees_atan);

    // 转换函数
    double to_radians_result = trig_calc(180.0, "degrees", "to_radians");
    printf("180 degrees = %.6f radians\n", to_radians_result);

    double to_degrees_result = trig_calc(3.14159, "radians", "to_degrees");
    printf("3.14159 radians = %.6f degrees\n", to_degrees_result);

    return 0;
}

