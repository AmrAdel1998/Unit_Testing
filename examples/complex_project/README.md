# Complex C Project Example

This is a comprehensive C project example designed to test the pytest tool's parsing capabilities on larger, more complex projects.

## Project Structure

```
complex_project/
├── main.c                 # Main entry point
├── calculator.h           # Calculator header
├── calculator.c           # Calculator implementation
├── string_utils.h         # String utilities header
├── string_utils.c         # String utilities implementation
├── data_structures.h      # Data structures header
├── data_structures.c      # Data structures implementation
└── README.md             # This file
```

## Features

### Calculator Module
- `add()` - Addition
- `subtract()` - Subtraction
- `multiply()` - Multiplication
- `divide()` - Division with error handling
- `power()` - Exponentiation
- `factorial()` - Factorial calculation

### String Utilities Module
- `reverse_string()` - Reverse string in place
- `to_uppercase()` - Convert to uppercase
- `to_lowercase()` - Convert to lowercase
- `trim_string()` - Remove leading/trailing whitespace
- `is_palindrome()` - Check if string is palindrome
- `count_char()` - Count character occurrences

### Data Structures Module
- **Stack**: LIFO data structure
  - `create_stack()` - Create new stack
  - `push()` - Push element
  - `pop()` - Pop element
  - `peek()` - View top element
  - `is_empty()` - Check if empty
  - `is_full()` - Check if full
  - `destroy_stack()` - Free memory

- **Queue**: FIFO data structure
  - `create_queue()` - Create new queue
  - `enqueue()` - Add element
  - `dequeue()` - Remove element
  - `destroy_queue()` - Free memory

## Total Functions

This project contains **20+ functions** across multiple modules, making it a good test case for:
- Parsing multiple files
- Handling header files (.h)
- Processing function signatures
- Generating comprehensive test cases

## Usage with Pytest Tool

1. In the "Parse C Project" tab, set the project path to:
   ```
   examples/complex_project
   ```

2. Click "Parse Project" to extract all functions

3. Generate tests - the tool will create test files for all 20+ functions

4. Run tests to verify functionality

## Compilation (Optional)

To compile and run this project:

```bash
cd examples/complex_project
gcc -o complex_project *.c
./complex_project
```

