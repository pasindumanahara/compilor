#ifndef COMMON_H
#define COMMON_H

typedef enum {
    TOKEN_NUMBER,
    TOKEN_IDENTIFIER,
    TOKEN_OPERATOR,
    TOKEN_ASSIGN,
    TOKEN_SEMICOLON,
    TOKEN_LPAREN, 
    TOKEN_RPAREN,
    TOKEN_END
} TokenType;


#endif