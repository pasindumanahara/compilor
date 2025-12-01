#include <stdio.h>
#include "common.h"
#include "lexer.h"

// Helper function to convert Enum ID to String for readable output
const char* getTokenTypeString(TokenType type) {
    switch (type) {
        case TOKEN_NUMBER:     return "NUMBER";
        case TOKEN_IDENTIFIER: return "IDENTIFIER";
        case TOKEN_OPERATOR:   return "OPERATOR";
        case TOKEN_ASSIGN:     return "ASSIGN";
        case TOKEN_SEMICOLON:  return "SEMICOLON";
        case TOKEN_LPAREN:     return "LPAREN";
        case TOKEN_RPAREN:     return "RPAREN";
        case TOKEN_END:        return "EOF";
        default:               return "UNKNOWN";
    }
}

int main() {
    // 1. The source code we want to test
    // We test identifiers, numbers, assignment, and operators here.
    const char *code = "sum = a + 10;";

    printf("Scanning source: \"%s\"\n", code);
    printf("----------------------------------------\n");
    printf("%-15s | %s\n", "TOKEN TYPE", "VALUE");
    printf("----------------------------------------\n");

    // 2. Initialize the lexer
    initLexer(code);

    Token token;
    
    // 3. Loop until we hit the end of the string
    do {
        token = getNextToken();

        // Print the result
        printf("%-15s | '%s'\n", 
               getTokenTypeString(token.type), 
               token.value);

    } while (token.type != TOKEN_END);

    return 0;
}