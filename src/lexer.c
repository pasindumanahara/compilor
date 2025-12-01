#include "lexer.h"

static const char *source;
static int pos = 0;

void initLexer(const char *src) {
    source = src;
    pos = 0;
}

int isalpha(char *src){
    return ((src >= 'A' && src <= 'Z') || (src >= 'a' && src <= 'z'));
}

int isdigit(char *src){
    return ((src >= '0' && src <= '9'));
}

int isspace(char *src){
    return (src == ' ' || src == '\f' || src == '\n' || src == '\r' || src == '\t' || src == '\v');
}
int islnum(char *src){
    return 1;
}

Token getNextToken() {
    Token token = {TOKEN_END, ""};

    while (isspace(source[pos])) 
        pos++;

    if (isdigit(source[pos])) {
        int start = pos;
        while (isdigit(source[pos])) pos++;
        strncpy(token.value, source + start, pos - start);
        token.value[pos - start] = '\0';
        token.type = TOKEN_NUMBER;
        return token;
    }

    if (isalpha(source[pos])) {
        int start = pos;
        while (isalnum(source[pos])) pos++;
        strncpy(token.value, source + start, pos - start);
        token.value[pos - start] = '\0';
        token.type = TOKEN_IDENTIFIER;
        return token;
    }

    switch (source[pos]) {
        case '+': case '-': case '*': case '/':
            token.type = TOKEN_OPERATOR; token.value[0] = source[pos++]; token.value[1] = '\0'; break;
        case '=':
            token.type = TOKEN_ASSIGN; token.value[0] = source[pos++]; token.value[1] = '\0'; break;
        case ';':
            token.type = TOKEN_SEMICOLON; token.value[0] = source[pos++]; token.value[1] = '\0'; break;
        case '(':
            token.type = TOKEN_LPAREN; token.value[0] = source[pos++]; token.value[1] = '\0'; break;
        case ')':
            token.type = TOKEN_RPAREN; token.value[0] = source[pos++]; token.value[1] = '\0'; break;
        case '\0':
            token.type = TOKEN_END; break;
        default:
            printf("Unknown character: %c\n", source[pos++]);
            exit(1);
    }

    return token;
}
