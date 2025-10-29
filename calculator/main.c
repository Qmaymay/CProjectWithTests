#include "calculator.h"
#include <stdio.h>

int main() {
    printf("¼òµ¥¼ÆËãÆ÷\n");
    printf("==========\n");

    int a = 10, b = 5;

    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d - %d = %d\n", a, b, subtract(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    printf("%d / %d = %.2f\n", a, b, divide(a, b));
    printf("%d ^ 2 = %d\n", a, square(a));

    return 0;
}