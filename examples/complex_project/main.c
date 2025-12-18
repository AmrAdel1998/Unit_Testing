#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "calculator.h"
#include "string_utils.h"
#include "data_structures.h"

int main(int argc, char *argv[]) {
    printf("Complex C Project Demo\n");
    
    // Test calculator
    int result = add(10, 20);
    printf("10 + 20 = %d\n", result);
    
    result = multiply(5, 6);
    printf("5 * 6 = %d\n", result);
    
    // Test string utilities
    char str[] = "Hello World";
    reverse_string(str);
    printf("Reversed: %s\n", str);
    
    // Test data structures
    Stack *stack = create_stack(10);
    push(stack, 42);
    push(stack, 100);
    printf("Stack top: %d\n", peek(stack));
    
    destroy_stack(stack);
    
    return 0;
}

