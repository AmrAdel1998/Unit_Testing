#ifndef STRING_UTILS_H
#define STRING_UTILS_H

/**
 * Reverses a string in place
 * @param str String to reverse (must be null-terminated)
 * @return Pointer to the reversed string, or NULL if str is NULL
 */
char* reverse_string(char* str);

/**
 * Converts string to uppercase
 * @param str String to convert
 * @return Pointer to the converted string
 */
char* to_uppercase(char* str);

/**
 * Converts string to lowercase
 * @param str String to convert
 * @return Pointer to the converted string
 */
char* to_lowercase(char* str);

/**
 * Removes whitespace from beginning and end of string
 * @param str String to trim
 * @return Pointer to trimmed string
 */
char* trim_string(char* str);

/**
 * Checks if string is a palindrome
 * @param str String to check
 * @return 1 if palindrome, 0 otherwise
 */
int is_palindrome(const char* str);

/**
 * Counts occurrences of a character in a string
 * @param str String to search
 * @param ch Character to count
 * @return Number of occurrences
 */
int count_char(const char* str, char ch);

#endif // STRING_UTILS_H

