//
// Created by Admin on 2025/11/1.
//

#ifndef VERSION_H
#define VERSION_H

// 自动版本号 - 重新开始
#define CALC_MAJOR_VERSION 1
#define CALC_MINOR_VERSION 11
#define CALC_PATCH_VERSION 6
#define CALC_VERSION "1.11.0"

static inline const char* get_version(void) {
    return CALC_VERSION;
}

#endif