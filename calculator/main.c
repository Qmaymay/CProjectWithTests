/*
 * TODO calculator_app �µ���ɫ���� ����,
 * CLion ����������ģʽ��CMake ģʽ��ͨ�� CMakeLists.txt��
 * ��ȷ�������������ļ�ģʽ�����ٲ��Ե����ļ������޷�����������
 * �����python���빲��̬��ʱ��main.c �µ���ɫ����ֻ�����main.c
 * */
#include "calculator.h"
#include "version.h"
#include <stdio.h>


int main() {
    printf("Calculator Version:\n");
    printf("�򵥼�����\n");
    printf("==========\n");
    int a = 20, b = 10;

    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d - %d = %d\n", a, b, subtract(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    printf("%d / %d = %.2f\n", a, b, divide(a, b));
    printf("%d ^ 2 = %d\n", a, square(a));
    printf("%d ^ 3 "
           "= %d\n", a, cube(a));
    printf("%.2f ^ 2 = %.2f\n", (double)a, sqrt((double)a));
    printf("%d ^ %d = %.2f\n", a, b, power(a,b));

    return 0;
}