/*
 * TODO calculator_app 下点绿色三角 运行,
 * CLion 有两种运行模式：CMake 模式：通过 CMakeLists.txt，
 * 正确链接所有依单文件模式：快速测试单个文件，但无法处理复杂依赖
 * 与测试python代码共享动态库时，main.c 下点绿色三角只会编译main.c
 * */

#include <stdio.h>
#include "calculator.h"  // 只需要包含这个，会自动包含 error_handling.h

// 测试基本运算
void test_basic_operations(void) {
    printf("=== 基本运算测试 ===\n");

    // 不需要错误检查的简单运算
    printf("5 + 3 = %d\n", add(5, 3));
    printf("10 - 4 = %d\n", subtract(10, 4));

    // 需要错误检查的运算
    CalcErrorCode error;

    // 正常除法
    double result = divide(10, 2, &error);
    if (error == CALC_SUCCESS) {
        printf("10 / 2 = %.2f\n", result);
    } else {
        printf("除法错误: %s\n", get_last_error());
    }

    // 除零错误
    result = divide(10, 0, &error);
    if (error != CALC_SUCCESS) {
        printf("检测到除零错误: %s (错误码: %d)\n",
               get_last_error(), error);
        printf("错误描述: %s\n", error_code_to_string(error));
    }
}

// 测试高级运算
void test_advanced_operations(void) {
    printf("\n=== 高级运算测试 ===\n");

    CalcErrorCode error;

    // 平方根测试
    double sqrt_result = sqrt_calc(25.0, &error);
    if (error == CALC_SUCCESS) {
        printf("√25 = %.2f\n", sqrt_result);
    }

    // 负数平方根测试
    sqrt_result = sqrt_calc(-4.0, &error);
    if (error != CALC_SUCCESS) {
        printf("平方根错误: %s\n", error_code_to_string(error));
    }

}

// 幂运算测试
void test_power_function(void) {
    printf("\n=== 幂运算测试 ===\n");

    CalcErrorCode error;

    // 测试1: 正常情况
    double power_result = power(2.0, 3.0, &error);
    if (error == CALC_SUCCESS) {
        printf("2^3 = %.2f\n", power_result);
    } else {
        printf("计算失败: %s\n", get_last_error());
    }

    // 测试2: 0的负数次方（应该报错）
    power_result = power(0.0, -2.0, &error);
    if (error != CALC_SUCCESS) {
        printf("检测到错误: %s (错误码: %d)\n",
               get_last_error(), error);
        printf("错误描述: %s\n", error_code_to_string(error));
    }

    // 测试3: 负数底数的小数次方（应该报错）
    power_result = power(-4.0, 0.5, &error);
    if (error != CALC_SUCCESS) {
        printf("检测到错误: %s\n", error_code_to_string(error));
    }

    // 测试4: 无效输入（NaN）
//    double invalid_num = 0.0 / 0.0;  // 制造 NaN
//    power_result = power(invalid_num, 2.0, &error);
    double result = divide(10.0, 0.0, &error);  // 这个应该没问题
    if (error != CALC_SUCCESS) {
        (void )result;
        printf("无效输入检测: %s\n", get_last_error());
    }
}

// 测试三角函数
void test_trig_functions(void) {
    printf("\n=== 三角函数测试 ===\n");

    CalcErrorCode error;

    // 正常三角函数计算
    double sin_result = trig_calc(30.0, "degrees", "sin", &error);
    if (error == CALC_SUCCESS) {
        printf("sin(30°) = %.2f\n", sin_result);
    }

    // 无效角度模式测试
    double invalid_result = trig_calc(30.0, "invalid_mode", "sin", &error);
    if (error != CALC_SUCCESS) {
        (void)invalid_result;  // 明确表示故意不使用这个变量
        printf("三角函数错误: %s\n", get_last_error());

    }

    // 无效函数名测试
    invalid_result = trig_calc(30.0, "degrees", "invalid_func", &error);
    if (error != CALC_SUCCESS) {
        (void)invalid_result;
        printf("函数名错误: %s\n", error_code_to_string(error));
    }
}

