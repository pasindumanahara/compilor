# lexer.py

import sys
import string


# Ensure file is provided
if len(sys.argv) < 2:
    print("Usage: python lexer.py <source_file>")
    sys.exit(1)

source_file = sys.argv[1]

# Read file content
with open(source_file, "r") as f:
    content = f.read()

tokens = []
current = ""

i = 0
while i < len(content):
    ch = content[i]

    # Identifier or keyword (letters or _)
    if ch.isalpha() or ch == "_":
        current = ch
        i += 1
        while i < len(content) and (content[i].isalnum() or content[i] == "_"):
            current += content[i]
            i += 1
        tokens.append(("IDENT", current))
        continue

    # Number
    if ch.isdigit():
        current = ch
        i += 1
        while i < len(content) and content[i].isdigit():
            current += content[i]
            i += 1
        tokens.append(("NUMBER", current))
        continue

    # Whitespace → ignore
    if ch.isspace():
        i += 1
        continue

    # Single-character symbol
    if ch in string.punctuation:
        tokens.append(("SYMBOL", ch))
        i += 1
        continue

    # Unknown
    tokens.append(("UNKNOWN", ch))
    i += 1

print(tokens)
'''
# Print tokens
for t in tokens:
    print(t)
'''