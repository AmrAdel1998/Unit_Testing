#ifndef CALCULATOR_H
#define CALCULATOR_H

/**
 * Adds two integers
 * @param a First integer
 * @param b Second integer
 * @return Sum of a and b
 */
int add(int a, int b);

/**
 * Subtracts second integer from first
 * @param a First integer
 * @param b Second integer
 * @return Difference (a - b)
 */
int subtract(int a, int b);

/**
 * Multiplies two integers
 * @param a First integer
 * @param b Second integer
 * @return Product of a and b
 */
int multiply(int a, int b);

/**
 * Divides first integer by second
 * @param a Dividend
 * @param b Divisor
 * @return Quotient, or 0 if divisor is 0
 */
int divide(int a, int b);

/**
 * Calculates power of base raised to exponent
 * @param base Base number
 * @param exponent Exponent
 * @return base^exponent, or 1 if exponent is 0
 */
int power(int base, int exponent);

/**
 * Calculates factorial of a number
 * @param n Non-negative integer
 * @return Factorial of n, or -1 if n is negative
 */
int factorial(int n);

#endif // CALCULATOR_H