// 直接使用验证函数
void test_validation_functions(void) {
    printf("\n=== 输入验证测试 ===\n");

    // 直接使用验证函数（不需要通过计算器）
    printf("验证数字 3.14: %s\n", is_valid_number(3.14) ? "有效" : "无效");
    printf("验证角度模式 'degrees': %s\n",
           is_valid_angle_mode("degrees") ? "有效" : "无效");
    printf("验证函数名 'tan': %s\n",
           is_valid_trig_function("tan") ? "有效" : "无效");

    // 测试无效输入
    double invalid_num = 0.0 / 0.0;  // 制造 NaN
    printf("验证 NaN 数字: %s\n", is_valid_number(invalid_num) ? "有效" : "无效");
}

int main(void) {
    printf("计算器测试程序\n");
//    printf("版本: %s\n\n", get_version());

    test_basic_operations();
    test_advanced_operations();
    test_trig_functions();
    test_validation_functions();

    return 0;
}




//#include "calculator.h"
//#include <stdio.h>
//
//int main() {
//    printf("Simple Calculator\n");
//    printf("================\n");
//
//    int a = 20, b = 10;
//
//    printf("Basic Operations:\n");
//    printf("%d + %d = %d\n", a, b, add(a, b));
//    printf("%d - %d = %d\n", a, b, subtract(a, b));
//    printf("%d * %d = %d\n", a, b, multiply(a, b));
//    printf("%d / %d = %.2f\n", a, b, divide(a, b));
//    printf("%d ^ 2 = %d\n", a, square(a));
//    printf("%d ^ 3 = %d\n", a, cube(a));
//    printf("sqrt(%.2f) = %.2f\n", (double)a, sqrt((double)a));
//    printf("%d ^ %d = %.2f\n", a, b, power(a,b));
//
//    printf("\nTrigonometric Functions Test\n");
//    printf("============================\n");
//
//    // 角度制计算
//    double degrees_sin = trig_calc(30.0, "degrees", "sin");
//    printf("sin(30 degrees) = %.6f\n", degrees_sin);
//
//    double degrees_cos = trig_calc(45.0, "degrees", "cos");
//    printf("cos(45 degrees) = %.6f\n", degrees_cos);
//
//    double degrees_tan = trig_calc(60.0, "degrees", "tan");
//    printf("tan(60 degrees) = %.6f\n", degrees_tan);
//
//    // 弧度制计算
//    double radians_sin = trig_calc(1.047, "radians", "sin");
//    printf("sin(1.047 radians) = %.6f\n", radians_sin);
//
//    double radians_cos = trig_calc(0.785, "radians", "cos");
//    printf("cos(0.785 radians) = %.6f\n", radians_cos);
//
//    double radians_tan = trig_calc(1.047, "radians", "tan");
//    printf("tan(1.047 radians) = %.6f\n", radians_tan);
//
//    // 反三角函数
//    double degrees_asin = trig_calc(0.5, "degrees", "asin");
//    printf("asin(0.5) = %.6f degrees\n", degrees_asin);
//
//    double degrees_acos = trig_calc(0.5, "degrees", "acos");
//    printf("acos(0.5) = %.6f degrees\n", degrees_acos);
//
//    double degrees_atan = trig_calc(1.0, "degrees", "atan");
//    printf("atan(1.0) = %.6f degrees\n", degrees_atan);
//
//    // 转换函数
//    double to_radians_result = trig_calc(180.0, "degrees", "to_radians");
//    printf("180 degrees = %.6f radians\n", to_radians_result);
//
//    double to_degrees_result = trig_calc(3.14159, "radians", "to_degrees");
//    printf("3.14159 radians = %.6f degrees\n", to_degrees_result);
//
//    return 0;
//}
//
