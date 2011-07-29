G := $(basename $(wildcard *.g))

all: $(G)Lexer.py $(G)Parser.py

$(G)Lexer.py $(G)Parser.py: $(G).g
	antlr $(G).g

clean:
	rm -f $(G)Lexer.* $(G)Parser.* $(G).tokens

.PHONY: clean
