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
    printf("%d ^ 3 = %d\n", a, cube(a));
    printf("%.2f ^ 2 = %.2f\n", (double)a, sqrt((double)a));
    printf("%d ^ %d = %.2f\n", a, b, power(a,b));

    return 0;
}