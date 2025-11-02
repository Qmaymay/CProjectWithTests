//
// Created by Admin on 2025/11/2.
//

#ifndef CALCULATORPROJECT_ERROR_HANDLING_H
#define CALCULATORPROJECT_ERROR_HANDLING_H

#include <stdbool.h>

// 错误码定义
typedef enum {
    CALC_SUCCESS = 0,
    CALC_ERROR_DIVISION_BY_ZERO = -1,
    CALC_ERROR_NEGATIVE_SQRT = -2,
    CALC_ERROR_INVALID_POWER = -3,
    CALC_ERROR_INVALID_TRIG = -4,
    CALC_ERROR_INVALID_INPUT = -5,
    CALC_ERROR_TANGENT_UNDEFINED = -6
} CalcErrorCode;

// 错误处理函数
void set_error(const char* format, ...);
const char* get_last_error(void);
void clear_error(void);
const char* error_code_to_string(CalcErrorCode code);

// 输入验证函数
bool is_valid_number(double x);
bool is_valid_angle_mode(const char* mode);
bool is_valid_trig_function(const char* func);
bool is_in_range(double x, double min, double max);

#endif // CALCULATORPROJECT_ERROR_HANDLING_H
