#include <stdio.h>

// 加法函数
int add(int a, int b) {
    return a + b;
}

// 减法函数
int subtract(int a, int b) {
    return a - b;
}

// 乘法函数
int multiply(int a, int b) {
    return a * b;
}

// 除法函数
double divide(int a, int b) {
    if (b == 0) {
        printf("错误：除数不能为零！\n");
        return 0;
    }
    return (double)a / b;
}

int main() {
    printf("简单计算器\n");
    printf("==========\n");

    int a = 10, b = 5;

    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d - %d = %d\n", a, b, subtract(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    printf("%d / %d = %.2f\n", a, b, divide(a, b));

    return 0;
}