#include "calculator.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int divide(int a, int b) {
    if (b == 0) {
        return 0; // Error: division by zero
    }
    return a / b;
}

int power(int base, int exponent) {
    if (exponent < 0) {
        return 0; // Negative exponents not supported
    }
    if (exponent == 0) {
        return 1;
    }
    int result = 1;
    for (int i = 0; i < exponent; i++) {
        result *= base;
    }
    return result;
}

int factorial(int n) {
    if (n < 0) {
        return -1; // Error: negative number
    }
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

