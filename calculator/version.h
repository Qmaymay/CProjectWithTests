//
// Created by Admin on 2025/10/31.
//

// calculator/version.h
#ifndef VERSION_H
#define VERSION_H

// 手动维护版本号 - 有重大更新时才改
#define CALC_MAJOR_VERSION 1
#define CALC_MINOR_VERSION 9
#define CALC_PATCH_VERSION 0
#define CALC_VERSION "1.9.0"

// 版本信息函数
static inline const char* get_version(void) {
    return CALC_VERSION;
}

#endif