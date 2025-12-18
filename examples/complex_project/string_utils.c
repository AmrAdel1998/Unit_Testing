#include "string_utils.h"
#include <ctype.h>
#include <string.h>

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

char* to_uppercase(char* str) {
    if (str == NULL) {
        return NULL;
    }
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = toupper(str[i]);
    }
    return str;
}

char* to_lowercase(char* str) {
    if (str == NULL) {
        return NULL;
    }
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = tolower(str[i]);
    }
    return str;
}

char* trim_string(char* str) {
    if (str == NULL) {
        return NULL;
    }
    
    // Trim leading whitespace
    char* start = str;
    while (isspace(*start)) {
        start++;
    }
    
    // Trim trailing whitespace
    char* end = str + strlen(str) - 1;
    while (end > start && isspace(*end)) {
        *end = '\0';
        end--;
    }
    
    // Move trimmed string to beginning
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }
    
    return str;
}

int is_palindrome(const char* str) {
    if (str == NULL) {
        return 0;
    }
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        if (str[i] != str[len - 1 - i]) {
            return 0;
        }
    }
    return 1;
}

int count_char(const char* str, char ch) {
    if (str == NULL) {
        return 0;
    }
    int count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == ch) {
            count++;
        }
    }
    return count;
}

