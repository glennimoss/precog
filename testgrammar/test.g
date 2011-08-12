grammar test;

options {
  language=Python;
  output=AST;
}

tokens {
  STMT;
}


@lexer::header {
  from antlr3.ext import NamedConstant

  NL_CHANNEL = DEFAULT_CHANNEL + 1
}

@lexer::members {
  def aloneOnLine (self, dir=None):
    if not dir:
      return self.aloneOnLine(-1) and self.aloneOnLine(1)

    # A terminator can only occur on a line by itself, possibly with whitespace
    p = 1 if dir == 1 else 0
    c = 0
    while c != EOF:
      p += dir
      c = self.input.LT(p)
      if c == '\n':
        return True
      if not (c == ' ' or c == '\t'):
        return False

    # EOF is as good as a line terminator
    return True
}

@lexer::main {

  NamedConstant.name(locals())

  def main(argv):
      from antlr3.ext import MultiChannelTokenStream
      inStream = FileStream(argv[1])
      lexer = testLexer(inStream)
      tokenStream = MultiChannelTokenStream(lexer)
      tokenStream.add(NL_CHANNEL, HIDDEN)
      for t in tokenStream.getTokens():
        print(t)
}

@main {
  def main(argv):
    from antlr3.ext import MultiChannelTokenStream
    from .testLexer import testLexer
    inStream = FileStream(argv[1])
    lexer = testLexer(inStream)
    tokenStream = MultiChannelTokenStream(lexer)
    parser = testParser(tokenStream)
    result = parser.prog()
    if result is not None:
      if hasattr(result, 'tree'):
        if result.tree is not None:
          print(result.tree.toStringTree())
      else:
        print(repr(result))
}


prog
  : stmt* EOF
  ;

stmt
  : //foo+=(WORD | SYMBOL)+ TERMINATOR
    comma_separated[SYMBOL]
  ;

comma_separated[token]
  : {self.input.LA(1) == $token}? . (COMMA^ {self.input.LA(1) == $token}? .)*
  ;

WORD : ( 'a'..'z' | 'A'..'Z' | '0'..'9' )+ ;
SYMBOL : ('!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(' | ')' ) { #$channel=HIDDEN };
COMMA : ',';
SLASH : '/' ;
NL : '\r'? '\n' { $channel=HIDDEN };
SPACE	:	(' '|'\t') { $channel=HIDDEN };
SL_COMMENT
	:	'--' ~('\n'|'\r')* NL { $channel=HIDDEN }
	;
ML_COMMENT
	:	'/*' ( options {greedy=false;} : . )* '*/' { $channel=HIDDEN }
	;
TERMINATOR
  : { self.aloneOnLine() }? SLASH
  ;
