#include "calculator.h"
#include <stdio.h>
#include <math.h>
#include <string.h>

// 简单的函数不需要错误参数
CALC_API int add(int a, int b) { return a + b; }

CALC_API int subtract(int a, int b) { return a - b; }

CALC_API int multiply(int a, int b) { return a * b; }

CALC_API double divide(int a, int b, CalcErrorCode* error) {
    if (error) *error = CALC_SUCCESS;  // 有点想flag的功能

    if (b == 0) {
        set_error("Division by zero: %d / %d", a, b);
        if (error) *error = CALC_ERROR_DIVISION_BY_ZERO;
        return 0.0;
    } 
    return (double)a / b; 
}

CALC_API int square(int x) { return x * x; }

CALC_API int cube(int x) {
    return x * x * x;
}

// sqrt_calc避免与内置函数sqrt重名
CALC_API double sqrt_calc(double x, CalcErrorCode* error) {
    if (error) *error = CALC_SUCCESS;

    // 使用输入验证函数
    if (!is_valid_number(x)) {
        set_error("Invalid number for sqrt: %f", x);
        if (error) *error = CALC_ERROR_INVALID_INPUT;
        return 0.0;
    }

    if (x < 0) {
        set_error("Square root of negative number: %f", x);
        if (error) *error = CALC_ERROR_NEGATIVE_SQRT;
        return 0.0;
    }

    // 牛顿迭代法计算平方根
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
CALC_API double power(double base, double exponent, CalcErrorCode* error) {
    // 1. 初始化错误码为成功
    if (error) *error = CALC_SUCCESS;

    // 2. 检查输入数字是否有效（不是NaN或无穷大）
    if (!is_valid_number(base) || !is_valid_number(exponent)) {
        set_error("无效的输入数字: base=%.2f, exponent=%.2f", base, exponent);
        if (error) *error = CALC_ERROR_INVALID_INPUT;
        return 0.0;
    }

    // 3. 任何数的0次方都是1
    if (exponent == 0.0) {
        return 1.0;
    }

    // 4. 处理底数为0的情况
    if (base == 0.0) {
        if (exponent > 0.0) {
            return 0.0;  // 0的正数次方是0
        } else if (exponent < 0.0) {
            set_error("0的负数次方未定义: 0^%.2f", exponent);
            if (error) *error = CALC_ERROR_INVALID_POWER;
            return 0.0;
        }
    }

    // 5. 1的任何次方都是1
    if (base == 1.0) {
        return 1.0;
    }

    // 6. 处理负数底数的情况
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
            set_error("负数底数的小数次方在实数范围内未定义: %.2f^%.2f", base, exponent);
            if (error) *error = CALC_ERROR_INVALID_POWER;
            return 0.0;
        }
    }

    // 7. 一般情况：使用数学库的pow函数
    return pow(base, exponent);
}
// 三角函数计算
CALC_API double trig_calc(double input, const char* angle_mode, const char* func,
                 CalcErrorCode* error) {
    if (error) *error = CALC_SUCCESS;

    // 使用输入验证函数，代码更简洁
    if (!is_valid_number(input)) {
        set_error("Invalid input number: %f", input);
        if (error) *error = CALC_ERROR_INVALID_INPUT;
        return 0.0;
    }

    if (!is_valid_angle_mode(angle_mode)) {
        set_error("Invalid angle mode: %s", angle_mode ? angle_mode : "NULL");
        if (error) *error = CALC_ERROR_INVALID_TRIG;
        return 0.0;
    }

    if (!is_valid_trig_function(func)) {
        set_error("Invalid trig function: %s", func ? func : "NULL");
        if (error) *error = CALC_ERROR_INVALID_TRIG;
        return 0.0;
    }


    // 三角函数计算逻辑
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

    return 0.0;
}
