// Sample C file for testing the pytest tool

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * Adds two integers
 * @param a First integer
 * @param b Second integer
 * @return Sum of a and b
 */
int add(int a, int b) {
    return a + b;
}

/**
 * Multiplies two integers
 * @param a First integer
 * @param b Second integer
 * @return Product of a and b
 */
int multiply(int a, int b) {
    return a * b;
}

/**
 * Calculates the factorial of a number
 * @param n Non-negative integer
 * @return Factorial of n, or -1 if n is negative
 */
int factorial(int n) {
    if (n < 0) {
        return -1;
    }
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

/**
 * Finds the maximum value in an array
 * @param arr Array of integers
 * @param size Size of the array
 * @return Maximum value, or INT_MIN if array is empty
 */
int find_max(int arr[], int size) {
    if (size <= 0) {
        return -2147483648; // INT_MIN
    }
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

/**
 * Reverses a string in place
 * @param str String to reverse (must be null-terminated)
 * @return Pointer to the reversed string
 */
char* reverse_string(char* str) {
    if (str == NULL) {
        return NULL;
    }
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
    return str;
}

