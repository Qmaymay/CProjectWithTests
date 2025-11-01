#include "calculator.h"
#include <stdio.h>
#include <math.h>
#include <string.h>

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


/**
 * 幂运算函数 - 支持浮点指数的健壮实现
 * @param base 底数
 * @param exponent 指数
 * @return base^exponent 的结果
 *
 * 特性：
 * ✅ 支持正负小数指数
 * ✅ 处理负数底数的合理情况
 * ✅ 完善的错误处理和边界情况
 * ✅ 使用数学库优化性能
 */
double power(double base, double exponent) {
    // 特殊情况快速处理
    if (exponent == 0.0) {
        return 1.0;  // 任何数的0次方都是1
    }

    if (base == 0.0) {
        if (exponent > 0.0) {
            return 0.0;  // 0的正数次方是0
        } else if (exponent < 0.0) {
            printf("Error: Zero to a negative power is undefined!\n");
            return 0.0;  // 0的负数次方未定义
        }
    }

    if (base == 1.0) {
        return 1.0;  // 1的任何次方都是1
    }

    // 处理负数底数的情况
    if (base < 0.0) {
        // 检查指数是否为整数（允许负底数的整数次方）
        double int_part;
        if (modf(exponent, &int_part) == 0.0) {
            // 指数是整数，可以计算负底数的幂
            double result = pow(-base, exponent);  // 先算正数的幂
            // 如果指数是奇数，结果为负
            if (fmod(exponent, 2.0) != 0.0) {
                return -result;
            }
            return result;
        } else {
            // 负底数的小数次方在实数范围内未定义
            printf("Error: Negative base with fractional exponent is undefined in real numbers!\n");
            return 0.0;
        }
    }

    // 一般情况：使用数学库的pow函数（经过优化）
    return pow(base, exponent);
}

// 三角函数计算
double trig_calc(double input, const char* angle_mode, const char* func) {
    int is_degrees = (strcmp(angle_mode, "degrees") == 0);

    double radians = input;
    if (is_degrees) {
        radians = input * 3.141592653589793 / 180.0;
    }

    if (strcmp(func, "sin") == 0) return sin(radians);
    if (strcmp(func, "cos") == 0) return cos(radians);
    if (strcmp(func, "tan") == 0) return tan(radians);

    // 修复反三角函数的错误处理
    if (strcmp(func, "asin") == 0) {
        if (input < -1.0 || input > 1.0) return 0.0;  // 错误处理
        return asin(input) * (is_degrees ? 57.295779513 : 1.0);
    }
    if (strcmp(func, "acos") == 0) {
        if (input < -1.0 || input > 1.0) return 0.0;  // 错误处理
        return acos(input) * (is_degrees ? 57.295779513 : 1.0);
    }
    if (strcmp(func, "atan") == 0) return atan(input) * (is_degrees ? 57.295779513 : 1.0);
    if (strcmp(func, "to_radians") == 0) return is_degrees ? radians : input;
    if (strcmp(func, "to_degrees") == 0) return is_degrees ? input : input * 57.295779513;

    return 0.0;g
}
