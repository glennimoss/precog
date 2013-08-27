G := $(basename $(wildcard src/**/**/*.g))
#G := $(basename $(wildcard **/*.g))
DIR := $(dir $(G))

all: $(G)Lexer.py $(G)Parser.py

$(G)Lexer.py $(G)Parser.py: $(G).g lib/antlr-3.4-complete.jar
	# More verbosity: -Xwatchconversion
	java -jar lib/antlr-3.4-complete.jar -fo $(DIR) $(G).g

lib/antlr-3.4-complete.jar: lib/org/antlr/codegen/templates/Python/*
	jar uvf lib/antlr-3.4-complete.jar -C lib org

clean:
	rm -f $(G)Lexer.* $(G)Parser.* $(G).tokens

.PHONY: clean
