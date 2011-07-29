grammar test;

options {
  language=Python;
}


@lexer::header {
  from custom_antlr import NamedConstant

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
      from custom_antlr import MultiChannelTokenStream
      inStream = FileStream(argv[1])
      lexer = testLexer(inStream)
      tokenStream = MultiChannelTokenStream(lexer)
      tokenStream.add(NL_CHANNEL, HIDDEN)
      for t in tokenStream.getTokens():
        print t
}

prog :
  SLASH
  ;

SLASH : '/' ;
NL : '\r'? '\n' ;
SPACE	:	(' '|'\t') ;
SL_COMMENT
	:	'--' ~('\n'|'\r')* NL {$channel=HIDDEN;}
	;
ML_COMMENT
	:	'/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
	; 
TERMINATOR
  : { self.aloneOnLine() }? SLASH
  ;
