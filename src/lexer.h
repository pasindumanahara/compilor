/*TODO: Define functions here
and lexer.c file
CRITICAL ERROR*/

#ifndef LEXER_H
#define LECER_H
#include "common.h"

typedef struct
{
    TokenType type;
    char value[64];
}Token;

void initLexer(const char *src);
Token getNextToken();

#endif