all: sqlLexer.py sqlParser.py

sqlLexer.py sqlParser.py: sql.g
	antlr sql.g
	2to3-3.1 -wn sqlLexer.py sqlParser.py

clean:
	rm -f sqlLexer.* sqlParser.* sql.tokens

.PHONY: clean
