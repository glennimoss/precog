# $ANTLR 3.4 test.g 2011-07-29 01:44:06

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

               
NL_CHANNEL = DEFAULT_CHANNEL + 1



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
ML_COMMENT=4
NL=5
SLASH=6
SL_COMMENT=7
SPACE=8
TERMINATOR=9


class test(Lexer):

    grammarFileName = "test.g"
    api_version = 1

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(test, self).__init__(input, state)

        self.delegates = []






    # $ANTLR start "SLASH"
    def mSLASH(self, ):
        try:
            _type = SLASH
            _channel = DEFAULT_CHANNEL

            # test.g:24:7: ( '/' )
            # test.g:24:9: '/'
            pass 
            self.match(47)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "SLASH"



    # $ANTLR start "NL"
    def mNL(self, ):
        try:
            _type = NL
            _channel = DEFAULT_CHANNEL

            # test.g:25:4: ( ( '\\r' )? '\\n' )
            # test.g:25:6: ( '\\r' )? '\\n'
            pass 
            # test.g:25:6: ( '\\r' )?
            alt1 = 2
            LA1_0 = self.input.LA(1)

            if (LA1_0 == 13) :
                alt1 = 1
            if alt1 == 1:
                # test.g:25:6: '\\r'
                pass 
                self.match(13)




            self.match(10)

            #action start
            _channel = NL_CHANNEL 
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "NL"



    # $ANTLR start "SPACE"
    def mSPACE(self, ):
        try:
            _type = SPACE
            _channel = DEFAULT_CHANNEL

            # test.g:26:7: ( ( ' ' | '\\t' ) )
            # test.g:26:9: ( ' ' | '\\t' )
            pass 
            if self.input.LA(1) == 9 or self.input.LA(1) == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            #action start
            _channel=HIDDEN 
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "SPACE"



    # $ANTLR start "TERMINATOR"
    def mTERMINATOR(self, ):
        try:
            _type = TERMINATOR
            _channel = DEFAULT_CHANNEL

            # test.g:28:3: ({...}? => ( ' ' )* SLASH ( ' ' )* NL )
            # test.g:28:5: {...}? => ( ' ' )* SLASH ( ' ' )* NL
            pass 
            if not ((self.input.LT(-1) == '\n' )):
                raise FailedPredicateException(self.input, "TERMINATOR", " self.input.LT(-1) == '\\n' ")


            # test.g:28:38: ( ' ' )*
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if (LA2_0 == 32) :
                    alt2 = 1


                if alt2 == 1:
                    # test.g:28:38: ' '
                    pass 
                    self.match(32)


                else:
                    break #loop2


            self.mSLASH()


            # test.g:28:49: ( ' ' )*
            while True: #loop3
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == 32) :
                    alt3 = 1


                if alt3 == 1:
                    # test.g:28:49: ' '
                    pass 
                    self.match(32)


                else:
                    break #loop3


            self.mNL()




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "TERMINATOR"



    # $ANTLR start "SL_COMMENT"
    def mSL_COMMENT(self, ):
        try:
            _type = SL_COMMENT
            _channel = DEFAULT_CHANNEL

            # test.g:31:2: ( '--' (~ ( '\\n' | '\\r' ) )* NL )
            # test.g:31:4: '--' (~ ( '\\n' | '\\r' ) )* NL
            pass 
            self.match("--")


            # test.g:31:9: (~ ( '\\n' | '\\r' ) )*
            while True: #loop4
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if ((0 <= LA4_0 <= 9) or (11 <= LA4_0 <= 12) or (14 <= LA4_0 <= 65535)) :
                    alt4 = 1


                if alt4 == 1:
                    # test.g:
                    pass 
                    if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop4


            self.mNL()


            #action start
            _channel=HIDDEN;
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "SL_COMMENT"



    # $ANTLR start "ML_COMMENT"
    def mML_COMMENT(self, ):
        try:
            _type = ML_COMMENT
            _channel = DEFAULT_CHANNEL

            # test.g:34:2: ( '/*' ( options {greedy=false; } : . )* '*/' )
            # test.g:34:4: '/*' ( options {greedy=false; } : . )* '*/'
            pass 
            self.match("/*")


            # test.g:34:9: ( options {greedy=false; } : . )*
            while True: #loop5
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 42) :
                    LA5_1 = self.input.LA(2)

                    if (LA5_1 == 47) :
                        alt5 = 2
                    elif ((0 <= LA5_1 <= 46) or (48 <= LA5_1 <= 65535)) :
                        alt5 = 1


                elif ((0 <= LA5_0 <= 41) or (43 <= LA5_0 <= 65535)) :
                    alt5 = 1


                if alt5 == 1:
                    # test.g:34:37: .
                    pass 
                    self.matchAny()


                else:
                    break #loop5


            self.match("*/")


            #action start
            _channel=HIDDEN;
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "ML_COMMENT"



    def mTokens(self):
        # test.g:1:8: ( SLASH | NL | SPACE | TERMINATOR | SL_COMMENT | ML_COMMENT )
        alt6 = 6
        LA6 = self.input.LA(1)
        if LA6 == 47:
            LA6_1 = self.input.LA(2)

            if (LA6_1 == 42) :
                alt6 = 6
            elif (LA6_1 == 10 or LA6_1 == 13 or LA6_1 == 32) and ((self.input.LT(-1) == '\n' )):
                alt6 = 4
            else:
                alt6 = 1

        elif LA6 == 10 or LA6 == 13:
            alt6 = 2
        elif LA6 == 32:
            LA6_3 = self.input.LA(2)

            if (LA6_3 == 32 or LA6_3 == 47) and ((self.input.LT(-1) == '\n' )):
                alt6 = 4
            else:
                alt6 = 3

        elif LA6 == 9:
            alt6 = 3
        elif LA6 == 45:
            alt6 = 5
        else:
            nvae = NoViableAltException("", 6, 0, self.input)

            raise nvae


        if alt6 == 1:
            # test.g:1:10: SLASH
            pass 
            self.mSLASH()



        elif alt6 == 2:
            # test.g:1:16: NL
            pass 
            self.mNL()



        elif alt6 == 3:
            # test.g:1:19: SPACE
            pass 
            self.mSPACE()



        elif alt6 == 4:
            # test.g:1:25: TERMINATOR
            pass 
            self.mTERMINATOR()



        elif alt6 == 5:
            # test.g:1:36: SL_COMMENT
            pass 
            self.mSL_COMMENT()



        elif alt6 == 6:
            # test.g:1:47: ML_COMMENT
            pass 
            self.mML_COMMENT()








 



             
def main(argv):
    from custom_antlr import MultiChannelTokenStream
    from testLexer import testLexer
    inStream = ANTLRFileStream(argv[1])
    lexer = sqlLexer(inStream)
    tokenStream = MultiChannelTokenStream(lexer)
    tokenStream.add(NL_CHANNEL, HIDDEN)
    for t in tokenStream.getTokens():
      print t


if __name__ == '__main__':
    main(sys.argv)
