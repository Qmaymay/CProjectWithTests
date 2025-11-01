//
// Created by Admin on 2025/11/1.
//

#ifndef VERSION_H
#define VERSION_H

// C开发只管前两位，第三位永远为0
#define CALC_MAJOR_VERSION 1
#define CALC_MINOR_VERSION 19
#define CALC_VERSION "1.8.0"  // 第三位固定为0


static inline const char* get_version(void) {
    return CALC_VERSION;
}

#endif
