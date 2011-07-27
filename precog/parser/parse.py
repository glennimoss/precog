import sys

import antlr3
from sqlLexer import sqlLexer
from sqlParser import sqlParser

#sqlstr = 'create table foo (id number)'

char_stream = antlr3.ANTLRFileStream(sys.argv[1])
lexer = sqlLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = sqlParser(tokens)
root = parser.create_object()

print(root)

