G := $(basename $(wildcard *.g))

all: $(G)Lexer.py $(G)Parser.py

$(G)Lexer.py $(G)Parser.py: $(G).g
	antlr $(G).g
	2to3-3.1 -wn $(G)Lexer.py $(G)Parser.py

clean:
	rm -f $(G)Lexer.* $(G)Parser.* $(G).tokens

.PHONY: clean
