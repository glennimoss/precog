grammar test;

options {
  language=Python;
  backtrack=true;
}


@lexer::header {
  NL_CHANNEL = DEFAULT_CHANNEL + 1
}

@lexer::main {
  def main(argv):
      from custom_antlr import MultiChannelTokenStream
      from testLexer import testLexer
      inStream = ANTLRFileStream(argv[1])
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
  : NL ' '* SLASH ' '* NL
  ;
