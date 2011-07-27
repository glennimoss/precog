# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 sql.g 2011-07-27 17:07:15

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
PACKAGE=115
FUNCTION=8
EXTERNAL=117
EXPONENT=99
WHILE=87
DETERMINISTIC=36
VARYING=26
CASE=50
DOUBLEDOT=66
NOT=20
SUBTYPE=24
EOF=-1
SQL=100
RPAREN=12
CREATE=114
INSERT=79
USING=62
RETURNING=63
BEGIN=41
LOOP=49
SAVEPOINT=82
RETURN=9
BODY=116
RAISE=74
GEQ=93
GOTO=69
EQ=88
SELECT=83
ISOPEN=102
INTO=59
ARRAY=27
DIVIDE=4
EXCEPTION=23
RBRACK=125
EXIT=56
RECORD=25
N=128
TRANSACTION=85
NULL=21
ELSE=51
AT_SIGN=124
DEFINER=120
DELETE=48
DOUBLEVERTBAR=97
ROLLBACK=81
AUTHID=118
NOCOPY=15
WS=130
LANGUAGE=121
FETCH=57
OUT=14
REAL_NUMBER=105
PIPELINED=37
SL_COMMENT=131
OR=44
CONSTANT=22
ELSIF=71
END=42
FALSE=107
COLLECT=61
CURSOR=18
OTHERS=45
LBRACK=126
POINT=123
CURRENT_USER=119
LIMIT=58
EXECUTE=54
INSERTING=110
GTH=92
NOTFOUND=103
PRAGMA=73
RESULT_CACHE=39
TABLE=29
LLABEL=76
UPDATE=86
FOR=64
ID=7
AND=68
ASTERISK=98
LPAREN=10
LOCK=80
UPDATING=111
IF=70
RLABEL=77
ML_COMMENT=132
AS=40
INDEX=30
ROWTYPE=35
IN=13
THEN=46
CONTINUE=53
COMMA=11
IS=19
QUOTED_STRING=108
PLUS=96
EXISTS=109
DOT=33
LIKE=94
INTEGER=104
BY=31
VARRAY=28
PARALLEL_ENABLE=38
PERCENT=34
DOUBLEQUOTED_STRING=122
DEFAULT=17
FORALL=65
SET=84
MINUS=95
TRUE=106
SEMI=5
PROCEDURE=6
NOT_EQ=89
REF=32
VERTBAR=127
COLON=47
OPEN=72
LTH=90
BULK_ROWCOUNT=101
COMMIT=78
CLOSE=52
WHEN=43
ASSIGN=16
NUMBER_VALUE=129
IMMEDIATE=55
ARROW=113
DECLARE=75
DELETING=112
BULK=60
BETWEEN=67
LEQ=91

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "DIVIDE", "SEMI", "PROCEDURE", "ID", "FUNCTION", "RETURN", "LPAREN", 
    "COMMA", "RPAREN", "IN", "OUT", "NOCOPY", "ASSIGN", "DEFAULT", "CURSOR", 
    "IS", "NOT", "NULL", "CONSTANT", "EXCEPTION", "SUBTYPE", "RECORD", "VARYING", 
    "ARRAY", "VARRAY", "TABLE", "INDEX", "BY", "REF", "DOT", "PERCENT", 
    "ROWTYPE", "DETERMINISTIC", "PIPELINED", "PARALLEL_ENABLE", "RESULT_CACHE", 
    "AS", "BEGIN", "END", "WHEN", "OR", "OTHERS", "THEN", "COLON", "DELETE", 
    "LOOP", "CASE", "ELSE", "CLOSE", "CONTINUE", "EXECUTE", "IMMEDIATE", 
    "EXIT", "FETCH", "LIMIT", "INTO", "BULK", "COLLECT", "USING", "RETURNING", 
    "FOR", "FORALL", "DOUBLEDOT", "BETWEEN", "AND", "GOTO", "IF", "ELSIF", 
    "OPEN", "PRAGMA", "RAISE", "DECLARE", "LLABEL", "RLABEL", "COMMIT", 
    "INSERT", "LOCK", "ROLLBACK", "SAVEPOINT", "SELECT", "SET", "TRANSACTION", 
    "UPDATE", "WHILE", "EQ", "NOT_EQ", "LTH", "LEQ", "GTH", "GEQ", "LIKE", 
    "MINUS", "PLUS", "DOUBLEVERTBAR", "ASTERISK", "EXPONENT", "SQL", "BULK_ROWCOUNT", 
    "ISOPEN", "NOTFOUND", "INTEGER", "REAL_NUMBER", "TRUE", "FALSE", "QUOTED_STRING", 
    "EXISTS", "INSERTING", "UPDATING", "DELETING", "ARROW", "CREATE", "PACKAGE", 
    "BODY", "EXTERNAL", "AUTHID", "CURRENT_USER", "DEFINER", "LANGUAGE", 
    "DOUBLEQUOTED_STRING", "POINT", "AT_SIGN", "RBRACK", "LBRACK", "VERTBAR", 
    "N", "NUMBER_VALUE", "WS", "SL_COMMENT", "ML_COMMENT"
]




class sqlParser(Parser):
    grammarFileName = "sql.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(sqlParser, self).__init__(input, state, *args, **kwargs)

        self.dfa13 = self.DFA13(
            self, 13,
            eot = self.DFA13_eot,
            eof = self.DFA13_eof,
            min = self.DFA13_min,
            max = self.DFA13_max,
            accept = self.DFA13_accept,
            special = self.DFA13_special,
            transition = self.DFA13_transition
            )

        self.dfa93 = self.DFA93(
            self, 93,
            eot = self.DFA93_eot,
            eof = self.DFA93_eof,
            min = self.DFA93_min,
            max = self.DFA93_max,
            accept = self.DFA93_accept,
            special = self.DFA93_special,
            transition = self.DFA93_transition
            )

        self.dfa136 = self.DFA136(
            self, 136,
            eot = self.DFA136_eot,
            eof = self.DFA136_eof,
            min = self.DFA136_min,
            max = self.DFA136_max,
            accept = self.DFA136_accept,
            special = self.DFA136_special,
            transition = self.DFA136_transition
            )






        self._adaptor = None
        self.adaptor = CommonTreeAdaptor()
                


        
    def getTreeAdaptor(self):
        return self._adaptor

    def setTreeAdaptor(self, adaptor):
        self._adaptor = adaptor

    adaptor = property(getTreeAdaptor, setTreeAdaptor)


    class sqlplus_file_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.sqlplus_file_return, self).__init__()

            self.tree = None




    # $ANTLR start "sqlplus_file"
    # sql.g:39:1: sqlplus_file : ( create_object ( DIVIDE show_errors )? ( DIVIDE )? )+ EOF ;
    def sqlplus_file(self, ):

        retval = self.sqlplus_file_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DIVIDE2 = None
        DIVIDE4 = None
        EOF5 = None
        create_object1 = None

        show_errors3 = None


        DIVIDE2_tree = None
        DIVIDE4_tree = None
        EOF5_tree = None

        try:
            try:
                # sql.g:40:5: ( ( create_object ( DIVIDE show_errors )? ( DIVIDE )? )+ EOF )
                # sql.g:40:7: ( create_object ( DIVIDE show_errors )? ( DIVIDE )? )+ EOF
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:40:7: ( create_object ( DIVIDE show_errors )? ( DIVIDE )? )+
                cnt3 = 0
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == CREATE) :
                        alt3 = 1


                    if alt3 == 1:
                        # sql.g:40:9: create_object ( DIVIDE show_errors )? ( DIVIDE )?
                        pass 
                        self._state.following.append(self.FOLLOW_create_object_in_sqlplus_file47)
                        create_object1 = self.create_object()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, create_object1.tree)
                        # sql.g:40:23: ( DIVIDE show_errors )?
                        alt1 = 2
                        LA1_0 = self.input.LA(1)

                        if (LA1_0 == DIVIDE) :
                            LA1_1 = self.input.LA(2)

                            if (LA1_1 == ID) :
                                alt1 = 1
                        if alt1 == 1:
                            # sql.g:40:25: DIVIDE show_errors
                            pass 
                            DIVIDE2=self.match(self.input, DIVIDE, self.FOLLOW_DIVIDE_in_sqlplus_file51)

                            DIVIDE2_tree = self._adaptor.createWithPayload(DIVIDE2)
                            self._adaptor.addChild(root_0, DIVIDE2_tree)

                            self._state.following.append(self.FOLLOW_show_errors_in_sqlplus_file53)
                            show_errors3 = self.show_errors()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, show_errors3.tree)



                        # sql.g:40:47: ( DIVIDE )?
                        alt2 = 2
                        LA2_0 = self.input.LA(1)

                        if (LA2_0 == DIVIDE) :
                            alt2 = 1
                        if alt2 == 1:
                            # sql.g:40:47: DIVIDE
                            pass 
                            DIVIDE4=self.match(self.input, DIVIDE, self.FOLLOW_DIVIDE_in_sqlplus_file58)

                            DIVIDE4_tree = self._adaptor.createWithPayload(DIVIDE4)
                            self._adaptor.addChild(root_0, DIVIDE4_tree)






                    else:
                        if cnt3 >= 1:
                            break #loop3

                        eee = EarlyExitException(3, self.input)
                        raise eee

                    cnt3 += 1
                EOF5=self.match(self.input, EOF, self.FOLLOW_EOF_in_sqlplus_file64)

                EOF5_tree = self._adaptor.createWithPayload(EOF5)
                self._adaptor.addChild(root_0, EOF5_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "sqlplus_file"

    class show_errors_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.show_errors_return, self).__init__()

            self.tree = None




    # $ANTLR start "show_errors"
    # sql.g:43:1: show_errors : kSHOW kERRORS ( SEMI )? ;
    def show_errors(self, ):

        retval = self.show_errors_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SEMI8 = None
        kSHOW6 = None

        kERRORS7 = None


        SEMI8_tree = None

        try:
            try:
                # sql.g:44:5: ( kSHOW kERRORS ( SEMI )? )
                # sql.g:44:7: kSHOW kERRORS ( SEMI )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_kSHOW_in_show_errors85)
                kSHOW6 = self.kSHOW()

                self._state.following.pop()
                self._adaptor.addChild(root_0, kSHOW6.tree)
                self._state.following.append(self.FOLLOW_kERRORS_in_show_errors87)
                kERRORS7 = self.kERRORS()

                self._state.following.pop()
                self._adaptor.addChild(root_0, kERRORS7.tree)
                # sql.g:44:21: ( SEMI )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == SEMI) :
                    alt4 = 1
                if alt4 == 1:
                    # sql.g:44:21: SEMI
                    pass 
                    SEMI8=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_show_errors89)

                    SEMI8_tree = self._adaptor.createWithPayload(SEMI8)
                    self._adaptor.addChild(root_0, SEMI8_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "show_errors"

    class create_object_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.create_object_return, self).__init__()

            self.tree = None




    # $ANTLR start "create_object"
    # sql.g:47:1: create_object : ( create_package | create_package_body | create_function | create_procedure );
    def create_object(self, ):

        retval = self.create_object_return()
        retval.start = self.input.LT(1)

        root_0 = None

        create_package9 = None

        create_package_body10 = None

        create_function11 = None

        create_procedure12 = None



        try:
            try:
                # sql.g:48:5: ( create_package | create_package_body | create_function | create_procedure )
                alt5 = 4
                LA5_0 = self.input.LA(1)

                if (LA5_0 == CREATE) :
                    LA5 = self.input.LA(2)
                    if LA5 == OR:
                        LA5_2 = self.input.LA(3)

                        if (LA5_2 == ID) :
                            LA5 = self.input.LA(4)
                            if LA5 == PROCEDURE:
                                alt5 = 4
                            elif LA5 == PACKAGE:
                                LA5_3 = self.input.LA(5)

                                if (LA5_3 == BODY) :
                                    alt5 = 2
                                elif (LA5_3 == ID) :
                                    alt5 = 1
                                else:
                                    nvae = NoViableAltException("", 5, 3, self.input)

                                    raise nvae

                            elif LA5 == FUNCTION:
                                alt5 = 3
                            else:
                                nvae = NoViableAltException("", 5, 6, self.input)

                                raise nvae

                        else:
                            nvae = NoViableAltException("", 5, 2, self.input)

                            raise nvae

                    elif LA5 == PACKAGE:
                        LA5_3 = self.input.LA(3)

                        if (LA5_3 == BODY) :
                            alt5 = 2
                        elif (LA5_3 == ID) :
                            alt5 = 1
                        else:
                            nvae = NoViableAltException("", 5, 3, self.input)

                            raise nvae

                    elif LA5 == FUNCTION:
                        alt5 = 3
                    elif LA5 == PROCEDURE:
                        alt5 = 4
                    else:
                        nvae = NoViableAltException("", 5, 1, self.input)

                        raise nvae

                else:
                    nvae = NoViableAltException("", 5, 0, self.input)

                    raise nvae

                if alt5 == 1:
                    # sql.g:48:7: create_package
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_create_package_in_create_object107)
                    create_package9 = self.create_package()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, create_package9.tree)


                elif alt5 == 2:
                    # sql.g:49:7: create_package_body
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_create_package_body_in_create_object115)
                    create_package_body10 = self.create_package_body()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, create_package_body10.tree)


                elif alt5 == 3:
                    # sql.g:50:7: create_function
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_create_function_in_create_object123)
                    create_function11 = self.create_function()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, create_function11.tree)


                elif alt5 == 4:
                    # sql.g:51:7: create_procedure
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_create_procedure_in_create_object131)
                    create_procedure12 = self.create_procedure()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, create_procedure12.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "create_object"

    class procedure_heading_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.procedure_heading_return, self).__init__()

            self.tree = None




    # $ANTLR start "procedure_heading"
    # sql.g:54:1: procedure_heading : PROCEDURE ID ( parameter_declarations )? ;
    def procedure_heading(self, ):

        retval = self.procedure_heading_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PROCEDURE13 = None
        ID14 = None
        parameter_declarations15 = None


        PROCEDURE13_tree = None
        ID14_tree = None

        try:
            try:
                # sql.g:54:19: ( PROCEDURE ID ( parameter_declarations )? )
                # sql.g:55:9: PROCEDURE ID ( parameter_declarations )?
                pass 
                root_0 = self._adaptor.nil()

                PROCEDURE13=self.match(self.input, PROCEDURE, self.FOLLOW_PROCEDURE_in_procedure_heading152)

                PROCEDURE13_tree = self._adaptor.createWithPayload(PROCEDURE13)
                self._adaptor.addChild(root_0, PROCEDURE13_tree)

                ID14=self.match(self.input, ID, self.FOLLOW_ID_in_procedure_heading154)

                ID14_tree = self._adaptor.createWithPayload(ID14)
                self._adaptor.addChild(root_0, ID14_tree)

                # sql.g:55:22: ( parameter_declarations )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == LPAREN) :
                    alt6 = 1
                if alt6 == 1:
                    # sql.g:55:22: parameter_declarations
                    pass 
                    self._state.following.append(self.FOLLOW_parameter_declarations_in_procedure_heading156)
                    parameter_declarations15 = self.parameter_declarations()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, parameter_declarations15.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "procedure_heading"

    class function_heading_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.function_heading_return, self).__init__()

            self.tree = None




    # $ANTLR start "function_heading"
    # sql.g:58:1: function_heading : FUNCTION ID ( parameter_declarations )? RETURN datatype ;
    def function_heading(self, ):

        retval = self.function_heading_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FUNCTION16 = None
        ID17 = None
        RETURN19 = None
        parameter_declarations18 = None

        datatype20 = None


        FUNCTION16_tree = None
        ID17_tree = None
        RETURN19_tree = None

        try:
            try:
                # sql.g:58:18: ( FUNCTION ID ( parameter_declarations )? RETURN datatype )
                # sql.g:59:9: FUNCTION ID ( parameter_declarations )? RETURN datatype
                pass 
                root_0 = self._adaptor.nil()

                FUNCTION16=self.match(self.input, FUNCTION, self.FOLLOW_FUNCTION_in_function_heading178)

                FUNCTION16_tree = self._adaptor.createWithPayload(FUNCTION16)
                self._adaptor.addChild(root_0, FUNCTION16_tree)

                ID17=self.match(self.input, ID, self.FOLLOW_ID_in_function_heading180)

                ID17_tree = self._adaptor.createWithPayload(ID17)
                self._adaptor.addChild(root_0, ID17_tree)

                # sql.g:59:21: ( parameter_declarations )?
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == LPAREN) :
                    alt7 = 1
                if alt7 == 1:
                    # sql.g:59:21: parameter_declarations
                    pass 
                    self._state.following.append(self.FOLLOW_parameter_declarations_in_function_heading182)
                    parameter_declarations18 = self.parameter_declarations()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, parameter_declarations18.tree)



                RETURN19=self.match(self.input, RETURN, self.FOLLOW_RETURN_in_function_heading185)

                RETURN19_tree = self._adaptor.createWithPayload(RETURN19)
                self._adaptor.addChild(root_0, RETURN19_tree)

                self._state.following.append(self.FOLLOW_datatype_in_function_heading187)
                datatype20 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype20.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function_heading"

    class parameter_declarations_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.parameter_declarations_return, self).__init__()

            self.tree = None




    # $ANTLR start "parameter_declarations"
    # sql.g:62:1: parameter_declarations : ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN ) ;
    def parameter_declarations(self, ):

        retval = self.parameter_declarations_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LPAREN21 = None
        COMMA23 = None
        RPAREN25 = None
        parameter_declaration22 = None

        parameter_declaration24 = None


        LPAREN21_tree = None
        COMMA23_tree = None
        RPAREN25_tree = None

        try:
            try:
                # sql.g:62:24: ( ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN ) )
                # sql.g:63:9: ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:63:9: ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )
                # sql.g:63:13: LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN
                pass 
                LPAREN21=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_parameter_declarations212)

                LPAREN21_tree = self._adaptor.createWithPayload(LPAREN21)
                self._adaptor.addChild(root_0, LPAREN21_tree)

                self._state.following.append(self.FOLLOW_parameter_declaration_in_parameter_declarations215)
                parameter_declaration22 = self.parameter_declaration()

                self._state.following.pop()
                self._adaptor.addChild(root_0, parameter_declaration22.tree)
                # sql.g:63:43: ( COMMA parameter_declaration )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == COMMA) :
                        alt8 = 1


                    if alt8 == 1:
                        # sql.g:63:45: COMMA parameter_declaration
                        pass 
                        COMMA23=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_parameter_declarations219)

                        COMMA23_tree = self._adaptor.createWithPayload(COMMA23)
                        self._adaptor.addChild(root_0, COMMA23_tree)

                        self._state.following.append(self.FOLLOW_parameter_declaration_in_parameter_declarations222)
                        parameter_declaration24 = self.parameter_declaration()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, parameter_declaration24.tree)


                    else:
                        break #loop8
                RPAREN25=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_parameter_declarations227)

                RPAREN25_tree = self._adaptor.createWithPayload(RPAREN25)
                self._adaptor.addChild(root_0, RPAREN25_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "parameter_declarations"

    class parameter_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.parameter_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "parameter_declaration"
    # sql.g:66:1: parameter_declaration : ID ( IN | ( ( OUT | IN OUT ) ( NOCOPY )? ) )? datatype ( ( ASSIGN | DEFAULT ) expression )? ;
    def parameter_declaration(self, ):

        retval = self.parameter_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID26 = None
        IN27 = None
        OUT28 = None
        IN29 = None
        OUT30 = None
        NOCOPY31 = None
        set33 = None
        datatype32 = None

        expression34 = None


        ID26_tree = None
        IN27_tree = None
        OUT28_tree = None
        IN29_tree = None
        OUT30_tree = None
        NOCOPY31_tree = None
        set33_tree = None

        try:
            try:
                # sql.g:66:23: ( ID ( IN | ( ( OUT | IN OUT ) ( NOCOPY )? ) )? datatype ( ( ASSIGN | DEFAULT ) expression )? )
                # sql.g:67:9: ID ( IN | ( ( OUT | IN OUT ) ( NOCOPY )? ) )? datatype ( ( ASSIGN | DEFAULT ) expression )?
                pass 
                root_0 = self._adaptor.nil()

                ID26=self.match(self.input, ID, self.FOLLOW_ID_in_parameter_declaration250)

                ID26_tree = self._adaptor.createWithPayload(ID26)
                self._adaptor.addChild(root_0, ID26_tree)

                # sql.g:67:12: ( IN | ( ( OUT | IN OUT ) ( NOCOPY )? ) )?
                alt11 = 3
                LA11_0 = self.input.LA(1)

                if (LA11_0 == IN) :
                    LA11_1 = self.input.LA(2)

                    if (LA11_1 == OUT) :
                        alt11 = 2
                    elif (LA11_1 == ID or LA11_1 == REF) :
                        alt11 = 1
                elif (LA11_0 == OUT) :
                    alt11 = 2
                if alt11 == 1:
                    # sql.g:67:14: IN
                    pass 
                    IN27=self.match(self.input, IN, self.FOLLOW_IN_in_parameter_declaration254)

                    IN27_tree = self._adaptor.createWithPayload(IN27)
                    self._adaptor.addChild(root_0, IN27_tree)



                elif alt11 == 2:
                    # sql.g:67:19: ( ( OUT | IN OUT ) ( NOCOPY )? )
                    pass 
                    # sql.g:67:19: ( ( OUT | IN OUT ) ( NOCOPY )? )
                    # sql.g:67:21: ( OUT | IN OUT ) ( NOCOPY )?
                    pass 
                    # sql.g:67:21: ( OUT | IN OUT )
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if (LA9_0 == OUT) :
                        alt9 = 1
                    elif (LA9_0 == IN) :
                        alt9 = 2
                    else:
                        nvae = NoViableAltException("", 9, 0, self.input)

                        raise nvae

                    if alt9 == 1:
                        # sql.g:67:23: OUT
                        pass 
                        OUT28=self.match(self.input, OUT, self.FOLLOW_OUT_in_parameter_declaration262)

                        OUT28_tree = self._adaptor.createWithPayload(OUT28)
                        self._adaptor.addChild(root_0, OUT28_tree)



                    elif alt9 == 2:
                        # sql.g:67:29: IN OUT
                        pass 
                        IN29=self.match(self.input, IN, self.FOLLOW_IN_in_parameter_declaration266)

                        IN29_tree = self._adaptor.createWithPayload(IN29)
                        self._adaptor.addChild(root_0, IN29_tree)

                        OUT30=self.match(self.input, OUT, self.FOLLOW_OUT_in_parameter_declaration268)

                        OUT30_tree = self._adaptor.createWithPayload(OUT30)
                        self._adaptor.addChild(root_0, OUT30_tree)




                    # sql.g:67:38: ( NOCOPY )?
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == NOCOPY) :
                        alt10 = 1
                    if alt10 == 1:
                        # sql.g:67:38: NOCOPY
                        pass 
                        NOCOPY31=self.match(self.input, NOCOPY, self.FOLLOW_NOCOPY_in_parameter_declaration272)

                        NOCOPY31_tree = self._adaptor.createWithPayload(NOCOPY31)
                        self._adaptor.addChild(root_0, NOCOPY31_tree)










                self._state.following.append(self.FOLLOW_datatype_in_parameter_declaration280)
                datatype32 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype32.tree)
                # sql.g:68:9: ( ( ASSIGN | DEFAULT ) expression )?
                alt12 = 2
                LA12_0 = self.input.LA(1)

                if ((ASSIGN <= LA12_0 <= DEFAULT)) :
                    alt12 = 1
                if alt12 == 1:
                    # sql.g:68:11: ( ASSIGN | DEFAULT ) expression
                    pass 
                    set33 = self.input.LT(1)
                    if (ASSIGN <= self.input.LA(1) <= DEFAULT):
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set33))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse


                    self._state.following.append(self.FOLLOW_expression_in_parameter_declaration302)
                    expression34 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression34.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "parameter_declaration"

    class declare_section_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.declare_section_return, self).__init__()

            self.tree = None




    # $ANTLR start "declare_section"
    # sql.g:71:1: declare_section : ( type_definition SEMI | subtype_definition SEMI | cursor_definition SEMI | item_declaration SEMI | function_declaration_or_definition SEMI | procedure_declaration_or_definition SEMI | pragma SEMI )+ ;
    def declare_section(self, ):

        retval = self.declare_section_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SEMI36 = None
        SEMI38 = None
        SEMI40 = None
        SEMI42 = None
        SEMI44 = None
        SEMI46 = None
        SEMI48 = None
        type_definition35 = None

        subtype_definition37 = None

        cursor_definition39 = None

        item_declaration41 = None

        function_declaration_or_definition43 = None

        procedure_declaration_or_definition45 = None

        pragma47 = None


        SEMI36_tree = None
        SEMI38_tree = None
        SEMI40_tree = None
        SEMI42_tree = None
        SEMI44_tree = None
        SEMI46_tree = None
        SEMI48_tree = None

        try:
            try:
                # sql.g:71:17: ( ( type_definition SEMI | subtype_definition SEMI | cursor_definition SEMI | item_declaration SEMI | function_declaration_or_definition SEMI | procedure_declaration_or_definition SEMI | pragma SEMI )+ )
                # sql.g:72:5: ( type_definition SEMI | subtype_definition SEMI | cursor_definition SEMI | item_declaration SEMI | function_declaration_or_definition SEMI | procedure_declaration_or_definition SEMI | pragma SEMI )+
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:72:5: ( type_definition SEMI | subtype_definition SEMI | cursor_definition SEMI | item_declaration SEMI | function_declaration_or_definition SEMI | procedure_declaration_or_definition SEMI | pragma SEMI )+
                cnt13 = 0
                while True: #loop13
                    alt13 = 8
                    alt13 = self.dfa13.predict(self.input)
                    if alt13 == 1:
                        # sql.g:72:7: type_definition SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_type_definition_in_declare_section324)
                        type_definition35 = self.type_definition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, type_definition35.tree)
                        SEMI36=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section326)

                        SEMI36_tree = self._adaptor.createWithPayload(SEMI36)
                        self._adaptor.addChild(root_0, SEMI36_tree)



                    elif alt13 == 2:
                        # sql.g:73:7: subtype_definition SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_subtype_definition_in_declare_section334)
                        subtype_definition37 = self.subtype_definition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, subtype_definition37.tree)
                        SEMI38=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section336)

                        SEMI38_tree = self._adaptor.createWithPayload(SEMI38)
                        self._adaptor.addChild(root_0, SEMI38_tree)



                    elif alt13 == 3:
                        # sql.g:74:7: cursor_definition SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_cursor_definition_in_declare_section344)
                        cursor_definition39 = self.cursor_definition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, cursor_definition39.tree)
                        SEMI40=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section346)

                        SEMI40_tree = self._adaptor.createWithPayload(SEMI40)
                        self._adaptor.addChild(root_0, SEMI40_tree)



                    elif alt13 == 4:
                        # sql.g:75:7: item_declaration SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_item_declaration_in_declare_section354)
                        item_declaration41 = self.item_declaration()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, item_declaration41.tree)
                        SEMI42=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section356)

                        SEMI42_tree = self._adaptor.createWithPayload(SEMI42)
                        self._adaptor.addChild(root_0, SEMI42_tree)



                    elif alt13 == 5:
                        # sql.g:76:7: function_declaration_or_definition SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_function_declaration_or_definition_in_declare_section364)
                        function_declaration_or_definition43 = self.function_declaration_or_definition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, function_declaration_or_definition43.tree)
                        SEMI44=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section366)

                        SEMI44_tree = self._adaptor.createWithPayload(SEMI44)
                        self._adaptor.addChild(root_0, SEMI44_tree)



                    elif alt13 == 6:
                        # sql.g:77:7: procedure_declaration_or_definition SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_procedure_declaration_or_definition_in_declare_section374)
                        procedure_declaration_or_definition45 = self.procedure_declaration_or_definition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, procedure_declaration_or_definition45.tree)
                        SEMI46=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section376)

                        SEMI46_tree = self._adaptor.createWithPayload(SEMI46)
                        self._adaptor.addChild(root_0, SEMI46_tree)



                    elif alt13 == 7:
                        # sql.g:78:7: pragma SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_pragma_in_declare_section384)
                        pragma47 = self.pragma()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, pragma47.tree)
                        SEMI48=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_declare_section386)

                        SEMI48_tree = self._adaptor.createWithPayload(SEMI48)
                        self._adaptor.addChild(root_0, SEMI48_tree)



                    else:
                        if cnt13 >= 1:
                            break #loop13

                        eee = EarlyExitException(13, self.input)
                        raise eee

                    cnt13 += 1



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "declare_section"

    class cursor_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.cursor_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "cursor_definition"
    # sql.g:82:1: cursor_definition : CURSOR ID ( parameter_declarations )? IS select_statement ;
    def cursor_definition(self, ):

        retval = self.cursor_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        CURSOR49 = None
        ID50 = None
        IS52 = None
        parameter_declarations51 = None

        select_statement53 = None


        CURSOR49_tree = None
        ID50_tree = None
        IS52_tree = None

        try:
            try:
                # sql.g:82:19: ( CURSOR ID ( parameter_declarations )? IS select_statement )
                # sql.g:83:9: CURSOR ID ( parameter_declarations )? IS select_statement
                pass 
                root_0 = self._adaptor.nil()

                CURSOR49=self.match(self.input, CURSOR, self.FOLLOW_CURSOR_in_cursor_definition414)

                CURSOR49_tree = self._adaptor.createWithPayload(CURSOR49)
                self._adaptor.addChild(root_0, CURSOR49_tree)

                ID50=self.match(self.input, ID, self.FOLLOW_ID_in_cursor_definition416)

                ID50_tree = self._adaptor.createWithPayload(ID50)
                self._adaptor.addChild(root_0, ID50_tree)

                # sql.g:83:19: ( parameter_declarations )?
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if (LA14_0 == LPAREN) :
                    alt14 = 1
                if alt14 == 1:
                    # sql.g:83:19: parameter_declarations
                    pass 
                    self._state.following.append(self.FOLLOW_parameter_declarations_in_cursor_definition418)
                    parameter_declarations51 = self.parameter_declarations()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, parameter_declarations51.tree)



                IS52=self.match(self.input, IS, self.FOLLOW_IS_in_cursor_definition421)

                IS52_tree = self._adaptor.createWithPayload(IS52)
                self._adaptor.addChild(root_0, IS52_tree)

                self._state.following.append(self.FOLLOW_select_statement_in_cursor_definition423)
                select_statement53 = self.select_statement()

                self._state.following.pop()
                self._adaptor.addChild(root_0, select_statement53.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "cursor_definition"

    class item_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.item_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "item_declaration"
    # sql.g:86:1: item_declaration : ( variable_declaration | constant_declaration | exception_declaration );
    def item_declaration(self, ):

        retval = self.item_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        variable_declaration54 = None

        constant_declaration55 = None

        exception_declaration56 = None



        try:
            try:
                # sql.g:87:5: ( variable_declaration | constant_declaration | exception_declaration )
                alt15 = 3
                LA15_0 = self.input.LA(1)

                if (LA15_0 == ID) :
                    LA15 = self.input.LA(2)
                    if LA15 == CONSTANT:
                        alt15 = 2
                    elif LA15 == EXCEPTION:
                        alt15 = 3
                    elif LA15 == ID or LA15 == REF:
                        alt15 = 1
                    else:
                        nvae = NoViableAltException("", 15, 1, self.input)

                        raise nvae

                else:
                    nvae = NoViableAltException("", 15, 0, self.input)

                    raise nvae

                if alt15 == 1:
                    # sql.g:87:7: variable_declaration
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_variable_declaration_in_item_declaration440)
                    variable_declaration54 = self.variable_declaration()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, variable_declaration54.tree)


                elif alt15 == 2:
                    # sql.g:88:7: constant_declaration
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_constant_declaration_in_item_declaration448)
                    constant_declaration55 = self.constant_declaration()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, constant_declaration55.tree)


                elif alt15 == 3:
                    # sql.g:89:7: exception_declaration
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_exception_declaration_in_item_declaration456)
                    exception_declaration56 = self.exception_declaration()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exception_declaration56.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "item_declaration"

    class variable_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.variable_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "variable_declaration"
    # sql.g:92:1: variable_declaration : ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )? ;
    def variable_declaration(self, ):

        retval = self.variable_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID57 = None
        NOT59 = None
        NULL60 = None
        set61 = None
        datatype58 = None

        expression62 = None


        ID57_tree = None
        NOT59_tree = None
        NULL60_tree = None
        set61_tree = None

        try:
            try:
                # sql.g:92:22: ( ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )? )
                # sql.g:93:9: ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )?
                pass 
                root_0 = self._adaptor.nil()

                ID57=self.match(self.input, ID, self.FOLLOW_ID_in_variable_declaration477)

                ID57_tree = self._adaptor.createWithPayload(ID57)
                self._adaptor.addChild(root_0, ID57_tree)

                self._state.following.append(self.FOLLOW_datatype_in_variable_declaration479)
                datatype58 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype58.tree)
                # sql.g:93:21: ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )?
                alt17 = 2
                LA17_0 = self.input.LA(1)

                if ((ASSIGN <= LA17_0 <= DEFAULT) or LA17_0 == NOT) :
                    alt17 = 1
                if alt17 == 1:
                    # sql.g:93:24: ( NOT NULL )? ( ASSIGN | DEFAULT ) expression
                    pass 
                    # sql.g:93:24: ( NOT NULL )?
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if (LA16_0 == NOT) :
                        alt16 = 1
                    if alt16 == 1:
                        # sql.g:93:27: NOT NULL
                        pass 
                        NOT59=self.match(self.input, NOT, self.FOLLOW_NOT_in_variable_declaration487)

                        NOT59_tree = self._adaptor.createWithPayload(NOT59)
                        self._adaptor.addChild(root_0, NOT59_tree)

                        NULL60=self.match(self.input, NULL, self.FOLLOW_NULL_in_variable_declaration489)

                        NULL60_tree = self._adaptor.createWithPayload(NULL60)
                        self._adaptor.addChild(root_0, NULL60_tree)




                    set61 = self.input.LT(1)
                    if (ASSIGN <= self.input.LA(1) <= DEFAULT):
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set61))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse


                    self._state.following.append(self.FOLLOW_expression_in_variable_declaration506)
                    expression62 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression62.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "variable_declaration"

    class constant_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.constant_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "constant_declaration"
    # sql.g:96:1: constant_declaration : ID CONSTANT datatype ( NOT NULL )? ( ASSIGN | DEFAULT ) expression ;
    def constant_declaration(self, ):

        retval = self.constant_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID63 = None
        CONSTANT64 = None
        NOT66 = None
        NULL67 = None
        set68 = None
        datatype65 = None

        expression69 = None


        ID63_tree = None
        CONSTANT64_tree = None
        NOT66_tree = None
        NULL67_tree = None
        set68_tree = None

        try:
            try:
                # sql.g:96:22: ( ID CONSTANT datatype ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )
                # sql.g:97:9: ID CONSTANT datatype ( NOT NULL )? ( ASSIGN | DEFAULT ) expression
                pass 
                root_0 = self._adaptor.nil()

                ID63=self.match(self.input, ID, self.FOLLOW_ID_in_constant_declaration531)

                ID63_tree = self._adaptor.createWithPayload(ID63)
                self._adaptor.addChild(root_0, ID63_tree)

                CONSTANT64=self.match(self.input, CONSTANT, self.FOLLOW_CONSTANT_in_constant_declaration533)

                CONSTANT64_tree = self._adaptor.createWithPayload(CONSTANT64)
                self._adaptor.addChild(root_0, CONSTANT64_tree)

                self._state.following.append(self.FOLLOW_datatype_in_constant_declaration535)
                datatype65 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype65.tree)
                # sql.g:97:30: ( NOT NULL )?
                alt18 = 2
                LA18_0 = self.input.LA(1)

                if (LA18_0 == NOT) :
                    alt18 = 1
                if alt18 == 1:
                    # sql.g:97:32: NOT NULL
                    pass 
                    NOT66=self.match(self.input, NOT, self.FOLLOW_NOT_in_constant_declaration539)

                    NOT66_tree = self._adaptor.createWithPayload(NOT66)
                    self._adaptor.addChild(root_0, NOT66_tree)

                    NULL67=self.match(self.input, NULL, self.FOLLOW_NULL_in_constant_declaration541)

                    NULL67_tree = self._adaptor.createWithPayload(NULL67)
                    self._adaptor.addChild(root_0, NULL67_tree)




                set68 = self.input.LT(1)
                if (ASSIGN <= self.input.LA(1) <= DEFAULT):
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set68))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                self._state.following.append(self.FOLLOW_expression_in_constant_declaration560)
                expression69 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression69.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "constant_declaration"

    class exception_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.exception_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "exception_declaration"
    # sql.g:100:1: exception_declaration : ID EXCEPTION ;
    def exception_declaration(self, ):

        retval = self.exception_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID70 = None
        EXCEPTION71 = None

        ID70_tree = None
        EXCEPTION71_tree = None

        try:
            try:
                # sql.g:100:23: ( ID EXCEPTION )
                # sql.g:101:9: ID EXCEPTION
                pass 
                root_0 = self._adaptor.nil()

                ID70=self.match(self.input, ID, self.FOLLOW_ID_in_exception_declaration581)

                ID70_tree = self._adaptor.createWithPayload(ID70)
                self._adaptor.addChild(root_0, ID70_tree)

                EXCEPTION71=self.match(self.input, EXCEPTION, self.FOLLOW_EXCEPTION_in_exception_declaration583)

                EXCEPTION71_tree = self._adaptor.createWithPayload(EXCEPTION71)
                self._adaptor.addChild(root_0, EXCEPTION71_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "exception_declaration"

    class type_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.type_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "type_definition"
    # sql.g:104:1: type_definition : kTYPE ID IS ( record_type_definition | collection_type_definition | ref_cursor_type_definition ) ;
    def type_definition(self, ):

        retval = self.type_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID73 = None
        IS74 = None
        kTYPE72 = None

        record_type_definition75 = None

        collection_type_definition76 = None

        ref_cursor_type_definition77 = None


        ID73_tree = None
        IS74_tree = None

        try:
            try:
                # sql.g:104:17: ( kTYPE ID IS ( record_type_definition | collection_type_definition | ref_cursor_type_definition ) )
                # sql.g:105:9: kTYPE ID IS ( record_type_definition | collection_type_definition | ref_cursor_type_definition )
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_kTYPE_in_type_definition604)
                kTYPE72 = self.kTYPE()

                self._state.following.pop()
                self._adaptor.addChild(root_0, kTYPE72.tree)
                ID73=self.match(self.input, ID, self.FOLLOW_ID_in_type_definition606)

                ID73_tree = self._adaptor.createWithPayload(ID73)
                self._adaptor.addChild(root_0, ID73_tree)

                IS74=self.match(self.input, IS, self.FOLLOW_IS_in_type_definition608)

                IS74_tree = self._adaptor.createWithPayload(IS74)
                self._adaptor.addChild(root_0, IS74_tree)

                # sql.g:105:21: ( record_type_definition | collection_type_definition | ref_cursor_type_definition )
                alt19 = 3
                LA19 = self.input.LA(1)
                if LA19 == RECORD:
                    alt19 = 1
                elif LA19 == VARYING or LA19 == VARRAY or LA19 == TABLE:
                    alt19 = 2
                elif LA19 == REF:
                    alt19 = 3
                else:
                    nvae = NoViableAltException("", 19, 0, self.input)

                    raise nvae

                if alt19 == 1:
                    # sql.g:105:23: record_type_definition
                    pass 
                    self._state.following.append(self.FOLLOW_record_type_definition_in_type_definition612)
                    record_type_definition75 = self.record_type_definition()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, record_type_definition75.tree)


                elif alt19 == 2:
                    # sql.g:105:48: collection_type_definition
                    pass 
                    self._state.following.append(self.FOLLOW_collection_type_definition_in_type_definition616)
                    collection_type_definition76 = self.collection_type_definition()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, collection_type_definition76.tree)


                elif alt19 == 3:
                    # sql.g:105:77: ref_cursor_type_definition
                    pass 
                    self._state.following.append(self.FOLLOW_ref_cursor_type_definition_in_type_definition620)
                    ref_cursor_type_definition77 = self.ref_cursor_type_definition()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, ref_cursor_type_definition77.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "type_definition"

    class subtype_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.subtype_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "subtype_definition"
    # sql.g:108:1: subtype_definition : SUBTYPE ID IS datatype ( NOT NULL )? ;
    def subtype_definition(self, ):

        retval = self.subtype_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SUBTYPE78 = None
        ID79 = None
        IS80 = None
        NOT82 = None
        NULL83 = None
        datatype81 = None


        SUBTYPE78_tree = None
        ID79_tree = None
        IS80_tree = None
        NOT82_tree = None
        NULL83_tree = None

        try:
            try:
                # sql.g:108:20: ( SUBTYPE ID IS datatype ( NOT NULL )? )
                # sql.g:109:9: SUBTYPE ID IS datatype ( NOT NULL )?
                pass 
                root_0 = self._adaptor.nil()

                SUBTYPE78=self.match(self.input, SUBTYPE, self.FOLLOW_SUBTYPE_in_subtype_definition643)

                SUBTYPE78_tree = self._adaptor.createWithPayload(SUBTYPE78)
                self._adaptor.addChild(root_0, SUBTYPE78_tree)

                ID79=self.match(self.input, ID, self.FOLLOW_ID_in_subtype_definition645)

                ID79_tree = self._adaptor.createWithPayload(ID79)
                self._adaptor.addChild(root_0, ID79_tree)

                IS80=self.match(self.input, IS, self.FOLLOW_IS_in_subtype_definition647)

                IS80_tree = self._adaptor.createWithPayload(IS80)
                self._adaptor.addChild(root_0, IS80_tree)

                self._state.following.append(self.FOLLOW_datatype_in_subtype_definition649)
                datatype81 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype81.tree)
                # sql.g:109:32: ( NOT NULL )?
                alt20 = 2
                LA20_0 = self.input.LA(1)

                if (LA20_0 == NOT) :
                    alt20 = 1
                if alt20 == 1:
                    # sql.g:109:34: NOT NULL
                    pass 
                    NOT82=self.match(self.input, NOT, self.FOLLOW_NOT_in_subtype_definition653)

                    NOT82_tree = self._adaptor.createWithPayload(NOT82)
                    self._adaptor.addChild(root_0, NOT82_tree)

                    NULL83=self.match(self.input, NULL, self.FOLLOW_NULL_in_subtype_definition655)

                    NULL83_tree = self._adaptor.createWithPayload(NULL83)
                    self._adaptor.addChild(root_0, NULL83_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "subtype_definition"

    class record_type_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.record_type_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "record_type_definition"
    # sql.g:112:1: record_type_definition : RECORD LPAREN record_field_declaration ( COMMA record_field_declaration )* RPAREN ;
    def record_type_definition(self, ):

        retval = self.record_type_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RECORD84 = None
        LPAREN85 = None
        COMMA87 = None
        RPAREN89 = None
        record_field_declaration86 = None

        record_field_declaration88 = None


        RECORD84_tree = None
        LPAREN85_tree = None
        COMMA87_tree = None
        RPAREN89_tree = None

        try:
            try:
                # sql.g:112:24: ( RECORD LPAREN record_field_declaration ( COMMA record_field_declaration )* RPAREN )
                # sql.g:113:2: RECORD LPAREN record_field_declaration ( COMMA record_field_declaration )* RPAREN
                pass 
                root_0 = self._adaptor.nil()

                RECORD84=self.match(self.input, RECORD, self.FOLLOW_RECORD_in_record_type_definition676)

                RECORD84_tree = self._adaptor.createWithPayload(RECORD84)
                self._adaptor.addChild(root_0, RECORD84_tree)

                LPAREN85=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_record_type_definition678)

                LPAREN85_tree = self._adaptor.createWithPayload(LPAREN85)
                self._adaptor.addChild(root_0, LPAREN85_tree)

                self._state.following.append(self.FOLLOW_record_field_declaration_in_record_type_definition680)
                record_field_declaration86 = self.record_field_declaration()

                self._state.following.pop()
                self._adaptor.addChild(root_0, record_field_declaration86.tree)
                # sql.g:113:41: ( COMMA record_field_declaration )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == COMMA) :
                        alt21 = 1


                    if alt21 == 1:
                        # sql.g:113:43: COMMA record_field_declaration
                        pass 
                        COMMA87=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_record_type_definition684)

                        COMMA87_tree = self._adaptor.createWithPayload(COMMA87)
                        self._adaptor.addChild(root_0, COMMA87_tree)

                        self._state.following.append(self.FOLLOW_record_field_declaration_in_record_type_definition686)
                        record_field_declaration88 = self.record_field_declaration()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, record_field_declaration88.tree)


                    else:
                        break #loop21
                RPAREN89=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_record_type_definition691)

                RPAREN89_tree = self._adaptor.createWithPayload(RPAREN89)
                self._adaptor.addChild(root_0, RPAREN89_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "record_type_definition"

    class record_field_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.record_field_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "record_field_declaration"
    # sql.g:116:1: record_field_declaration : ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )? ;
    def record_field_declaration(self, ):

        retval = self.record_field_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID90 = None
        NOT92 = None
        NULL93 = None
        set94 = None
        datatype91 = None

        expression95 = None


        ID90_tree = None
        NOT92_tree = None
        NULL93_tree = None
        set94_tree = None

        try:
            try:
                # sql.g:116:26: ( ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )? )
                # sql.g:117:2: ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )?
                pass 
                root_0 = self._adaptor.nil()

                ID90=self.match(self.input, ID, self.FOLLOW_ID_in_record_field_declaration705)

                ID90_tree = self._adaptor.createWithPayload(ID90)
                self._adaptor.addChild(root_0, ID90_tree)

                self._state.following.append(self.FOLLOW_datatype_in_record_field_declaration707)
                datatype91 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype91.tree)
                # sql.g:117:14: ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )?
                alt23 = 2
                LA23_0 = self.input.LA(1)

                if ((ASSIGN <= LA23_0 <= DEFAULT) or LA23_0 == NOT) :
                    alt23 = 1
                if alt23 == 1:
                    # sql.g:117:16: ( NOT NULL )? ( ASSIGN | DEFAULT ) expression
                    pass 
                    # sql.g:117:16: ( NOT NULL )?
                    alt22 = 2
                    LA22_0 = self.input.LA(1)

                    if (LA22_0 == NOT) :
                        alt22 = 1
                    if alt22 == 1:
                        # sql.g:117:18: NOT NULL
                        pass 
                        NOT92=self.match(self.input, NOT, self.FOLLOW_NOT_in_record_field_declaration713)

                        NOT92_tree = self._adaptor.createWithPayload(NOT92)
                        self._adaptor.addChild(root_0, NOT92_tree)

                        NULL93=self.match(self.input, NULL, self.FOLLOW_NULL_in_record_field_declaration715)

                        NULL93_tree = self._adaptor.createWithPayload(NULL93)
                        self._adaptor.addChild(root_0, NULL93_tree)




                    set94 = self.input.LT(1)
                    if (ASSIGN <= self.input.LA(1) <= DEFAULT):
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set94))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse


                    self._state.following.append(self.FOLLOW_expression_in_record_field_declaration730)
                    expression95 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression95.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "record_field_declaration"

    class collection_type_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.collection_type_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "collection_type_definition"
    # sql.g:120:1: collection_type_definition : ( varray_type_definition | nested_table_type_definition );
    def collection_type_definition(self, ):

        retval = self.collection_type_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        varray_type_definition96 = None

        nested_table_type_definition97 = None



        try:
            try:
                # sql.g:121:2: ( varray_type_definition | nested_table_type_definition )
                alt24 = 2
                LA24_0 = self.input.LA(1)

                if (LA24_0 == VARYING or LA24_0 == VARRAY) :
                    alt24 = 1
                elif (LA24_0 == TABLE) :
                    alt24 = 2
                else:
                    nvae = NoViableAltException("", 24, 0, self.input)

                    raise nvae

                if alt24 == 1:
                    # sql.g:121:4: varray_type_definition
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_varray_type_definition_in_collection_type_definition747)
                    varray_type_definition96 = self.varray_type_definition()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, varray_type_definition96.tree)


                elif alt24 == 2:
                    # sql.g:122:4: nested_table_type_definition
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_nested_table_type_definition_in_collection_type_definition752)
                    nested_table_type_definition97 = self.nested_table_type_definition()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, nested_table_type_definition97.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "collection_type_definition"

    class varray_type_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.varray_type_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "varray_type_definition"
    # sql.g:125:1: varray_type_definition : ( VARYING ( ARRAY )? | VARRAY ) LPAREN numeric_literal RPAREN kOF datatype ( NOT NULL )? ;
    def varray_type_definition(self, ):

        retval = self.varray_type_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        VARYING98 = None
        ARRAY99 = None
        VARRAY100 = None
        LPAREN101 = None
        RPAREN103 = None
        NOT106 = None
        NULL107 = None
        numeric_literal102 = None

        kOF104 = None

        datatype105 = None


        VARYING98_tree = None
        ARRAY99_tree = None
        VARRAY100_tree = None
        LPAREN101_tree = None
        RPAREN103_tree = None
        NOT106_tree = None
        NULL107_tree = None

        try:
            try:
                # sql.g:126:2: ( ( VARYING ( ARRAY )? | VARRAY ) LPAREN numeric_literal RPAREN kOF datatype ( NOT NULL )? )
                # sql.g:126:4: ( VARYING ( ARRAY )? | VARRAY ) LPAREN numeric_literal RPAREN kOF datatype ( NOT NULL )?
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:126:4: ( VARYING ( ARRAY )? | VARRAY )
                alt26 = 2
                LA26_0 = self.input.LA(1)

                if (LA26_0 == VARYING) :
                    alt26 = 1
                elif (LA26_0 == VARRAY) :
                    alt26 = 2
                else:
                    nvae = NoViableAltException("", 26, 0, self.input)

                    raise nvae

                if alt26 == 1:
                    # sql.g:126:6: VARYING ( ARRAY )?
                    pass 
                    VARYING98=self.match(self.input, VARYING, self.FOLLOW_VARYING_in_varray_type_definition765)

                    VARYING98_tree = self._adaptor.createWithPayload(VARYING98)
                    self._adaptor.addChild(root_0, VARYING98_tree)

                    # sql.g:126:14: ( ARRAY )?
                    alt25 = 2
                    LA25_0 = self.input.LA(1)

                    if (LA25_0 == ARRAY) :
                        alt25 = 1
                    if alt25 == 1:
                        # sql.g:126:14: ARRAY
                        pass 
                        ARRAY99=self.match(self.input, ARRAY, self.FOLLOW_ARRAY_in_varray_type_definition767)

                        ARRAY99_tree = self._adaptor.createWithPayload(ARRAY99)
                        self._adaptor.addChild(root_0, ARRAY99_tree)






                elif alt26 == 2:
                    # sql.g:126:23: VARRAY
                    pass 
                    VARRAY100=self.match(self.input, VARRAY, self.FOLLOW_VARRAY_in_varray_type_definition772)

                    VARRAY100_tree = self._adaptor.createWithPayload(VARRAY100)
                    self._adaptor.addChild(root_0, VARRAY100_tree)




                LPAREN101=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_varray_type_definition776)

                LPAREN101_tree = self._adaptor.createWithPayload(LPAREN101)
                self._adaptor.addChild(root_0, LPAREN101_tree)

                self._state.following.append(self.FOLLOW_numeric_literal_in_varray_type_definition778)
                numeric_literal102 = self.numeric_literal()

                self._state.following.pop()
                self._adaptor.addChild(root_0, numeric_literal102.tree)
                RPAREN103=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_varray_type_definition780)

                RPAREN103_tree = self._adaptor.createWithPayload(RPAREN103)
                self._adaptor.addChild(root_0, RPAREN103_tree)

                self._state.following.append(self.FOLLOW_kOF_in_varray_type_definition782)
                kOF104 = self.kOF()

                self._state.following.pop()
                self._adaptor.addChild(root_0, kOF104.tree)
                self._state.following.append(self.FOLLOW_datatype_in_varray_type_definition784)
                datatype105 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype105.tree)
                # sql.g:126:75: ( NOT NULL )?
                alt27 = 2
                LA27_0 = self.input.LA(1)

                if (LA27_0 == NOT) :
                    alt27 = 1
                if alt27 == 1:
                    # sql.g:126:77: NOT NULL
                    pass 
                    NOT106=self.match(self.input, NOT, self.FOLLOW_NOT_in_varray_type_definition788)

                    NOT106_tree = self._adaptor.createWithPayload(NOT106)
                    self._adaptor.addChild(root_0, NOT106_tree)

                    NULL107=self.match(self.input, NULL, self.FOLLOW_NULL_in_varray_type_definition790)

                    NULL107_tree = self._adaptor.createWithPayload(NULL107)
                    self._adaptor.addChild(root_0, NULL107_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "varray_type_definition"

    class nested_table_type_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.nested_table_type_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "nested_table_type_definition"
    # sql.g:129:1: nested_table_type_definition : TABLE kOF datatype ( NOT NULL )? ( INDEX BY associative_index_type )? ;
    def nested_table_type_definition(self, ):

        retval = self.nested_table_type_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TABLE108 = None
        NOT111 = None
        NULL112 = None
        INDEX113 = None
        BY114 = None
        kOF109 = None

        datatype110 = None

        associative_index_type115 = None


        TABLE108_tree = None
        NOT111_tree = None
        NULL112_tree = None
        INDEX113_tree = None
        BY114_tree = None

        try:
            try:
                # sql.g:130:2: ( TABLE kOF datatype ( NOT NULL )? ( INDEX BY associative_index_type )? )
                # sql.g:130:4: TABLE kOF datatype ( NOT NULL )? ( INDEX BY associative_index_type )?
                pass 
                root_0 = self._adaptor.nil()

                TABLE108=self.match(self.input, TABLE, self.FOLLOW_TABLE_in_nested_table_type_definition804)

                TABLE108_tree = self._adaptor.createWithPayload(TABLE108)
                self._adaptor.addChild(root_0, TABLE108_tree)

                self._state.following.append(self.FOLLOW_kOF_in_nested_table_type_definition806)
                kOF109 = self.kOF()

                self._state.following.pop()
                self._adaptor.addChild(root_0, kOF109.tree)
                self._state.following.append(self.FOLLOW_datatype_in_nested_table_type_definition808)
                datatype110 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype110.tree)
                # sql.g:130:23: ( NOT NULL )?
                alt28 = 2
                LA28_0 = self.input.LA(1)

                if (LA28_0 == NOT) :
                    alt28 = 1
                if alt28 == 1:
                    # sql.g:130:25: NOT NULL
                    pass 
                    NOT111=self.match(self.input, NOT, self.FOLLOW_NOT_in_nested_table_type_definition812)

                    NOT111_tree = self._adaptor.createWithPayload(NOT111)
                    self._adaptor.addChild(root_0, NOT111_tree)

                    NULL112=self.match(self.input, NULL, self.FOLLOW_NULL_in_nested_table_type_definition814)

                    NULL112_tree = self._adaptor.createWithPayload(NULL112)
                    self._adaptor.addChild(root_0, NULL112_tree)




                # sql.g:130:37: ( INDEX BY associative_index_type )?
                alt29 = 2
                LA29_0 = self.input.LA(1)

                if (LA29_0 == INDEX) :
                    alt29 = 1
                if alt29 == 1:
                    # sql.g:130:39: INDEX BY associative_index_type
                    pass 
                    INDEX113=self.match(self.input, INDEX, self.FOLLOW_INDEX_in_nested_table_type_definition821)

                    INDEX113_tree = self._adaptor.createWithPayload(INDEX113)
                    self._adaptor.addChild(root_0, INDEX113_tree)

                    BY114=self.match(self.input, BY, self.FOLLOW_BY_in_nested_table_type_definition823)

                    BY114_tree = self._adaptor.createWithPayload(BY114)
                    self._adaptor.addChild(root_0, BY114_tree)

                    self._state.following.append(self.FOLLOW_associative_index_type_in_nested_table_type_definition825)
                    associative_index_type115 = self.associative_index_type()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, associative_index_type115.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "nested_table_type_definition"

    class associative_index_type_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.associative_index_type_return, self).__init__()

            self.tree = None




    # $ANTLR start "associative_index_type"
    # sql.g:133:1: associative_index_type : datatype ;
    def associative_index_type(self, ):

        retval = self.associative_index_type_return()
        retval.start = self.input.LT(1)

        root_0 = None

        datatype116 = None



        try:
            try:
                # sql.g:134:2: ( datatype )
                # sql.g:134:4: datatype
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_datatype_in_associative_index_type839)
                datatype116 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype116.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "associative_index_type"

    class ref_cursor_type_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.ref_cursor_type_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "ref_cursor_type_definition"
    # sql.g:137:1: ref_cursor_type_definition : REF CURSOR ( RETURN datatype )? ;
    def ref_cursor_type_definition(self, ):

        retval = self.ref_cursor_type_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        REF117 = None
        CURSOR118 = None
        RETURN119 = None
        datatype120 = None


        REF117_tree = None
        CURSOR118_tree = None
        RETURN119_tree = None

        try:
            try:
                # sql.g:138:2: ( REF CURSOR ( RETURN datatype )? )
                # sql.g:138:4: REF CURSOR ( RETURN datatype )?
                pass 
                root_0 = self._adaptor.nil()

                REF117=self.match(self.input, REF, self.FOLLOW_REF_in_ref_cursor_type_definition850)

                REF117_tree = self._adaptor.createWithPayload(REF117)
                self._adaptor.addChild(root_0, REF117_tree)

                CURSOR118=self.match(self.input, CURSOR, self.FOLLOW_CURSOR_in_ref_cursor_type_definition852)

                CURSOR118_tree = self._adaptor.createWithPayload(CURSOR118)
                self._adaptor.addChild(root_0, CURSOR118_tree)

                # sql.g:138:15: ( RETURN datatype )?
                alt30 = 2
                LA30_0 = self.input.LA(1)

                if (LA30_0 == RETURN) :
                    alt30 = 1
                if alt30 == 1:
                    # sql.g:138:17: RETURN datatype
                    pass 
                    RETURN119=self.match(self.input, RETURN, self.FOLLOW_RETURN_in_ref_cursor_type_definition856)

                    RETURN119_tree = self._adaptor.createWithPayload(RETURN119)
                    self._adaptor.addChild(root_0, RETURN119_tree)

                    self._state.following.append(self.FOLLOW_datatype_in_ref_cursor_type_definition858)
                    datatype120 = self.datatype()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, datatype120.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "ref_cursor_type_definition"

    class datatype_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.datatype_return, self).__init__()

            self.tree = None




    # $ANTLR start "datatype"
    # sql.g:141:1: datatype : ( REF )? ID ( DOT ID )? ( LPAREN numeric_literal ( COMMA numeric_literal )* RPAREN | PERCENT ( kTYPE | ROWTYPE ) )? ;
    def datatype(self, ):

        retval = self.datatype_return()
        retval.start = self.input.LT(1)

        root_0 = None

        REF121 = None
        ID122 = None
        DOT123 = None
        ID124 = None
        LPAREN125 = None
        COMMA127 = None
        RPAREN129 = None
        PERCENT130 = None
        ROWTYPE132 = None
        numeric_literal126 = None

        numeric_literal128 = None

        kTYPE131 = None


        REF121_tree = None
        ID122_tree = None
        DOT123_tree = None
        ID124_tree = None
        LPAREN125_tree = None
        COMMA127_tree = None
        RPAREN129_tree = None
        PERCENT130_tree = None
        ROWTYPE132_tree = None

        try:
            try:
                # sql.g:142:5: ( ( REF )? ID ( DOT ID )? ( LPAREN numeric_literal ( COMMA numeric_literal )* RPAREN | PERCENT ( kTYPE | ROWTYPE ) )? )
                # sql.g:142:7: ( REF )? ID ( DOT ID )? ( LPAREN numeric_literal ( COMMA numeric_literal )* RPAREN | PERCENT ( kTYPE | ROWTYPE ) )?
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:142:7: ( REF )?
                alt31 = 2
                LA31_0 = self.input.LA(1)

                if (LA31_0 == REF) :
                    alt31 = 1
                if alt31 == 1:
                    # sql.g:142:9: REF
                    pass 
                    REF121=self.match(self.input, REF, self.FOLLOW_REF_in_datatype877)

                    REF121_tree = self._adaptor.createWithPayload(REF121)
                    self._adaptor.addChild(root_0, REF121_tree)




                ID122=self.match(self.input, ID, self.FOLLOW_ID_in_datatype882)

                ID122_tree = self._adaptor.createWithPayload(ID122)
                self._adaptor.addChild(root_0, ID122_tree)

                # sql.g:142:19: ( DOT ID )?
                alt32 = 2
                LA32_0 = self.input.LA(1)

                if (LA32_0 == DOT) :
                    alt32 = 1
                if alt32 == 1:
                    # sql.g:142:21: DOT ID
                    pass 
                    DOT123=self.match(self.input, DOT, self.FOLLOW_DOT_in_datatype886)

                    DOT123_tree = self._adaptor.createWithPayload(DOT123)
                    self._adaptor.addChild(root_0, DOT123_tree)

                    ID124=self.match(self.input, ID, self.FOLLOW_ID_in_datatype888)

                    ID124_tree = self._adaptor.createWithPayload(ID124)
                    self._adaptor.addChild(root_0, ID124_tree)




                # sql.g:142:31: ( LPAREN numeric_literal ( COMMA numeric_literal )* RPAREN | PERCENT ( kTYPE | ROWTYPE ) )?
                alt35 = 3
                LA35_0 = self.input.LA(1)

                if (LA35_0 == LPAREN) :
                    alt35 = 1
                elif (LA35_0 == PERCENT) :
                    alt35 = 2
                if alt35 == 1:
                    # sql.g:142:33: LPAREN numeric_literal ( COMMA numeric_literal )* RPAREN
                    pass 
                    LPAREN125=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_datatype895)

                    LPAREN125_tree = self._adaptor.createWithPayload(LPAREN125)
                    self._adaptor.addChild(root_0, LPAREN125_tree)

                    self._state.following.append(self.FOLLOW_numeric_literal_in_datatype897)
                    numeric_literal126 = self.numeric_literal()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, numeric_literal126.tree)
                    # sql.g:142:56: ( COMMA numeric_literal )*
                    while True: #loop33
                        alt33 = 2
                        LA33_0 = self.input.LA(1)

                        if (LA33_0 == COMMA) :
                            alt33 = 1


                        if alt33 == 1:
                            # sql.g:142:58: COMMA numeric_literal
                            pass 
                            COMMA127=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_datatype901)

                            COMMA127_tree = self._adaptor.createWithPayload(COMMA127)
                            self._adaptor.addChild(root_0, COMMA127_tree)

                            self._state.following.append(self.FOLLOW_numeric_literal_in_datatype903)
                            numeric_literal128 = self.numeric_literal()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, numeric_literal128.tree)


                        else:
                            break #loop33
                    RPAREN129=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_datatype908)

                    RPAREN129_tree = self._adaptor.createWithPayload(RPAREN129)
                    self._adaptor.addChild(root_0, RPAREN129_tree)



                elif alt35 == 2:
                    # sql.g:142:92: PERCENT ( kTYPE | ROWTYPE )
                    pass 
                    PERCENT130=self.match(self.input, PERCENT, self.FOLLOW_PERCENT_in_datatype912)

                    PERCENT130_tree = self._adaptor.createWithPayload(PERCENT130)
                    self._adaptor.addChild(root_0, PERCENT130_tree)

                    # sql.g:142:100: ( kTYPE | ROWTYPE )
                    alt34 = 2
                    LA34_0 = self.input.LA(1)

                    if (LA34_0 == ID) :
                        alt34 = 1
                    elif (LA34_0 == ROWTYPE) :
                        alt34 = 2
                    else:
                        nvae = NoViableAltException("", 34, 0, self.input)

                        raise nvae

                    if alt34 == 1:
                        # sql.g:142:102: kTYPE
                        pass 
                        self._state.following.append(self.FOLLOW_kTYPE_in_datatype916)
                        kTYPE131 = self.kTYPE()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, kTYPE131.tree)


                    elif alt34 == 2:
                        # sql.g:142:110: ROWTYPE
                        pass 
                        ROWTYPE132=self.match(self.input, ROWTYPE, self.FOLLOW_ROWTYPE_in_datatype920)

                        ROWTYPE132_tree = self._adaptor.createWithPayload(ROWTYPE132)
                        self._adaptor.addChild(root_0, ROWTYPE132_tree)










                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "datatype"

    class function_declaration_or_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.function_declaration_or_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "function_declaration_or_definition"
    # sql.g:145:1: function_declaration_or_definition : function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ( ( IS | AS ) ( declare_section )? body )? ;
    def function_declaration_or_definition(self, ):

        retval = self.function_declaration_or_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set134 = None
        set135 = None
        function_heading133 = None

        declare_section136 = None

        body137 = None


        set134_tree = None
        set135_tree = None

        try:
            try:
                # sql.g:145:36: ( function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ( ( IS | AS ) ( declare_section )? body )? )
                # sql.g:146:9: function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ( ( IS | AS ) ( declare_section )? body )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_function_heading_in_function_declaration_or_definition946)
                function_heading133 = self.function_heading()

                self._state.following.pop()
                self._adaptor.addChild(root_0, function_heading133.tree)
                # sql.g:147:9: ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if ((DETERMINISTIC <= LA36_0 <= RESULT_CACHE)) :
                        alt36 = 1


                    if alt36 == 1:
                        # sql.g:
                        pass 
                        set134 = self.input.LT(1)
                        if (DETERMINISTIC <= self.input.LA(1) <= RESULT_CACHE):
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set134))
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        break #loop36
                # sql.g:148:9: ( ( IS | AS ) ( declare_section )? body )?
                alt38 = 2
                LA38_0 = self.input.LA(1)

                if (LA38_0 == IS or LA38_0 == AS) :
                    alt38 = 1
                if alt38 == 1:
                    # sql.g:148:11: ( IS | AS ) ( declare_section )? body
                    pass 
                    set135 = self.input.LT(1)
                    if self.input.LA(1) == IS or self.input.LA(1) == AS:
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set135))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse


                    # sql.g:148:23: ( declare_section )?
                    alt37 = 2
                    LA37_0 = self.input.LA(1)

                    if ((PROCEDURE <= LA37_0 <= FUNCTION) or LA37_0 == CURSOR or LA37_0 == SUBTYPE or LA37_0 == PRAGMA) :
                        alt37 = 1
                    if alt37 == 1:
                        # sql.g:148:23: declare_section
                        pass 
                        self._state.following.append(self.FOLLOW_declare_section_in_function_declaration_or_definition995)
                        declare_section136 = self.declare_section()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, declare_section136.tree)



                    self._state.following.append(self.FOLLOW_body_in_function_declaration_or_definition998)
                    body137 = self.body()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, body137.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function_declaration_or_definition"

    class function_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.function_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "function_declaration"
    # sql.g:151:1: function_declaration : function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ;
    def function_declaration(self, ):

        retval = self.function_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set139 = None
        function_heading138 = None


        set139_tree = None

        try:
            try:
                # sql.g:151:22: ( function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* )
                # sql.g:152:9: function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_function_heading_in_function_declaration1019)
                function_heading138 = self.function_heading()

                self._state.following.pop()
                self._adaptor.addChild(root_0, function_heading138.tree)
                # sql.g:153:9: ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
                while True: #loop39
                    alt39 = 2
                    LA39_0 = self.input.LA(1)

                    if ((DETERMINISTIC <= LA39_0 <= RESULT_CACHE)) :
                        alt39 = 1


                    if alt39 == 1:
                        # sql.g:
                        pass 
                        set139 = self.input.LT(1)
                        if (DETERMINISTIC <= self.input.LA(1) <= RESULT_CACHE):
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set139))
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        break #loop39



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function_declaration"

    class function_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.function_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "function_definition"
    # sql.g:156:1: function_definition : function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ( IS | AS ) ( declare_section )? body ;
    def function_definition(self, ):

        retval = self.function_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set141 = None
        set142 = None
        function_heading140 = None

        declare_section143 = None

        body144 = None


        set141_tree = None
        set142_tree = None

        try:
            try:
                # sql.g:156:21: ( function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ( IS | AS ) ( declare_section )? body )
                # sql.g:157:9: function_heading ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )* ( IS | AS ) ( declare_section )? body
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_function_heading_in_function_definition1067)
                function_heading140 = self.function_heading()

                self._state.following.pop()
                self._adaptor.addChild(root_0, function_heading140.tree)
                # sql.g:158:9: ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if ((DETERMINISTIC <= LA40_0 <= RESULT_CACHE)) :
                        alt40 = 1


                    if alt40 == 1:
                        # sql.g:
                        pass 
                        set141 = self.input.LT(1)
                        if (DETERMINISTIC <= self.input.LA(1) <= RESULT_CACHE):
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set141))
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        break #loop40
                set142 = self.input.LT(1)
                if self.input.LA(1) == IS or self.input.LA(1) == AS:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set142))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:159:21: ( declare_section )?
                alt41 = 2
                LA41_0 = self.input.LA(1)

                if ((PROCEDURE <= LA41_0 <= FUNCTION) or LA41_0 == CURSOR or LA41_0 == SUBTYPE or LA41_0 == PRAGMA) :
                    alt41 = 1
                if alt41 == 1:
                    # sql.g:159:21: declare_section
                    pass 
                    self._state.following.append(self.FOLLOW_declare_section_in_function_definition1114)
                    declare_section143 = self.declare_section()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, declare_section143.tree)



                self._state.following.append(self.FOLLOW_body_in_function_definition1117)
                body144 = self.body()

                self._state.following.pop()
                self._adaptor.addChild(root_0, body144.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function_definition"

    class procedure_declaration_or_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.procedure_declaration_or_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "procedure_declaration_or_definition"
    # sql.g:162:1: procedure_declaration_or_definition : procedure_heading ( ( IS | AS ) ( declare_section )? body )? ;
    def procedure_declaration_or_definition(self, ):

        retval = self.procedure_declaration_or_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set146 = None
        procedure_heading145 = None

        declare_section147 = None

        body148 = None


        set146_tree = None

        try:
            try:
                # sql.g:162:37: ( procedure_heading ( ( IS | AS ) ( declare_section )? body )? )
                # sql.g:163:9: procedure_heading ( ( IS | AS ) ( declare_section )? body )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_procedure_heading_in_procedure_declaration_or_definition1135)
                procedure_heading145 = self.procedure_heading()

                self._state.following.pop()
                self._adaptor.addChild(root_0, procedure_heading145.tree)
                # sql.g:164:9: ( ( IS | AS ) ( declare_section )? body )?
                alt43 = 2
                LA43_0 = self.input.LA(1)

                if (LA43_0 == IS or LA43_0 == AS) :
                    alt43 = 1
                if alt43 == 1:
                    # sql.g:164:11: ( IS | AS ) ( declare_section )? body
                    pass 
                    set146 = self.input.LT(1)
                    if self.input.LA(1) == IS or self.input.LA(1) == AS:
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set146))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse


                    # sql.g:164:23: ( declare_section )?
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if ((PROCEDURE <= LA42_0 <= FUNCTION) or LA42_0 == CURSOR or LA42_0 == SUBTYPE or LA42_0 == PRAGMA) :
                        alt42 = 1
                    if alt42 == 1:
                        # sql.g:164:23: declare_section
                        pass 
                        self._state.following.append(self.FOLLOW_declare_section_in_procedure_declaration_or_definition1157)
                        declare_section147 = self.declare_section()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, declare_section147.tree)



                    self._state.following.append(self.FOLLOW_body_in_procedure_declaration_or_definition1160)
                    body148 = self.body()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, body148.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "procedure_declaration_or_definition"

    class procedure_declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.procedure_declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "procedure_declaration"
    # sql.g:167:1: procedure_declaration : procedure_heading ;
    def procedure_declaration(self, ):

        retval = self.procedure_declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        procedure_heading149 = None



        try:
            try:
                # sql.g:167:23: ( procedure_heading )
                # sql.g:168:2: procedure_heading
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_procedure_heading_in_procedure_declaration1177)
                procedure_heading149 = self.procedure_heading()

                self._state.following.pop()
                self._adaptor.addChild(root_0, procedure_heading149.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "procedure_declaration"

    class procedure_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.procedure_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "procedure_definition"
    # sql.g:171:1: procedure_definition : procedure_heading ( IS | AS ) ( declare_section )? body ;
    def procedure_definition(self, ):

        retval = self.procedure_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set151 = None
        procedure_heading150 = None

        declare_section152 = None

        body153 = None


        set151_tree = None

        try:
            try:
                # sql.g:171:22: ( procedure_heading ( IS | AS ) ( declare_section )? body )
                # sql.g:172:2: procedure_heading ( IS | AS ) ( declare_section )? body
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_procedure_heading_in_procedure_definition1188)
                procedure_heading150 = self.procedure_heading()

                self._state.following.pop()
                self._adaptor.addChild(root_0, procedure_heading150.tree)
                set151 = self.input.LT(1)
                if self.input.LA(1) == IS or self.input.LA(1) == AS:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set151))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:173:14: ( declare_section )?
                alt44 = 2
                LA44_0 = self.input.LA(1)

                if ((PROCEDURE <= LA44_0 <= FUNCTION) or LA44_0 == CURSOR or LA44_0 == SUBTYPE or LA44_0 == PRAGMA) :
                    alt44 = 1
                if alt44 == 1:
                    # sql.g:173:14: declare_section
                    pass 
                    self._state.following.append(self.FOLLOW_declare_section_in_procedure_definition1201)
                    declare_section152 = self.declare_section()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, declare_section152.tree)



                self._state.following.append(self.FOLLOW_body_in_procedure_definition1204)
                body153 = self.body()

                self._state.following.pop()
                self._adaptor.addChild(root_0, body153.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "procedure_definition"

    class body_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.body_return, self).__init__()

            self.tree = None




    # $ANTLR start "body"
    # sql.g:176:1: body : BEGIN statement SEMI ( statement SEMI | pragma SEMI )* ( EXCEPTION ( exception_handler )+ )? END ( ID )? ;
    def body(self, ):

        retval = self.body_return()
        retval.start = self.input.LT(1)

        root_0 = None

        BEGIN154 = None
        SEMI156 = None
        SEMI158 = None
        SEMI160 = None
        EXCEPTION161 = None
        END163 = None
        ID164 = None
        statement155 = None

        statement157 = None

        pragma159 = None

        exception_handler162 = None


        BEGIN154_tree = None
        SEMI156_tree = None
        SEMI158_tree = None
        SEMI160_tree = None
        EXCEPTION161_tree = None
        END163_tree = None
        ID164_tree = None

        try:
            try:
                # sql.g:176:7: ( BEGIN statement SEMI ( statement SEMI | pragma SEMI )* ( EXCEPTION ( exception_handler )+ )? END ( ID )? )
                # sql.g:177:2: BEGIN statement SEMI ( statement SEMI | pragma SEMI )* ( EXCEPTION ( exception_handler )+ )? END ( ID )?
                pass 
                root_0 = self._adaptor.nil()

                BEGIN154=self.match(self.input, BEGIN, self.FOLLOW_BEGIN_in_body1218)

                BEGIN154_tree = self._adaptor.createWithPayload(BEGIN154)
                self._adaptor.addChild(root_0, BEGIN154_tree)

                self._state.following.append(self.FOLLOW_statement_in_body1220)
                statement155 = self.statement()

                self._state.following.pop()
                self._adaptor.addChild(root_0, statement155.tree)
                SEMI156=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_body1222)

                SEMI156_tree = self._adaptor.createWithPayload(SEMI156)
                self._adaptor.addChild(root_0, SEMI156_tree)

                # sql.g:177:23: ( statement SEMI | pragma SEMI )*
                while True: #loop45
                    alt45 = 3
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == ID or LA45_0 == RETURN or LA45_0 == NULL or LA45_0 == BEGIN or (COLON <= LA45_0 <= CASE) or (CLOSE <= LA45_0 <= EXECUTE) or (EXIT <= LA45_0 <= FETCH) or (FOR <= LA45_0 <= FORALL) or (GOTO <= LA45_0 <= IF) or LA45_0 == OPEN or (RAISE <= LA45_0 <= LLABEL) or (COMMIT <= LA45_0 <= SET) or (UPDATE <= LA45_0 <= WHILE)) :
                        alt45 = 1
                    elif (LA45_0 == PRAGMA) :
                        alt45 = 2


                    if alt45 == 1:
                        # sql.g:177:25: statement SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_body1226)
                        statement157 = self.statement()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, statement157.tree)
                        SEMI158=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_body1228)

                        SEMI158_tree = self._adaptor.createWithPayload(SEMI158)
                        self._adaptor.addChild(root_0, SEMI158_tree)



                    elif alt45 == 2:
                        # sql.g:177:42: pragma SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_pragma_in_body1232)
                        pragma159 = self.pragma()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, pragma159.tree)
                        SEMI160=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_body1234)

                        SEMI160_tree = self._adaptor.createWithPayload(SEMI160)
                        self._adaptor.addChild(root_0, SEMI160_tree)



                    else:
                        break #loop45
                # sql.g:178:2: ( EXCEPTION ( exception_handler )+ )?
                alt47 = 2
                LA47_0 = self.input.LA(1)

                if (LA47_0 == EXCEPTION) :
                    alt47 = 1
                if alt47 == 1:
                    # sql.g:178:4: EXCEPTION ( exception_handler )+
                    pass 
                    EXCEPTION161=self.match(self.input, EXCEPTION, self.FOLLOW_EXCEPTION_in_body1242)

                    EXCEPTION161_tree = self._adaptor.createWithPayload(EXCEPTION161)
                    self._adaptor.addChild(root_0, EXCEPTION161_tree)

                    # sql.g:178:14: ( exception_handler )+
                    cnt46 = 0
                    while True: #loop46
                        alt46 = 2
                        LA46_0 = self.input.LA(1)

                        if (LA46_0 == WHEN) :
                            alt46 = 1


                        if alt46 == 1:
                            # sql.g:178:14: exception_handler
                            pass 
                            self._state.following.append(self.FOLLOW_exception_handler_in_body1244)
                            exception_handler162 = self.exception_handler()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, exception_handler162.tree)


                        else:
                            if cnt46 >= 1:
                                break #loop46

                            eee = EarlyExitException(46, self.input)
                            raise eee

                        cnt46 += 1



                END163=self.match(self.input, END, self.FOLLOW_END_in_body1250)

                END163_tree = self._adaptor.createWithPayload(END163)
                self._adaptor.addChild(root_0, END163_tree)

                # sql.g:178:40: ( ID )?
                alt48 = 2
                LA48_0 = self.input.LA(1)

                if (LA48_0 == ID) :
                    alt48 = 1
                if alt48 == 1:
                    # sql.g:178:40: ID
                    pass 
                    ID164=self.match(self.input, ID, self.FOLLOW_ID_in_body1252)

                    ID164_tree = self._adaptor.createWithPayload(ID164)
                    self._adaptor.addChild(root_0, ID164_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "body"

    class exception_handler_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.exception_handler_return, self).__init__()

            self.tree = None




    # $ANTLR start "exception_handler"
    # sql.g:181:1: exception_handler : WHEN ( qual_id ( OR qual_id )* | OTHERS ) THEN ( statement SEMI )+ ;
    def exception_handler(self, ):

        retval = self.exception_handler_return()
        retval.start = self.input.LT(1)

        root_0 = None

        WHEN165 = None
        OR167 = None
        OTHERS169 = None
        THEN170 = None
        SEMI172 = None
        qual_id166 = None

        qual_id168 = None

        statement171 = None


        WHEN165_tree = None
        OR167_tree = None
        OTHERS169_tree = None
        THEN170_tree = None
        SEMI172_tree = None

        try:
            try:
                # sql.g:182:2: ( WHEN ( qual_id ( OR qual_id )* | OTHERS ) THEN ( statement SEMI )+ )
                # sql.g:182:4: WHEN ( qual_id ( OR qual_id )* | OTHERS ) THEN ( statement SEMI )+
                pass 
                root_0 = self._adaptor.nil()

                WHEN165=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_exception_handler1264)

                WHEN165_tree = self._adaptor.createWithPayload(WHEN165)
                self._adaptor.addChild(root_0, WHEN165_tree)

                # sql.g:182:9: ( qual_id ( OR qual_id )* | OTHERS )
                alt50 = 2
                LA50_0 = self.input.LA(1)

                if (LA50_0 == ID or LA50_0 == COLON) :
                    alt50 = 1
                elif (LA50_0 == OTHERS) :
                    alt50 = 2
                else:
                    nvae = NoViableAltException("", 50, 0, self.input)

                    raise nvae

                if alt50 == 1:
                    # sql.g:182:11: qual_id ( OR qual_id )*
                    pass 
                    self._state.following.append(self.FOLLOW_qual_id_in_exception_handler1268)
                    qual_id166 = self.qual_id()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, qual_id166.tree)
                    # sql.g:182:19: ( OR qual_id )*
                    while True: #loop49
                        alt49 = 2
                        LA49_0 = self.input.LA(1)

                        if (LA49_0 == OR) :
                            alt49 = 1


                        if alt49 == 1:
                            # sql.g:182:21: OR qual_id
                            pass 
                            OR167=self.match(self.input, OR, self.FOLLOW_OR_in_exception_handler1272)

                            OR167_tree = self._adaptor.createWithPayload(OR167)
                            self._adaptor.addChild(root_0, OR167_tree)

                            self._state.following.append(self.FOLLOW_qual_id_in_exception_handler1274)
                            qual_id168 = self.qual_id()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, qual_id168.tree)


                        else:
                            break #loop49


                elif alt50 == 2:
                    # sql.g:182:37: OTHERS
                    pass 
                    OTHERS169=self.match(self.input, OTHERS, self.FOLLOW_OTHERS_in_exception_handler1281)

                    OTHERS169_tree = self._adaptor.createWithPayload(OTHERS169)
                    self._adaptor.addChild(root_0, OTHERS169_tree)




                THEN170=self.match(self.input, THEN, self.FOLLOW_THEN_in_exception_handler1287)

                THEN170_tree = self._adaptor.createWithPayload(THEN170)
                self._adaptor.addChild(root_0, THEN170_tree)

                # sql.g:183:8: ( statement SEMI )+
                cnt51 = 0
                while True: #loop51
                    alt51 = 2
                    LA51_0 = self.input.LA(1)

                    if (LA51_0 == ID or LA51_0 == RETURN or LA51_0 == NULL or LA51_0 == BEGIN or (COLON <= LA51_0 <= CASE) or (CLOSE <= LA51_0 <= EXECUTE) or (EXIT <= LA51_0 <= FETCH) or (FOR <= LA51_0 <= FORALL) or (GOTO <= LA51_0 <= IF) or LA51_0 == OPEN or (RAISE <= LA51_0 <= LLABEL) or (COMMIT <= LA51_0 <= SET) or (UPDATE <= LA51_0 <= WHILE)) :
                        alt51 = 1


                    if alt51 == 1:
                        # sql.g:183:10: statement SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_exception_handler1291)
                        statement171 = self.statement()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, statement171.tree)
                        SEMI172=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_exception_handler1293)

                        SEMI172_tree = self._adaptor.createWithPayload(SEMI172)
                        self._adaptor.addChild(root_0, SEMI172_tree)



                    else:
                        if cnt51 >= 1:
                            break #loop51

                        eee = EarlyExitException(51, self.input)
                        raise eee

                    cnt51 += 1



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "exception_handler"

    class statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "statement"
    # sql.g:186:1: statement : ( label )* ( assign_or_call_statement | case_statement | close_statement | continue_statement | basic_loop_statement | execute_immediate_statement | exit_statement | fetch_statement | for_loop_statement | forall_statement | goto_statement | if_statement | null_statement | open_statement | plsql_block | raise_statement | return_statement | sql_statement | while_loop_statement ) ;
    def statement(self, ):

        retval = self.statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        label173 = None

        assign_or_call_statement174 = None

        case_statement175 = None

        close_statement176 = None

        continue_statement177 = None

        basic_loop_statement178 = None

        execute_immediate_statement179 = None

        exit_statement180 = None

        fetch_statement181 = None

        for_loop_statement182 = None

        forall_statement183 = None

        goto_statement184 = None

        if_statement185 = None

        null_statement186 = None

        open_statement187 = None

        plsql_block188 = None

        raise_statement189 = None

        return_statement190 = None

        sql_statement191 = None

        while_loop_statement192 = None



        try:
            try:
                # sql.g:186:11: ( ( label )* ( assign_or_call_statement | case_statement | close_statement | continue_statement | basic_loop_statement | execute_immediate_statement | exit_statement | fetch_statement | for_loop_statement | forall_statement | goto_statement | if_statement | null_statement | open_statement | plsql_block | raise_statement | return_statement | sql_statement | while_loop_statement ) )
                # sql.g:187:5: ( label )* ( assign_or_call_statement | case_statement | close_statement | continue_statement | basic_loop_statement | execute_immediate_statement | exit_statement | fetch_statement | for_loop_statement | forall_statement | goto_statement | if_statement | null_statement | open_statement | plsql_block | raise_statement | return_statement | sql_statement | while_loop_statement )
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:187:5: ( label )*
                while True: #loop52
                    alt52 = 2
                    LA52_0 = self.input.LA(1)

                    if (LA52_0 == LLABEL) :
                        alt52 = 1


                    if alt52 == 1:
                        # sql.g:187:5: label
                        pass 
                        self._state.following.append(self.FOLLOW_label_in_statement1311)
                        label173 = self.label()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, label173.tree)


                    else:
                        break #loop52
                # sql.g:188:5: ( assign_or_call_statement | case_statement | close_statement | continue_statement | basic_loop_statement | execute_immediate_statement | exit_statement | fetch_statement | for_loop_statement | forall_statement | goto_statement | if_statement | null_statement | open_statement | plsql_block | raise_statement | return_statement | sql_statement | while_loop_statement )
                alt53 = 19
                LA53 = self.input.LA(1)
                if LA53 == ID or LA53 == COLON:
                    alt53 = 1
                elif LA53 == CASE:
                    alt53 = 2
                elif LA53 == CLOSE:
                    alt53 = 3
                elif LA53 == CONTINUE:
                    alt53 = 4
                elif LA53 == LOOP:
                    alt53 = 5
                elif LA53 == EXECUTE:
                    alt53 = 6
                elif LA53 == EXIT:
                    alt53 = 7
                elif LA53 == FETCH:
                    alt53 = 8
                elif LA53 == FOR:
                    alt53 = 9
                elif LA53 == FORALL:
                    alt53 = 10
                elif LA53 == GOTO:
                    alt53 = 11
                elif LA53 == IF:
                    alt53 = 12
                elif LA53 == NULL:
                    alt53 = 13
                elif LA53 == OPEN:
                    alt53 = 14
                elif LA53 == BEGIN or LA53 == DECLARE:
                    alt53 = 15
                elif LA53 == RAISE:
                    alt53 = 16
                elif LA53 == RETURN:
                    alt53 = 17
                elif LA53 == DELETE or LA53 == COMMIT or LA53 == INSERT or LA53 == LOCK or LA53 == ROLLBACK or LA53 == SAVEPOINT or LA53 == SELECT or LA53 == SET or LA53 == UPDATE:
                    alt53 = 18
                elif LA53 == WHILE:
                    alt53 = 19
                else:
                    nvae = NoViableAltException("", 53, 0, self.input)

                    raise nvae

                if alt53 == 1:
                    # sql.g:188:7: assign_or_call_statement
                    pass 
                    self._state.following.append(self.FOLLOW_assign_or_call_statement_in_statement1320)
                    assign_or_call_statement174 = self.assign_or_call_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, assign_or_call_statement174.tree)


                elif alt53 == 2:
                    # sql.g:189:7: case_statement
                    pass 
                    self._state.following.append(self.FOLLOW_case_statement_in_statement1328)
                    case_statement175 = self.case_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, case_statement175.tree)


                elif alt53 == 3:
                    # sql.g:190:7: close_statement
                    pass 
                    self._state.following.append(self.FOLLOW_close_statement_in_statement1336)
                    close_statement176 = self.close_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, close_statement176.tree)


                elif alt53 == 4:
                    # sql.g:191:7: continue_statement
                    pass 
                    self._state.following.append(self.FOLLOW_continue_statement_in_statement1344)
                    continue_statement177 = self.continue_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, continue_statement177.tree)


                elif alt53 == 5:
                    # sql.g:192:7: basic_loop_statement
                    pass 
                    self._state.following.append(self.FOLLOW_basic_loop_statement_in_statement1352)
                    basic_loop_statement178 = self.basic_loop_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, basic_loop_statement178.tree)


                elif alt53 == 6:
                    # sql.g:193:7: execute_immediate_statement
                    pass 
                    self._state.following.append(self.FOLLOW_execute_immediate_statement_in_statement1360)
                    execute_immediate_statement179 = self.execute_immediate_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, execute_immediate_statement179.tree)


                elif alt53 == 7:
                    # sql.g:194:7: exit_statement
                    pass 
                    self._state.following.append(self.FOLLOW_exit_statement_in_statement1368)
                    exit_statement180 = self.exit_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exit_statement180.tree)


                elif alt53 == 8:
                    # sql.g:195:7: fetch_statement
                    pass 
                    self._state.following.append(self.FOLLOW_fetch_statement_in_statement1376)
                    fetch_statement181 = self.fetch_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, fetch_statement181.tree)


                elif alt53 == 9:
                    # sql.g:196:7: for_loop_statement
                    pass 
                    self._state.following.append(self.FOLLOW_for_loop_statement_in_statement1384)
                    for_loop_statement182 = self.for_loop_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, for_loop_statement182.tree)


                elif alt53 == 10:
                    # sql.g:197:7: forall_statement
                    pass 
                    self._state.following.append(self.FOLLOW_forall_statement_in_statement1392)
                    forall_statement183 = self.forall_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, forall_statement183.tree)


                elif alt53 == 11:
                    # sql.g:198:7: goto_statement
                    pass 
                    self._state.following.append(self.FOLLOW_goto_statement_in_statement1400)
                    goto_statement184 = self.goto_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, goto_statement184.tree)


                elif alt53 == 12:
                    # sql.g:199:7: if_statement
                    pass 
                    self._state.following.append(self.FOLLOW_if_statement_in_statement1408)
                    if_statement185 = self.if_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, if_statement185.tree)


                elif alt53 == 13:
                    # sql.g:200:7: null_statement
                    pass 
                    self._state.following.append(self.FOLLOW_null_statement_in_statement1416)
                    null_statement186 = self.null_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, null_statement186.tree)


                elif alt53 == 14:
                    # sql.g:201:7: open_statement
                    pass 
                    self._state.following.append(self.FOLLOW_open_statement_in_statement1424)
                    open_statement187 = self.open_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, open_statement187.tree)


                elif alt53 == 15:
                    # sql.g:202:7: plsql_block
                    pass 
                    self._state.following.append(self.FOLLOW_plsql_block_in_statement1432)
                    plsql_block188 = self.plsql_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, plsql_block188.tree)


                elif alt53 == 16:
                    # sql.g:203:7: raise_statement
                    pass 
                    self._state.following.append(self.FOLLOW_raise_statement_in_statement1440)
                    raise_statement189 = self.raise_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, raise_statement189.tree)


                elif alt53 == 17:
                    # sql.g:204:7: return_statement
                    pass 
                    self._state.following.append(self.FOLLOW_return_statement_in_statement1448)
                    return_statement190 = self.return_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, return_statement190.tree)


                elif alt53 == 18:
                    # sql.g:205:7: sql_statement
                    pass 
                    self._state.following.append(self.FOLLOW_sql_statement_in_statement1456)
                    sql_statement191 = self.sql_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, sql_statement191.tree)


                elif alt53 == 19:
                    # sql.g:206:7: while_loop_statement
                    pass 
                    self._state.following.append(self.FOLLOW_while_loop_statement_in_statement1464)
                    while_loop_statement192 = self.while_loop_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, while_loop_statement192.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "statement"

    class lvalue_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.lvalue_return, self).__init__()

            self.tree = None




    # $ANTLR start "lvalue"
    # sql.g:210:1: lvalue : call ( DOT call )* ;
    def lvalue(self, ):

        retval = self.lvalue_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DOT194 = None
        call193 = None

        call195 = None


        DOT194_tree = None

        try:
            try:
                # sql.g:211:5: ( call ( DOT call )* )
                # sql.g:211:7: call ( DOT call )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_call_in_lvalue1487)
                call193 = self.call()

                self._state.following.pop()
                self._adaptor.addChild(root_0, call193.tree)
                # sql.g:211:12: ( DOT call )*
                while True: #loop54
                    alt54 = 2
                    LA54_0 = self.input.LA(1)

                    if (LA54_0 == DOT) :
                        LA54_1 = self.input.LA(2)

                        if (LA54_1 == ID or LA54_1 == COLON) :
                            alt54 = 1




                    if alt54 == 1:
                        # sql.g:211:14: DOT call
                        pass 
                        DOT194=self.match(self.input, DOT, self.FOLLOW_DOT_in_lvalue1491)

                        DOT194_tree = self._adaptor.createWithPayload(DOT194)
                        self._adaptor.addChild(root_0, DOT194_tree)

                        self._state.following.append(self.FOLLOW_call_in_lvalue1493)
                        call195 = self.call()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, call195.tree)


                    else:
                        break #loop54



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "lvalue"

    class assign_or_call_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.assign_or_call_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "assign_or_call_statement"
    # sql.g:214:1: assign_or_call_statement : lvalue ( DOT delete_call | ASSIGN expression )? ;
    def assign_or_call_statement(self, ):

        retval = self.assign_or_call_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DOT197 = None
        ASSIGN199 = None
        lvalue196 = None

        delete_call198 = None

        expression200 = None


        DOT197_tree = None
        ASSIGN199_tree = None

        try:
            try:
                # sql.g:215:5: ( lvalue ( DOT delete_call | ASSIGN expression )? )
                # sql.g:215:7: lvalue ( DOT delete_call | ASSIGN expression )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_lvalue_in_assign_or_call_statement1513)
                lvalue196 = self.lvalue()

                self._state.following.pop()
                self._adaptor.addChild(root_0, lvalue196.tree)
                # sql.g:215:14: ( DOT delete_call | ASSIGN expression )?
                alt55 = 3
                LA55_0 = self.input.LA(1)

                if (LA55_0 == DOT) :
                    alt55 = 1
                elif (LA55_0 == ASSIGN) :
                    alt55 = 2
                if alt55 == 1:
                    # sql.g:215:16: DOT delete_call
                    pass 
                    DOT197=self.match(self.input, DOT, self.FOLLOW_DOT_in_assign_or_call_statement1517)

                    DOT197_tree = self._adaptor.createWithPayload(DOT197)
                    self._adaptor.addChild(root_0, DOT197_tree)

                    self._state.following.append(self.FOLLOW_delete_call_in_assign_or_call_statement1519)
                    delete_call198 = self.delete_call()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, delete_call198.tree)


                elif alt55 == 2:
                    # sql.g:215:34: ASSIGN expression
                    pass 
                    ASSIGN199=self.match(self.input, ASSIGN, self.FOLLOW_ASSIGN_in_assign_or_call_statement1523)

                    ASSIGN199_tree = self._adaptor.createWithPayload(ASSIGN199)
                    self._adaptor.addChild(root_0, ASSIGN199_tree)

                    self._state.following.append(self.FOLLOW_expression_in_assign_or_call_statement1525)
                    expression200 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression200.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "assign_or_call_statement"

    class call_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.call_return, self).__init__()

            self.tree = None




    # $ANTLR start "call"
    # sql.g:218:1: call : ( COLON )? ID ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN )? ;
    def call(self, ):

        retval = self.call_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COLON201 = None
        ID202 = None
        LPAREN203 = None
        COMMA205 = None
        RPAREN207 = None
        parameter204 = None

        parameter206 = None


        COLON201_tree = None
        ID202_tree = None
        LPAREN203_tree = None
        COMMA205_tree = None
        RPAREN207_tree = None

        try:
            try:
                # sql.g:219:5: ( ( COLON )? ID ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN )? )
                # sql.g:219:7: ( COLON )? ID ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN )?
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:219:7: ( COLON )?
                alt56 = 2
                LA56_0 = self.input.LA(1)

                if (LA56_0 == COLON) :
                    alt56 = 1
                if alt56 == 1:
                    # sql.g:219:7: COLON
                    pass 
                    COLON201=self.match(self.input, COLON, self.FOLLOW_COLON_in_call1545)

                    COLON201_tree = self._adaptor.createWithPayload(COLON201)
                    self._adaptor.addChild(root_0, COLON201_tree)




                ID202=self.match(self.input, ID, self.FOLLOW_ID_in_call1548)

                ID202_tree = self._adaptor.createWithPayload(ID202)
                self._adaptor.addChild(root_0, ID202_tree)

                # sql.g:219:17: ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN )?
                alt59 = 2
                LA59_0 = self.input.LA(1)

                if (LA59_0 == LPAREN) :
                    alt59 = 1
                if alt59 == 1:
                    # sql.g:219:19: LPAREN ( parameter ( COMMA parameter )* )? RPAREN
                    pass 
                    LPAREN203=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_call1552)

                    LPAREN203_tree = self._adaptor.createWithPayload(LPAREN203)
                    self._adaptor.addChild(root_0, LPAREN203_tree)

                    # sql.g:219:26: ( parameter ( COMMA parameter )* )?
                    alt58 = 2
                    LA58_0 = self.input.LA(1)

                    if (LA58_0 == ID or LA58_0 == LPAREN or (NOT <= LA58_0 <= NULL) or LA58_0 == COLON or (MINUS <= LA58_0 <= PLUS) or LA58_0 == SQL or (INTEGER <= LA58_0 <= QUOTED_STRING) or (INSERTING <= LA58_0 <= DELETING)) :
                        alt58 = 1
                    if alt58 == 1:
                        # sql.g:219:28: parameter ( COMMA parameter )*
                        pass 
                        self._state.following.append(self.FOLLOW_parameter_in_call1556)
                        parameter204 = self.parameter()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, parameter204.tree)
                        # sql.g:219:38: ( COMMA parameter )*
                        while True: #loop57
                            alt57 = 2
                            LA57_0 = self.input.LA(1)

                            if (LA57_0 == COMMA) :
                                alt57 = 1


                            if alt57 == 1:
                                # sql.g:219:40: COMMA parameter
                                pass 
                                COMMA205=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_call1560)

                                COMMA205_tree = self._adaptor.createWithPayload(COMMA205)
                                self._adaptor.addChild(root_0, COMMA205_tree)

                                self._state.following.append(self.FOLLOW_parameter_in_call1562)
                                parameter206 = self.parameter()

                                self._state.following.pop()
                                self._adaptor.addChild(root_0, parameter206.tree)


                            else:
                                break #loop57



                    RPAREN207=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_call1570)

                    RPAREN207_tree = self._adaptor.createWithPayload(RPAREN207)
                    self._adaptor.addChild(root_0, RPAREN207_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "call"

    class delete_call_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.delete_call_return, self).__init__()

            self.tree = None




    # $ANTLR start "delete_call"
    # sql.g:222:1: delete_call : DELETE ( LPAREN ( parameter )? RPAREN )? ;
    def delete_call(self, ):

        retval = self.delete_call_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DELETE208 = None
        LPAREN209 = None
        RPAREN211 = None
        parameter210 = None


        DELETE208_tree = None
        LPAREN209_tree = None
        RPAREN211_tree = None

        try:
            try:
                # sql.g:223:5: ( DELETE ( LPAREN ( parameter )? RPAREN )? )
                # sql.g:223:7: DELETE ( LPAREN ( parameter )? RPAREN )?
                pass 
                root_0 = self._adaptor.nil()

                DELETE208=self.match(self.input, DELETE, self.FOLLOW_DELETE_in_delete_call1590)

                DELETE208_tree = self._adaptor.createWithPayload(DELETE208)
                self._adaptor.addChild(root_0, DELETE208_tree)

                # sql.g:223:14: ( LPAREN ( parameter )? RPAREN )?
                alt61 = 2
                LA61_0 = self.input.LA(1)

                if (LA61_0 == LPAREN) :
                    alt61 = 1
                if alt61 == 1:
                    # sql.g:223:16: LPAREN ( parameter )? RPAREN
                    pass 
                    LPAREN209=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_delete_call1594)

                    LPAREN209_tree = self._adaptor.createWithPayload(LPAREN209)
                    self._adaptor.addChild(root_0, LPAREN209_tree)

                    # sql.g:223:23: ( parameter )?
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if (LA60_0 == ID or LA60_0 == LPAREN or (NOT <= LA60_0 <= NULL) or LA60_0 == COLON or (MINUS <= LA60_0 <= PLUS) or LA60_0 == SQL or (INTEGER <= LA60_0 <= QUOTED_STRING) or (INSERTING <= LA60_0 <= DELETING)) :
                        alt60 = 1
                    if alt60 == 1:
                        # sql.g:223:23: parameter
                        pass 
                        self._state.following.append(self.FOLLOW_parameter_in_delete_call1596)
                        parameter210 = self.parameter()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, parameter210.tree)



                    RPAREN211=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_delete_call1599)

                    RPAREN211_tree = self._adaptor.createWithPayload(RPAREN211)
                    self._adaptor.addChild(root_0, RPAREN211_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "delete_call"

    class basic_loop_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.basic_loop_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "basic_loop_statement"
    # sql.g:226:1: basic_loop_statement : LOOP ( statement SEMI )+ END LOOP ( label_name )? ;
    def basic_loop_statement(self, ):

        retval = self.basic_loop_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LOOP212 = None
        SEMI214 = None
        END215 = None
        LOOP216 = None
        statement213 = None

        label_name217 = None


        LOOP212_tree = None
        SEMI214_tree = None
        END215_tree = None
        LOOP216_tree = None

        try:
            try:
                # sql.g:226:22: ( LOOP ( statement SEMI )+ END LOOP ( label_name )? )
                # sql.g:227:9: LOOP ( statement SEMI )+ END LOOP ( label_name )?
                pass 
                root_0 = self._adaptor.nil()

                LOOP212=self.match(self.input, LOOP, self.FOLLOW_LOOP_in_basic_loop_statement1623)

                LOOP212_tree = self._adaptor.createWithPayload(LOOP212)
                self._adaptor.addChild(root_0, LOOP212_tree)

                # sql.g:227:14: ( statement SEMI )+
                cnt62 = 0
                while True: #loop62
                    alt62 = 2
                    LA62_0 = self.input.LA(1)

                    if (LA62_0 == ID or LA62_0 == RETURN or LA62_0 == NULL or LA62_0 == BEGIN or (COLON <= LA62_0 <= CASE) or (CLOSE <= LA62_0 <= EXECUTE) or (EXIT <= LA62_0 <= FETCH) or (FOR <= LA62_0 <= FORALL) or (GOTO <= LA62_0 <= IF) or LA62_0 == OPEN or (RAISE <= LA62_0 <= LLABEL) or (COMMIT <= LA62_0 <= SET) or (UPDATE <= LA62_0 <= WHILE)) :
                        alt62 = 1


                    if alt62 == 1:
                        # sql.g:227:16: statement SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_basic_loop_statement1627)
                        statement213 = self.statement()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, statement213.tree)
                        SEMI214=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_basic_loop_statement1629)

                        SEMI214_tree = self._adaptor.createWithPayload(SEMI214)
                        self._adaptor.addChild(root_0, SEMI214_tree)



                    else:
                        if cnt62 >= 1:
                            break #loop62

                        eee = EarlyExitException(62, self.input)
                        raise eee

                    cnt62 += 1
                END215=self.match(self.input, END, self.FOLLOW_END_in_basic_loop_statement1634)

                END215_tree = self._adaptor.createWithPayload(END215)
                self._adaptor.addChild(root_0, END215_tree)

                LOOP216=self.match(self.input, LOOP, self.FOLLOW_LOOP_in_basic_loop_statement1636)

                LOOP216_tree = self._adaptor.createWithPayload(LOOP216)
                self._adaptor.addChild(root_0, LOOP216_tree)

                # sql.g:227:43: ( label_name )?
                alt63 = 2
                LA63_0 = self.input.LA(1)

                if (LA63_0 == ID) :
                    alt63 = 1
                if alt63 == 1:
                    # sql.g:227:43: label_name
                    pass 
                    self._state.following.append(self.FOLLOW_label_name_in_basic_loop_statement1638)
                    label_name217 = self.label_name()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, label_name217.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "basic_loop_statement"

    class case_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.case_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "case_statement"
    # sql.g:230:1: case_statement : CASE ( expression )? ( WHEN expression THEN ( statement SEMI )+ )+ ( ELSE statement SEMI )? END CASE ( label_name )? ;
    def case_statement(self, ):

        retval = self.case_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        CASE218 = None
        WHEN220 = None
        THEN222 = None
        SEMI224 = None
        ELSE225 = None
        SEMI227 = None
        END228 = None
        CASE229 = None
        expression219 = None

        expression221 = None

        statement223 = None

        statement226 = None

        label_name230 = None


        CASE218_tree = None
        WHEN220_tree = None
        THEN222_tree = None
        SEMI224_tree = None
        ELSE225_tree = None
        SEMI227_tree = None
        END228_tree = None
        CASE229_tree = None

        try:
            try:
                # sql.g:230:16: ( CASE ( expression )? ( WHEN expression THEN ( statement SEMI )+ )+ ( ELSE statement SEMI )? END CASE ( label_name )? )
                # sql.g:231:9: CASE ( expression )? ( WHEN expression THEN ( statement SEMI )+ )+ ( ELSE statement SEMI )? END CASE ( label_name )?
                pass 
                root_0 = self._adaptor.nil()

                CASE218=self.match(self.input, CASE, self.FOLLOW_CASE_in_case_statement1660)

                CASE218_tree = self._adaptor.createWithPayload(CASE218)
                self._adaptor.addChild(root_0, CASE218_tree)

                # sql.g:231:14: ( expression )?
                alt64 = 2
                LA64_0 = self.input.LA(1)

                if (LA64_0 == ID or LA64_0 == LPAREN or (NOT <= LA64_0 <= NULL) or LA64_0 == COLON or (MINUS <= LA64_0 <= PLUS) or LA64_0 == SQL or (INTEGER <= LA64_0 <= QUOTED_STRING) or (INSERTING <= LA64_0 <= DELETING)) :
                    alt64 = 1
                if alt64 == 1:
                    # sql.g:231:14: expression
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_case_statement1662)
                    expression219 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression219.tree)



                # sql.g:232:9: ( WHEN expression THEN ( statement SEMI )+ )+
                cnt66 = 0
                while True: #loop66
                    alt66 = 2
                    LA66_0 = self.input.LA(1)

                    if (LA66_0 == WHEN) :
                        alt66 = 1


                    if alt66 == 1:
                        # sql.g:232:11: WHEN expression THEN ( statement SEMI )+
                        pass 
                        WHEN220=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_case_statement1675)

                        WHEN220_tree = self._adaptor.createWithPayload(WHEN220)
                        self._adaptor.addChild(root_0, WHEN220_tree)

                        self._state.following.append(self.FOLLOW_expression_in_case_statement1677)
                        expression221 = self.expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, expression221.tree)
                        THEN222=self.match(self.input, THEN, self.FOLLOW_THEN_in_case_statement1679)

                        THEN222_tree = self._adaptor.createWithPayload(THEN222)
                        self._adaptor.addChild(root_0, THEN222_tree)

                        # sql.g:232:32: ( statement SEMI )+
                        cnt65 = 0
                        while True: #loop65
                            alt65 = 2
                            LA65_0 = self.input.LA(1)

                            if (LA65_0 == ID or LA65_0 == RETURN or LA65_0 == NULL or LA65_0 == BEGIN or (COLON <= LA65_0 <= CASE) or (CLOSE <= LA65_0 <= EXECUTE) or (EXIT <= LA65_0 <= FETCH) or (FOR <= LA65_0 <= FORALL) or (GOTO <= LA65_0 <= IF) or LA65_0 == OPEN or (RAISE <= LA65_0 <= LLABEL) or (COMMIT <= LA65_0 <= SET) or (UPDATE <= LA65_0 <= WHILE)) :
                                alt65 = 1


                            if alt65 == 1:
                                # sql.g:232:34: statement SEMI
                                pass 
                                self._state.following.append(self.FOLLOW_statement_in_case_statement1683)
                                statement223 = self.statement()

                                self._state.following.pop()
                                self._adaptor.addChild(root_0, statement223.tree)
                                SEMI224=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_case_statement1685)

                                SEMI224_tree = self._adaptor.createWithPayload(SEMI224)
                                self._adaptor.addChild(root_0, SEMI224_tree)



                            else:
                                if cnt65 >= 1:
                                    break #loop65

                                eee = EarlyExitException(65, self.input)
                                raise eee

                            cnt65 += 1


                    else:
                        if cnt66 >= 1:
                            break #loop66

                        eee = EarlyExitException(66, self.input)
                        raise eee

                    cnt66 += 1
                # sql.g:233:9: ( ELSE statement SEMI )?
                alt67 = 2
                LA67_0 = self.input.LA(1)

                if (LA67_0 == ELSE) :
                    alt67 = 1
                if alt67 == 1:
                    # sql.g:233:11: ELSE statement SEMI
                    pass 
                    ELSE225=self.match(self.input, ELSE, self.FOLLOW_ELSE_in_case_statement1703)

                    ELSE225_tree = self._adaptor.createWithPayload(ELSE225)
                    self._adaptor.addChild(root_0, ELSE225_tree)

                    self._state.following.append(self.FOLLOW_statement_in_case_statement1705)
                    statement226 = self.statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, statement226.tree)
                    SEMI227=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_case_statement1707)

                    SEMI227_tree = self._adaptor.createWithPayload(SEMI227)
                    self._adaptor.addChild(root_0, SEMI227_tree)




                END228=self.match(self.input, END, self.FOLLOW_END_in_case_statement1720)

                END228_tree = self._adaptor.createWithPayload(END228)
                self._adaptor.addChild(root_0, END228_tree)

                CASE229=self.match(self.input, CASE, self.FOLLOW_CASE_in_case_statement1722)

                CASE229_tree = self._adaptor.createWithPayload(CASE229)
                self._adaptor.addChild(root_0, CASE229_tree)

                # sql.g:234:18: ( label_name )?
                alt68 = 2
                LA68_0 = self.input.LA(1)

                if (LA68_0 == ID) :
                    alt68 = 1
                if alt68 == 1:
                    # sql.g:234:18: label_name
                    pass 
                    self._state.following.append(self.FOLLOW_label_name_in_case_statement1724)
                    label_name230 = self.label_name()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, label_name230.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "case_statement"

    class close_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.close_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "close_statement"
    # sql.g:237:1: close_statement : CLOSE ID ( DOT ID )? ;
    def close_statement(self, ):

        retval = self.close_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        CLOSE231 = None
        ID232 = None
        DOT233 = None
        ID234 = None

        CLOSE231_tree = None
        ID232_tree = None
        DOT233_tree = None
        ID234_tree = None

        try:
            try:
                # sql.g:237:17: ( CLOSE ID ( DOT ID )? )
                # sql.g:238:9: CLOSE ID ( DOT ID )?
                pass 
                root_0 = self._adaptor.nil()

                CLOSE231=self.match(self.input, CLOSE, self.FOLLOW_CLOSE_in_close_statement1746)

                CLOSE231_tree = self._adaptor.createWithPayload(CLOSE231)
                self._adaptor.addChild(root_0, CLOSE231_tree)

                ID232=self.match(self.input, ID, self.FOLLOW_ID_in_close_statement1748)

                ID232_tree = self._adaptor.createWithPayload(ID232)
                self._adaptor.addChild(root_0, ID232_tree)

                # sql.g:238:18: ( DOT ID )?
                alt69 = 2
                LA69_0 = self.input.LA(1)

                if (LA69_0 == DOT) :
                    alt69 = 1
                if alt69 == 1:
                    # sql.g:238:20: DOT ID
                    pass 
                    DOT233=self.match(self.input, DOT, self.FOLLOW_DOT_in_close_statement1752)

                    DOT233_tree = self._adaptor.createWithPayload(DOT233)
                    self._adaptor.addChild(root_0, DOT233_tree)

                    ID234=self.match(self.input, ID, self.FOLLOW_ID_in_close_statement1754)

                    ID234_tree = self._adaptor.createWithPayload(ID234)
                    self._adaptor.addChild(root_0, ID234_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "close_statement"

    class continue_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.continue_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "continue_statement"
    # sql.g:241:1: continue_statement : CONTINUE (lbl= ID )? ( WHEN expression )? ;
    def continue_statement(self, ):

        retval = self.continue_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        lbl = None
        CONTINUE235 = None
        WHEN236 = None
        expression237 = None


        lbl_tree = None
        CONTINUE235_tree = None
        WHEN236_tree = None

        try:
            try:
                # sql.g:241:20: ( CONTINUE (lbl= ID )? ( WHEN expression )? )
                # sql.g:242:9: CONTINUE (lbl= ID )? ( WHEN expression )?
                pass 
                root_0 = self._adaptor.nil()

                CONTINUE235=self.match(self.input, CONTINUE, self.FOLLOW_CONTINUE_in_continue_statement1778)

                CONTINUE235_tree = self._adaptor.createWithPayload(CONTINUE235)
                self._adaptor.addChild(root_0, CONTINUE235_tree)

                # sql.g:242:18: (lbl= ID )?
                alt70 = 2
                LA70_0 = self.input.LA(1)

                if (LA70_0 == ID) :
                    alt70 = 1
                if alt70 == 1:
                    # sql.g:242:20: lbl= ID
                    pass 
                    lbl=self.match(self.input, ID, self.FOLLOW_ID_in_continue_statement1784)

                    lbl_tree = self._adaptor.createWithPayload(lbl)
                    self._adaptor.addChild(root_0, lbl_tree)




                # sql.g:242:30: ( WHEN expression )?
                alt71 = 2
                LA71_0 = self.input.LA(1)

                if (LA71_0 == WHEN) :
                    alt71 = 1
                if alt71 == 1:
                    # sql.g:242:32: WHEN expression
                    pass 
                    WHEN236=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_continue_statement1791)

                    WHEN236_tree = self._adaptor.createWithPayload(WHEN236)
                    self._adaptor.addChild(root_0, WHEN236_tree)

                    self._state.following.append(self.FOLLOW_expression_in_continue_statement1793)
                    expression237 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression237.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "continue_statement"

    class execute_immediate_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.execute_immediate_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "execute_immediate_statement"
    # sql.g:245:1: execute_immediate_statement : EXECUTE IMMEDIATE expression ( ( into_clause | bulk_collect_into_clause ) ( using_clause )? | using_clause ( dynamic_returning_clause )? | dynamic_returning_clause )? ;
    def execute_immediate_statement(self, ):

        retval = self.execute_immediate_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        EXECUTE238 = None
        IMMEDIATE239 = None
        expression240 = None

        into_clause241 = None

        bulk_collect_into_clause242 = None

        using_clause243 = None

        using_clause244 = None

        dynamic_returning_clause245 = None

        dynamic_returning_clause246 = None


        EXECUTE238_tree = None
        IMMEDIATE239_tree = None

        try:
            try:
                # sql.g:245:29: ( EXECUTE IMMEDIATE expression ( ( into_clause | bulk_collect_into_clause ) ( using_clause )? | using_clause ( dynamic_returning_clause )? | dynamic_returning_clause )? )
                # sql.g:246:9: EXECUTE IMMEDIATE expression ( ( into_clause | bulk_collect_into_clause ) ( using_clause )? | using_clause ( dynamic_returning_clause )? | dynamic_returning_clause )?
                pass 
                root_0 = self._adaptor.nil()

                EXECUTE238=self.match(self.input, EXECUTE, self.FOLLOW_EXECUTE_in_execute_immediate_statement1817)

                EXECUTE238_tree = self._adaptor.createWithPayload(EXECUTE238)
                self._adaptor.addChild(root_0, EXECUTE238_tree)

                IMMEDIATE239=self.match(self.input, IMMEDIATE, self.FOLLOW_IMMEDIATE_in_execute_immediate_statement1819)

                IMMEDIATE239_tree = self._adaptor.createWithPayload(IMMEDIATE239)
                self._adaptor.addChild(root_0, IMMEDIATE239_tree)

                self._state.following.append(self.FOLLOW_expression_in_execute_immediate_statement1821)
                expression240 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression240.tree)
                # sql.g:246:38: ( ( into_clause | bulk_collect_into_clause ) ( using_clause )? | using_clause ( dynamic_returning_clause )? | dynamic_returning_clause )?
                alt75 = 4
                LA75 = self.input.LA(1)
                if LA75 == INTO or LA75 == BULK:
                    alt75 = 1
                elif LA75 == USING:
                    alt75 = 2
                elif LA75 == RETURN or LA75 == RETURNING:
                    alt75 = 3
                if alt75 == 1:
                    # sql.g:247:9: ( into_clause | bulk_collect_into_clause ) ( using_clause )?
                    pass 
                    # sql.g:247:9: ( into_clause | bulk_collect_into_clause )
                    alt72 = 2
                    LA72_0 = self.input.LA(1)

                    if (LA72_0 == INTO) :
                        alt72 = 1
                    elif (LA72_0 == BULK) :
                        alt72 = 2
                    else:
                        nvae = NoViableAltException("", 72, 0, self.input)

                        raise nvae

                    if alt72 == 1:
                        # sql.g:247:11: into_clause
                        pass 
                        self._state.following.append(self.FOLLOW_into_clause_in_execute_immediate_statement1835)
                        into_clause241 = self.into_clause()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, into_clause241.tree)


                    elif alt72 == 2:
                        # sql.g:247:25: bulk_collect_into_clause
                        pass 
                        self._state.following.append(self.FOLLOW_bulk_collect_into_clause_in_execute_immediate_statement1839)
                        bulk_collect_into_clause242 = self.bulk_collect_into_clause()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, bulk_collect_into_clause242.tree)



                    # sql.g:247:51: ( using_clause )?
                    alt73 = 2
                    LA73_0 = self.input.LA(1)

                    if (LA73_0 == USING) :
                        alt73 = 1
                    if alt73 == 1:
                        # sql.g:247:51: using_clause
                        pass 
                        self._state.following.append(self.FOLLOW_using_clause_in_execute_immediate_statement1842)
                        using_clause243 = self.using_clause()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, using_clause243.tree)





                elif alt75 == 2:
                    # sql.g:248:11: using_clause ( dynamic_returning_clause )?
                    pass 
                    self._state.following.append(self.FOLLOW_using_clause_in_execute_immediate_statement1855)
                    using_clause244 = self.using_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, using_clause244.tree)
                    # sql.g:248:24: ( dynamic_returning_clause )?
                    alt74 = 2
                    LA74_0 = self.input.LA(1)

                    if (LA74_0 == RETURN or LA74_0 == RETURNING) :
                        alt74 = 1
                    if alt74 == 1:
                        # sql.g:248:24: dynamic_returning_clause
                        pass 
                        self._state.following.append(self.FOLLOW_dynamic_returning_clause_in_execute_immediate_statement1857)
                        dynamic_returning_clause245 = self.dynamic_returning_clause()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, dynamic_returning_clause245.tree)





                elif alt75 == 3:
                    # sql.g:249:11: dynamic_returning_clause
                    pass 
                    self._state.following.append(self.FOLLOW_dynamic_returning_clause_in_execute_immediate_statement1870)
                    dynamic_returning_clause246 = self.dynamic_returning_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, dynamic_returning_clause246.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "execute_immediate_statement"

    class exit_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.exit_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "exit_statement"
    # sql.g:253:1: exit_statement : EXIT (lbl= ID )? ( WHEN expression )? ;
    def exit_statement(self, ):

        retval = self.exit_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        lbl = None
        EXIT247 = None
        WHEN248 = None
        expression249 = None


        lbl_tree = None
        EXIT247_tree = None
        WHEN248_tree = None

        try:
            try:
                # sql.g:253:16: ( EXIT (lbl= ID )? ( WHEN expression )? )
                # sql.g:254:9: EXIT (lbl= ID )? ( WHEN expression )?
                pass 
                root_0 = self._adaptor.nil()

                EXIT247=self.match(self.input, EXIT, self.FOLLOW_EXIT_in_exit_statement1902)

                EXIT247_tree = self._adaptor.createWithPayload(EXIT247)
                self._adaptor.addChild(root_0, EXIT247_tree)

                # sql.g:254:14: (lbl= ID )?
                alt76 = 2
                LA76_0 = self.input.LA(1)

                if (LA76_0 == ID) :
                    alt76 = 1
                if alt76 == 1:
                    # sql.g:254:16: lbl= ID
                    pass 
                    lbl=self.match(self.input, ID, self.FOLLOW_ID_in_exit_statement1908)

                    lbl_tree = self._adaptor.createWithPayload(lbl)
                    self._adaptor.addChild(root_0, lbl_tree)




                # sql.g:254:26: ( WHEN expression )?
                alt77 = 2
                LA77_0 = self.input.LA(1)

                if (LA77_0 == WHEN) :
                    alt77 = 1
                if alt77 == 1:
                    # sql.g:254:28: WHEN expression
                    pass 
                    WHEN248=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_exit_statement1915)

                    WHEN248_tree = self._adaptor.createWithPayload(WHEN248)
                    self._adaptor.addChild(root_0, WHEN248_tree)

                    self._state.following.append(self.FOLLOW_expression_in_exit_statement1917)
                    expression249 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression249.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "exit_statement"

    class fetch_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.fetch_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "fetch_statement"
    # sql.g:257:1: fetch_statement : FETCH qual_id ( into_clause | bulk_collect_into_clause ( LIMIT numeric_expression )? ) ;
    def fetch_statement(self, ):

        retval = self.fetch_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FETCH250 = None
        LIMIT254 = None
        qual_id251 = None

        into_clause252 = None

        bulk_collect_into_clause253 = None

        numeric_expression255 = None


        FETCH250_tree = None
        LIMIT254_tree = None

        try:
            try:
                # sql.g:257:17: ( FETCH qual_id ( into_clause | bulk_collect_into_clause ( LIMIT numeric_expression )? ) )
                # sql.g:258:9: FETCH qual_id ( into_clause | bulk_collect_into_clause ( LIMIT numeric_expression )? )
                pass 
                root_0 = self._adaptor.nil()

                FETCH250=self.match(self.input, FETCH, self.FOLLOW_FETCH_in_fetch_statement1941)

                FETCH250_tree = self._adaptor.createWithPayload(FETCH250)
                self._adaptor.addChild(root_0, FETCH250_tree)

                self._state.following.append(self.FOLLOW_qual_id_in_fetch_statement1943)
                qual_id251 = self.qual_id()

                self._state.following.pop()
                self._adaptor.addChild(root_0, qual_id251.tree)
                # sql.g:258:23: ( into_clause | bulk_collect_into_clause ( LIMIT numeric_expression )? )
                alt79 = 2
                LA79_0 = self.input.LA(1)

                if (LA79_0 == INTO) :
                    alt79 = 1
                elif (LA79_0 == BULK) :
                    alt79 = 2
                else:
                    nvae = NoViableAltException("", 79, 0, self.input)

                    raise nvae

                if alt79 == 1:
                    # sql.g:258:25: into_clause
                    pass 
                    self._state.following.append(self.FOLLOW_into_clause_in_fetch_statement1947)
                    into_clause252 = self.into_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, into_clause252.tree)


                elif alt79 == 2:
                    # sql.g:258:39: bulk_collect_into_clause ( LIMIT numeric_expression )?
                    pass 
                    self._state.following.append(self.FOLLOW_bulk_collect_into_clause_in_fetch_statement1951)
                    bulk_collect_into_clause253 = self.bulk_collect_into_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, bulk_collect_into_clause253.tree)
                    # sql.g:258:64: ( LIMIT numeric_expression )?
                    alt78 = 2
                    LA78_0 = self.input.LA(1)

                    if (LA78_0 == LIMIT) :
                        alt78 = 1
                    if alt78 == 1:
                        # sql.g:258:66: LIMIT numeric_expression
                        pass 
                        LIMIT254=self.match(self.input, LIMIT, self.FOLLOW_LIMIT_in_fetch_statement1955)

                        LIMIT254_tree = self._adaptor.createWithPayload(LIMIT254)
                        self._adaptor.addChild(root_0, LIMIT254_tree)

                        self._state.following.append(self.FOLLOW_numeric_expression_in_fetch_statement1957)
                        numeric_expression255 = self.numeric_expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, numeric_expression255.tree)









                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fetch_statement"

    class into_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.into_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "into_clause"
    # sql.g:261:1: into_clause : INTO lvalue ( COMMA lvalue )* ;
    def into_clause(self, ):

        retval = self.into_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        INTO256 = None
        COMMA258 = None
        lvalue257 = None

        lvalue259 = None


        INTO256_tree = None
        COMMA258_tree = None

        try:
            try:
                # sql.g:261:13: ( INTO lvalue ( COMMA lvalue )* )
                # sql.g:262:9: INTO lvalue ( COMMA lvalue )*
                pass 
                root_0 = self._adaptor.nil()

                INTO256=self.match(self.input, INTO, self.FOLLOW_INTO_in_into_clause1987)

                INTO256_tree = self._adaptor.createWithPayload(INTO256)
                self._adaptor.addChild(root_0, INTO256_tree)

                self._state.following.append(self.FOLLOW_lvalue_in_into_clause1989)
                lvalue257 = self.lvalue()

                self._state.following.pop()
                self._adaptor.addChild(root_0, lvalue257.tree)
                # sql.g:262:21: ( COMMA lvalue )*
                while True: #loop80
                    alt80 = 2
                    LA80_0 = self.input.LA(1)

                    if (LA80_0 == COMMA) :
                        alt80 = 1


                    if alt80 == 1:
                        # sql.g:262:23: COMMA lvalue
                        pass 
                        COMMA258=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_into_clause1993)

                        COMMA258_tree = self._adaptor.createWithPayload(COMMA258)
                        self._adaptor.addChild(root_0, COMMA258_tree)

                        self._state.following.append(self.FOLLOW_lvalue_in_into_clause1995)
                        lvalue259 = self.lvalue()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, lvalue259.tree)


                    else:
                        break #loop80



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "into_clause"

    class bulk_collect_into_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.bulk_collect_into_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "bulk_collect_into_clause"
    # sql.g:265:1: bulk_collect_into_clause : BULK COLLECT INTO lvalue ( COMMA lvalue )* ;
    def bulk_collect_into_clause(self, ):

        retval = self.bulk_collect_into_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        BULK260 = None
        COLLECT261 = None
        INTO262 = None
        COMMA264 = None
        lvalue263 = None

        lvalue265 = None


        BULK260_tree = None
        COLLECT261_tree = None
        INTO262_tree = None
        COMMA264_tree = None

        try:
            try:
                # sql.g:265:26: ( BULK COLLECT INTO lvalue ( COMMA lvalue )* )
                # sql.g:266:9: BULK COLLECT INTO lvalue ( COMMA lvalue )*
                pass 
                root_0 = self._adaptor.nil()

                BULK260=self.match(self.input, BULK, self.FOLLOW_BULK_in_bulk_collect_into_clause2023)

                BULK260_tree = self._adaptor.createWithPayload(BULK260)
                self._adaptor.addChild(root_0, BULK260_tree)

                COLLECT261=self.match(self.input, COLLECT, self.FOLLOW_COLLECT_in_bulk_collect_into_clause2025)

                COLLECT261_tree = self._adaptor.createWithPayload(COLLECT261)
                self._adaptor.addChild(root_0, COLLECT261_tree)

                INTO262=self.match(self.input, INTO, self.FOLLOW_INTO_in_bulk_collect_into_clause2027)

                INTO262_tree = self._adaptor.createWithPayload(INTO262)
                self._adaptor.addChild(root_0, INTO262_tree)

                self._state.following.append(self.FOLLOW_lvalue_in_bulk_collect_into_clause2029)
                lvalue263 = self.lvalue()

                self._state.following.pop()
                self._adaptor.addChild(root_0, lvalue263.tree)
                # sql.g:266:34: ( COMMA lvalue )*
                while True: #loop81
                    alt81 = 2
                    LA81_0 = self.input.LA(1)

                    if (LA81_0 == COMMA) :
                        alt81 = 1


                    if alt81 == 1:
                        # sql.g:266:36: COMMA lvalue
                        pass 
                        COMMA264=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_bulk_collect_into_clause2033)

                        COMMA264_tree = self._adaptor.createWithPayload(COMMA264)
                        self._adaptor.addChild(root_0, COMMA264_tree)

                        self._state.following.append(self.FOLLOW_lvalue_in_bulk_collect_into_clause2035)
                        lvalue265 = self.lvalue()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, lvalue265.tree)


                    else:
                        break #loop81



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "bulk_collect_into_clause"

    class using_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.using_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "using_clause"
    # sql.g:269:1: using_clause : USING ( param_modifiers )? expression ( COMMA ( param_modifiers )? expression )* ;
    def using_clause(self, ):

        retval = self.using_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        USING266 = None
        COMMA269 = None
        param_modifiers267 = None

        expression268 = None

        param_modifiers270 = None

        expression271 = None


        USING266_tree = None
        COMMA269_tree = None

        try:
            try:
                # sql.g:269:14: ( USING ( param_modifiers )? expression ( COMMA ( param_modifiers )? expression )* )
                # sql.g:270:9: USING ( param_modifiers )? expression ( COMMA ( param_modifiers )? expression )*
                pass 
                root_0 = self._adaptor.nil()

                USING266=self.match(self.input, USING, self.FOLLOW_USING_in_using_clause2059)

                USING266_tree = self._adaptor.createWithPayload(USING266)
                self._adaptor.addChild(root_0, USING266_tree)

                # sql.g:270:15: ( param_modifiers )?
                alt82 = 2
                LA82_0 = self.input.LA(1)

                if ((IN <= LA82_0 <= OUT)) :
                    alt82 = 1
                if alt82 == 1:
                    # sql.g:270:15: param_modifiers
                    pass 
                    self._state.following.append(self.FOLLOW_param_modifiers_in_using_clause2061)
                    param_modifiers267 = self.param_modifiers()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, param_modifiers267.tree)



                self._state.following.append(self.FOLLOW_expression_in_using_clause2064)
                expression268 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression268.tree)
                # sql.g:270:43: ( COMMA ( param_modifiers )? expression )*
                while True: #loop84
                    alt84 = 2
                    LA84_0 = self.input.LA(1)

                    if (LA84_0 == COMMA) :
                        alt84 = 1


                    if alt84 == 1:
                        # sql.g:270:45: COMMA ( param_modifiers )? expression
                        pass 
                        COMMA269=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_using_clause2068)

                        COMMA269_tree = self._adaptor.createWithPayload(COMMA269)
                        self._adaptor.addChild(root_0, COMMA269_tree)

                        # sql.g:270:51: ( param_modifiers )?
                        alt83 = 2
                        LA83_0 = self.input.LA(1)

                        if ((IN <= LA83_0 <= OUT)) :
                            alt83 = 1
                        if alt83 == 1:
                            # sql.g:270:51: param_modifiers
                            pass 
                            self._state.following.append(self.FOLLOW_param_modifiers_in_using_clause2070)
                            param_modifiers270 = self.param_modifiers()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, param_modifiers270.tree)



                        self._state.following.append(self.FOLLOW_expression_in_using_clause2073)
                        expression271 = self.expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, expression271.tree)


                    else:
                        break #loop84



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "using_clause"

    class param_modifiers_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.param_modifiers_return, self).__init__()

            self.tree = None




    # $ANTLR start "param_modifiers"
    # sql.g:273:1: param_modifiers : ( IN ( OUT )? | OUT );
    def param_modifiers(self, ):

        retval = self.param_modifiers_return()
        retval.start = self.input.LT(1)

        root_0 = None

        IN272 = None
        OUT273 = None
        OUT274 = None

        IN272_tree = None
        OUT273_tree = None
        OUT274_tree = None

        try:
            try:
                # sql.g:274:2: ( IN ( OUT )? | OUT )
                alt86 = 2
                LA86_0 = self.input.LA(1)

                if (LA86_0 == IN) :
                    alt86 = 1
                elif (LA86_0 == OUT) :
                    alt86 = 2
                else:
                    nvae = NoViableAltException("", 86, 0, self.input)

                    raise nvae

                if alt86 == 1:
                    # sql.g:274:4: IN ( OUT )?
                    pass 
                    root_0 = self._adaptor.nil()

                    IN272=self.match(self.input, IN, self.FOLLOW_IN_in_param_modifiers2090)

                    IN272_tree = self._adaptor.createWithPayload(IN272)
                    self._adaptor.addChild(root_0, IN272_tree)

                    # sql.g:274:7: ( OUT )?
                    alt85 = 2
                    LA85_0 = self.input.LA(1)

                    if (LA85_0 == OUT) :
                        alt85 = 1
                    if alt85 == 1:
                        # sql.g:274:7: OUT
                        pass 
                        OUT273=self.match(self.input, OUT, self.FOLLOW_OUT_in_param_modifiers2092)

                        OUT273_tree = self._adaptor.createWithPayload(OUT273)
                        self._adaptor.addChild(root_0, OUT273_tree)






                elif alt86 == 2:
                    # sql.g:274:14: OUT
                    pass 
                    root_0 = self._adaptor.nil()

                    OUT274=self.match(self.input, OUT, self.FOLLOW_OUT_in_param_modifiers2097)

                    OUT274_tree = self._adaptor.createWithPayload(OUT274)
                    self._adaptor.addChild(root_0, OUT274_tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "param_modifiers"

    class dynamic_returning_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.dynamic_returning_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "dynamic_returning_clause"
    # sql.g:277:1: dynamic_returning_clause : ( RETURNING | RETURN ) ( into_clause | bulk_collect_into_clause ) ;
    def dynamic_returning_clause(self, ):

        retval = self.dynamic_returning_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set275 = None
        into_clause276 = None

        bulk_collect_into_clause277 = None


        set275_tree = None

        try:
            try:
                # sql.g:277:26: ( ( RETURNING | RETURN ) ( into_clause | bulk_collect_into_clause ) )
                # sql.g:278:9: ( RETURNING | RETURN ) ( into_clause | bulk_collect_into_clause )
                pass 
                root_0 = self._adaptor.nil()

                set275 = self.input.LT(1)
                if self.input.LA(1) == RETURN or self.input.LA(1) == RETURNING:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set275))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:278:32: ( into_clause | bulk_collect_into_clause )
                alt87 = 2
                LA87_0 = self.input.LA(1)

                if (LA87_0 == INTO) :
                    alt87 = 1
                elif (LA87_0 == BULK) :
                    alt87 = 2
                else:
                    nvae = NoViableAltException("", 87, 0, self.input)

                    raise nvae

                if alt87 == 1:
                    # sql.g:278:34: into_clause
                    pass 
                    self._state.following.append(self.FOLLOW_into_clause_in_dynamic_returning_clause2127)
                    into_clause276 = self.into_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, into_clause276.tree)


                elif alt87 == 2:
                    # sql.g:278:48: bulk_collect_into_clause
                    pass 
                    self._state.following.append(self.FOLLOW_bulk_collect_into_clause_in_dynamic_returning_clause2131)
                    bulk_collect_into_clause277 = self.bulk_collect_into_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, bulk_collect_into_clause277.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "dynamic_returning_clause"

    class for_loop_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.for_loop_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "for_loop_statement"
    # sql.g:281:1: for_loop_statement : FOR ID IN (~ ( LOOP ) )+ LOOP ( statement SEMI )+ END LOOP ( label_name )? ;
    def for_loop_statement(self, ):

        retval = self.for_loop_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FOR278 = None
        ID279 = None
        IN280 = None
        set281 = None
        LOOP282 = None
        SEMI284 = None
        END285 = None
        LOOP286 = None
        statement283 = None

        label_name287 = None


        FOR278_tree = None
        ID279_tree = None
        IN280_tree = None
        set281_tree = None
        LOOP282_tree = None
        SEMI284_tree = None
        END285_tree = None
        LOOP286_tree = None

        try:
            try:
                # sql.g:281:20: ( FOR ID IN (~ ( LOOP ) )+ LOOP ( statement SEMI )+ END LOOP ( label_name )? )
                # sql.g:282:9: FOR ID IN (~ ( LOOP ) )+ LOOP ( statement SEMI )+ END LOOP ( label_name )?
                pass 
                root_0 = self._adaptor.nil()

                FOR278=self.match(self.input, FOR, self.FOLLOW_FOR_in_for_loop_statement2154)

                FOR278_tree = self._adaptor.createWithPayload(FOR278)
                self._adaptor.addChild(root_0, FOR278_tree)

                ID279=self.match(self.input, ID, self.FOLLOW_ID_in_for_loop_statement2156)

                ID279_tree = self._adaptor.createWithPayload(ID279)
                self._adaptor.addChild(root_0, ID279_tree)

                IN280=self.match(self.input, IN, self.FOLLOW_IN_in_for_loop_statement2158)

                IN280_tree = self._adaptor.createWithPayload(IN280)
                self._adaptor.addChild(root_0, IN280_tree)

                # sql.g:282:19: (~ ( LOOP ) )+
                cnt88 = 0
                while True: #loop88
                    alt88 = 2
                    LA88_0 = self.input.LA(1)

                    if ((DIVIDE <= LA88_0 <= DELETE) or (CASE <= LA88_0 <= ML_COMMENT)) :
                        alt88 = 1


                    if alt88 == 1:
                        # sql.g:282:21: ~ ( LOOP )
                        pass 
                        set281 = self.input.LT(1)
                        if (DIVIDE <= self.input.LA(1) <= DELETE) or (CASE <= self.input.LA(1) <= ML_COMMENT):
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set281))
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        if cnt88 >= 1:
                            break #loop88

                        eee = EarlyExitException(88, self.input)
                        raise eee

                    cnt88 += 1
                LOOP282=self.match(self.input, LOOP, self.FOLLOW_LOOP_in_for_loop_statement2170)

                LOOP282_tree = self._adaptor.createWithPayload(LOOP282)
                self._adaptor.addChild(root_0, LOOP282_tree)

                # sql.g:282:37: ( statement SEMI )+
                cnt89 = 0
                while True: #loop89
                    alt89 = 2
                    LA89_0 = self.input.LA(1)

                    if (LA89_0 == ID or LA89_0 == RETURN or LA89_0 == NULL or LA89_0 == BEGIN or (COLON <= LA89_0 <= CASE) or (CLOSE <= LA89_0 <= EXECUTE) or (EXIT <= LA89_0 <= FETCH) or (FOR <= LA89_0 <= FORALL) or (GOTO <= LA89_0 <= IF) or LA89_0 == OPEN or (RAISE <= LA89_0 <= LLABEL) or (COMMIT <= LA89_0 <= SET) or (UPDATE <= LA89_0 <= WHILE)) :
                        alt89 = 1


                    if alt89 == 1:
                        # sql.g:282:39: statement SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_for_loop_statement2174)
                        statement283 = self.statement()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, statement283.tree)
                        SEMI284=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_for_loop_statement2176)

                        SEMI284_tree = self._adaptor.createWithPayload(SEMI284)
                        self._adaptor.addChild(root_0, SEMI284_tree)



                    else:
                        if cnt89 >= 1:
                            break #loop89

                        eee = EarlyExitException(89, self.input)
                        raise eee

                    cnt89 += 1
                END285=self.match(self.input, END, self.FOLLOW_END_in_for_loop_statement2181)

                END285_tree = self._adaptor.createWithPayload(END285)
                self._adaptor.addChild(root_0, END285_tree)

                LOOP286=self.match(self.input, LOOP, self.FOLLOW_LOOP_in_for_loop_statement2183)

                LOOP286_tree = self._adaptor.createWithPayload(LOOP286)
                self._adaptor.addChild(root_0, LOOP286_tree)

                # sql.g:282:66: ( label_name )?
                alt90 = 2
                LA90_0 = self.input.LA(1)

                if (LA90_0 == ID) :
                    alt90 = 1
                if alt90 == 1:
                    # sql.g:282:66: label_name
                    pass 
                    self._state.following.append(self.FOLLOW_label_name_in_for_loop_statement2185)
                    label_name287 = self.label_name()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, label_name287.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "for_loop_statement"

    class forall_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.forall_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "forall_statement"
    # sql.g:285:1: forall_statement : FORALL ID IN bounds_clause sql_statement ( kSAVE kEXCEPTIONS )? ;
    def forall_statement(self, ):

        retval = self.forall_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FORALL288 = None
        ID289 = None
        IN290 = None
        bounds_clause291 = None

        sql_statement292 = None

        kSAVE293 = None

        kEXCEPTIONS294 = None


        FORALL288_tree = None
        ID289_tree = None
        IN290_tree = None

        try:
            try:
                # sql.g:285:18: ( FORALL ID IN bounds_clause sql_statement ( kSAVE kEXCEPTIONS )? )
                # sql.g:286:9: FORALL ID IN bounds_clause sql_statement ( kSAVE kEXCEPTIONS )?
                pass 
                root_0 = self._adaptor.nil()

                FORALL288=self.match(self.input, FORALL, self.FOLLOW_FORALL_in_forall_statement2207)

                FORALL288_tree = self._adaptor.createWithPayload(FORALL288)
                self._adaptor.addChild(root_0, FORALL288_tree)

                ID289=self.match(self.input, ID, self.FOLLOW_ID_in_forall_statement2209)

                ID289_tree = self._adaptor.createWithPayload(ID289)
                self._adaptor.addChild(root_0, ID289_tree)

                IN290=self.match(self.input, IN, self.FOLLOW_IN_in_forall_statement2211)

                IN290_tree = self._adaptor.createWithPayload(IN290)
                self._adaptor.addChild(root_0, IN290_tree)

                self._state.following.append(self.FOLLOW_bounds_clause_in_forall_statement2213)
                bounds_clause291 = self.bounds_clause()

                self._state.following.pop()
                self._adaptor.addChild(root_0, bounds_clause291.tree)
                self._state.following.append(self.FOLLOW_sql_statement_in_forall_statement2215)
                sql_statement292 = self.sql_statement()

                self._state.following.pop()
                self._adaptor.addChild(root_0, sql_statement292.tree)
                # sql.g:286:50: ( kSAVE kEXCEPTIONS )?
                alt91 = 2
                LA91_0 = self.input.LA(1)

                if (LA91_0 == ID) :
                    alt91 = 1
                if alt91 == 1:
                    # sql.g:286:52: kSAVE kEXCEPTIONS
                    pass 
                    self._state.following.append(self.FOLLOW_kSAVE_in_forall_statement2219)
                    kSAVE293 = self.kSAVE()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kSAVE293.tree)
                    self._state.following.append(self.FOLLOW_kEXCEPTIONS_in_forall_statement2221)
                    kEXCEPTIONS294 = self.kEXCEPTIONS()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kEXCEPTIONS294.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "forall_statement"

    class bounds_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.bounds_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "bounds_clause"
    # sql.g:289:1: bounds_clause : ( numeric_expression DOUBLEDOT numeric_expression | kINDICES kOF atom ( BETWEEN numeric_expression AND numeric_expression )? | kVALUES kOF atom );
    def bounds_clause(self, ):

        retval = self.bounds_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DOUBLEDOT296 = None
        BETWEEN301 = None
        AND303 = None
        numeric_expression295 = None

        numeric_expression297 = None

        kINDICES298 = None

        kOF299 = None

        atom300 = None

        numeric_expression302 = None

        numeric_expression304 = None

        kVALUES305 = None

        kOF306 = None

        atom307 = None


        DOUBLEDOT296_tree = None
        BETWEEN301_tree = None
        AND303_tree = None

        try:
            try:
                # sql.g:290:5: ( numeric_expression DOUBLEDOT numeric_expression | kINDICES kOF atom ( BETWEEN numeric_expression AND numeric_expression )? | kVALUES kOF atom )
                alt93 = 3
                alt93 = self.dfa93.predict(self.input)
                if alt93 == 1:
                    # sql.g:290:7: numeric_expression DOUBLEDOT numeric_expression
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_numeric_expression_in_bounds_clause2243)
                    numeric_expression295 = self.numeric_expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, numeric_expression295.tree)
                    DOUBLEDOT296=self.match(self.input, DOUBLEDOT, self.FOLLOW_DOUBLEDOT_in_bounds_clause2245)

                    DOUBLEDOT296_tree = self._adaptor.createWithPayload(DOUBLEDOT296)
                    self._adaptor.addChild(root_0, DOUBLEDOT296_tree)

                    self._state.following.append(self.FOLLOW_numeric_expression_in_bounds_clause2247)
                    numeric_expression297 = self.numeric_expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, numeric_expression297.tree)


                elif alt93 == 2:
                    # sql.g:291:7: kINDICES kOF atom ( BETWEEN numeric_expression AND numeric_expression )?
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_kINDICES_in_bounds_clause2255)
                    kINDICES298 = self.kINDICES()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kINDICES298.tree)
                    self._state.following.append(self.FOLLOW_kOF_in_bounds_clause2257)
                    kOF299 = self.kOF()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kOF299.tree)
                    self._state.following.append(self.FOLLOW_atom_in_bounds_clause2259)
                    atom300 = self.atom()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, atom300.tree)
                    # sql.g:291:25: ( BETWEEN numeric_expression AND numeric_expression )?
                    alt92 = 2
                    LA92_0 = self.input.LA(1)

                    if (LA92_0 == BETWEEN) :
                        alt92 = 1
                    if alt92 == 1:
                        # sql.g:291:27: BETWEEN numeric_expression AND numeric_expression
                        pass 
                        BETWEEN301=self.match(self.input, BETWEEN, self.FOLLOW_BETWEEN_in_bounds_clause2263)

                        BETWEEN301_tree = self._adaptor.createWithPayload(BETWEEN301)
                        self._adaptor.addChild(root_0, BETWEEN301_tree)

                        self._state.following.append(self.FOLLOW_numeric_expression_in_bounds_clause2265)
                        numeric_expression302 = self.numeric_expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, numeric_expression302.tree)
                        AND303=self.match(self.input, AND, self.FOLLOW_AND_in_bounds_clause2267)

                        AND303_tree = self._adaptor.createWithPayload(AND303)
                        self._adaptor.addChild(root_0, AND303_tree)

                        self._state.following.append(self.FOLLOW_numeric_expression_in_bounds_clause2269)
                        numeric_expression304 = self.numeric_expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, numeric_expression304.tree)





                elif alt93 == 3:
                    # sql.g:292:7: kVALUES kOF atom
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_kVALUES_in_bounds_clause2280)
                    kVALUES305 = self.kVALUES()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kVALUES305.tree)
                    self._state.following.append(self.FOLLOW_kOF_in_bounds_clause2282)
                    kOF306 = self.kOF()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kOF306.tree)
                    self._state.following.append(self.FOLLOW_atom_in_bounds_clause2284)
                    atom307 = self.atom()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, atom307.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "bounds_clause"

    class goto_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.goto_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "goto_statement"
    # sql.g:295:1: goto_statement : GOTO label_name ;
    def goto_statement(self, ):

        retval = self.goto_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        GOTO308 = None
        label_name309 = None


        GOTO308_tree = None

        try:
            try:
                # sql.g:295:16: ( GOTO label_name )
                # sql.g:296:9: GOTO label_name
                pass 
                root_0 = self._adaptor.nil()

                GOTO308=self.match(self.input, GOTO, self.FOLLOW_GOTO_in_goto_statement2305)

                GOTO308_tree = self._adaptor.createWithPayload(GOTO308)
                self._adaptor.addChild(root_0, GOTO308_tree)

                self._state.following.append(self.FOLLOW_label_name_in_goto_statement2307)
                label_name309 = self.label_name()

                self._state.following.pop()
                self._adaptor.addChild(root_0, label_name309.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "goto_statement"

    class if_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.if_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "if_statement"
    # sql.g:299:1: if_statement : IF expression THEN ( statement SEMI )+ ( ELSIF expression THEN ( statement SEMI )+ )* ( ELSE ( statement SEMI )+ )? END IF ;
    def if_statement(self, ):

        retval = self.if_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        IF310 = None
        THEN312 = None
        SEMI314 = None
        ELSIF315 = None
        THEN317 = None
        SEMI319 = None
        ELSE320 = None
        SEMI322 = None
        END323 = None
        IF324 = None
        expression311 = None

        statement313 = None

        expression316 = None

        statement318 = None

        statement321 = None


        IF310_tree = None
        THEN312_tree = None
        SEMI314_tree = None
        ELSIF315_tree = None
        THEN317_tree = None
        SEMI319_tree = None
        ELSE320_tree = None
        SEMI322_tree = None
        END323_tree = None
        IF324_tree = None

        try:
            try:
                # sql.g:299:14: ( IF expression THEN ( statement SEMI )+ ( ELSIF expression THEN ( statement SEMI )+ )* ( ELSE ( statement SEMI )+ )? END IF )
                # sql.g:300:9: IF expression THEN ( statement SEMI )+ ( ELSIF expression THEN ( statement SEMI )+ )* ( ELSE ( statement SEMI )+ )? END IF
                pass 
                root_0 = self._adaptor.nil()

                IF310=self.match(self.input, IF, self.FOLLOW_IF_in_if_statement2328)

                IF310_tree = self._adaptor.createWithPayload(IF310)
                self._adaptor.addChild(root_0, IF310_tree)

                self._state.following.append(self.FOLLOW_expression_in_if_statement2330)
                expression311 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression311.tree)
                THEN312=self.match(self.input, THEN, self.FOLLOW_THEN_in_if_statement2332)

                THEN312_tree = self._adaptor.createWithPayload(THEN312)
                self._adaptor.addChild(root_0, THEN312_tree)

                # sql.g:300:28: ( statement SEMI )+
                cnt94 = 0
                while True: #loop94
                    alt94 = 2
                    LA94_0 = self.input.LA(1)

                    if (LA94_0 == ID or LA94_0 == RETURN or LA94_0 == NULL or LA94_0 == BEGIN or (COLON <= LA94_0 <= CASE) or (CLOSE <= LA94_0 <= EXECUTE) or (EXIT <= LA94_0 <= FETCH) or (FOR <= LA94_0 <= FORALL) or (GOTO <= LA94_0 <= IF) or LA94_0 == OPEN or (RAISE <= LA94_0 <= LLABEL) or (COMMIT <= LA94_0 <= SET) or (UPDATE <= LA94_0 <= WHILE)) :
                        alt94 = 1


                    if alt94 == 1:
                        # sql.g:300:30: statement SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_if_statement2336)
                        statement313 = self.statement()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, statement313.tree)
                        SEMI314=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_if_statement2338)

                        SEMI314_tree = self._adaptor.createWithPayload(SEMI314)
                        self._adaptor.addChild(root_0, SEMI314_tree)



                    else:
                        if cnt94 >= 1:
                            break #loop94

                        eee = EarlyExitException(94, self.input)
                        raise eee

                    cnt94 += 1
                # sql.g:301:9: ( ELSIF expression THEN ( statement SEMI )+ )*
                while True: #loop96
                    alt96 = 2
                    LA96_0 = self.input.LA(1)

                    if (LA96_0 == ELSIF) :
                        alt96 = 1


                    if alt96 == 1:
                        # sql.g:301:11: ELSIF expression THEN ( statement SEMI )+
                        pass 
                        ELSIF315=self.match(self.input, ELSIF, self.FOLLOW_ELSIF_in_if_statement2353)

                        ELSIF315_tree = self._adaptor.createWithPayload(ELSIF315)
                        self._adaptor.addChild(root_0, ELSIF315_tree)

                        self._state.following.append(self.FOLLOW_expression_in_if_statement2355)
                        expression316 = self.expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, expression316.tree)
                        THEN317=self.match(self.input, THEN, self.FOLLOW_THEN_in_if_statement2357)

                        THEN317_tree = self._adaptor.createWithPayload(THEN317)
                        self._adaptor.addChild(root_0, THEN317_tree)

                        # sql.g:301:33: ( statement SEMI )+
                        cnt95 = 0
                        while True: #loop95
                            alt95 = 2
                            LA95_0 = self.input.LA(1)

                            if (LA95_0 == ID or LA95_0 == RETURN or LA95_0 == NULL or LA95_0 == BEGIN or (COLON <= LA95_0 <= CASE) or (CLOSE <= LA95_0 <= EXECUTE) or (EXIT <= LA95_0 <= FETCH) or (FOR <= LA95_0 <= FORALL) or (GOTO <= LA95_0 <= IF) or LA95_0 == OPEN or (RAISE <= LA95_0 <= LLABEL) or (COMMIT <= LA95_0 <= SET) or (UPDATE <= LA95_0 <= WHILE)) :
                                alt95 = 1


                            if alt95 == 1:
                                # sql.g:301:35: statement SEMI
                                pass 
                                self._state.following.append(self.FOLLOW_statement_in_if_statement2361)
                                statement318 = self.statement()

                                self._state.following.pop()
                                self._adaptor.addChild(root_0, statement318.tree)
                                SEMI319=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_if_statement2363)

                                SEMI319_tree = self._adaptor.createWithPayload(SEMI319)
                                self._adaptor.addChild(root_0, SEMI319_tree)



                            else:
                                if cnt95 >= 1:
                                    break #loop95

                                eee = EarlyExitException(95, self.input)
                                raise eee

                            cnt95 += 1


                    else:
                        break #loop96
                # sql.g:302:9: ( ELSE ( statement SEMI )+ )?
                alt98 = 2
                LA98_0 = self.input.LA(1)

                if (LA98_0 == ELSE) :
                    alt98 = 1
                if alt98 == 1:
                    # sql.g:302:11: ELSE ( statement SEMI )+
                    pass 
                    ELSE320=self.match(self.input, ELSE, self.FOLLOW_ELSE_in_if_statement2381)

                    ELSE320_tree = self._adaptor.createWithPayload(ELSE320)
                    self._adaptor.addChild(root_0, ELSE320_tree)

                    # sql.g:302:16: ( statement SEMI )+
                    cnt97 = 0
                    while True: #loop97
                        alt97 = 2
                        LA97_0 = self.input.LA(1)

                        if (LA97_0 == ID or LA97_0 == RETURN or LA97_0 == NULL or LA97_0 == BEGIN or (COLON <= LA97_0 <= CASE) or (CLOSE <= LA97_0 <= EXECUTE) or (EXIT <= LA97_0 <= FETCH) or (FOR <= LA97_0 <= FORALL) or (GOTO <= LA97_0 <= IF) or LA97_0 == OPEN or (RAISE <= LA97_0 <= LLABEL) or (COMMIT <= LA97_0 <= SET) or (UPDATE <= LA97_0 <= WHILE)) :
                            alt97 = 1


                        if alt97 == 1:
                            # sql.g:302:18: statement SEMI
                            pass 
                            self._state.following.append(self.FOLLOW_statement_in_if_statement2385)
                            statement321 = self.statement()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, statement321.tree)
                            SEMI322=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_if_statement2387)

                            SEMI322_tree = self._adaptor.createWithPayload(SEMI322)
                            self._adaptor.addChild(root_0, SEMI322_tree)



                        else:
                            if cnt97 >= 1:
                                break #loop97

                            eee = EarlyExitException(97, self.input)
                            raise eee

                        cnt97 += 1



                END323=self.match(self.input, END, self.FOLLOW_END_in_if_statement2403)

                END323_tree = self._adaptor.createWithPayload(END323)
                self._adaptor.addChild(root_0, END323_tree)

                IF324=self.match(self.input, IF, self.FOLLOW_IF_in_if_statement2405)

                IF324_tree = self._adaptor.createWithPayload(IF324)
                self._adaptor.addChild(root_0, IF324_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "if_statement"

    class null_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.null_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "null_statement"
    # sql.g:306:1: null_statement : NULL ;
    def null_statement(self, ):

        retval = self.null_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NULL325 = None

        NULL325_tree = None

        try:
            try:
                # sql.g:306:16: ( NULL )
                # sql.g:307:9: NULL
                pass 
                root_0 = self._adaptor.nil()

                NULL325=self.match(self.input, NULL, self.FOLLOW_NULL_in_null_statement2426)

                NULL325_tree = self._adaptor.createWithPayload(NULL325)
                self._adaptor.addChild(root_0, NULL325_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "null_statement"

    class open_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.open_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "open_statement"
    # sql.g:310:1: open_statement : OPEN ID ( DOT ID )* ( call_args )? ( FOR select_statement )? ;
    def open_statement(self, ):

        retval = self.open_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        OPEN326 = None
        ID327 = None
        DOT328 = None
        ID329 = None
        FOR331 = None
        call_args330 = None

        select_statement332 = None


        OPEN326_tree = None
        ID327_tree = None
        DOT328_tree = None
        ID329_tree = None
        FOR331_tree = None

        try:
            try:
                # sql.g:310:16: ( OPEN ID ( DOT ID )* ( call_args )? ( FOR select_statement )? )
                # sql.g:311:9: OPEN ID ( DOT ID )* ( call_args )? ( FOR select_statement )?
                pass 
                root_0 = self._adaptor.nil()

                OPEN326=self.match(self.input, OPEN, self.FOLLOW_OPEN_in_open_statement2447)

                OPEN326_tree = self._adaptor.createWithPayload(OPEN326)
                self._adaptor.addChild(root_0, OPEN326_tree)

                ID327=self.match(self.input, ID, self.FOLLOW_ID_in_open_statement2449)

                ID327_tree = self._adaptor.createWithPayload(ID327)
                self._adaptor.addChild(root_0, ID327_tree)

                # sql.g:311:17: ( DOT ID )*
                while True: #loop99
                    alt99 = 2
                    LA99_0 = self.input.LA(1)

                    if (LA99_0 == DOT) :
                        alt99 = 1


                    if alt99 == 1:
                        # sql.g:311:19: DOT ID
                        pass 
                        DOT328=self.match(self.input, DOT, self.FOLLOW_DOT_in_open_statement2453)

                        DOT328_tree = self._adaptor.createWithPayload(DOT328)
                        self._adaptor.addChild(root_0, DOT328_tree)

                        ID329=self.match(self.input, ID, self.FOLLOW_ID_in_open_statement2455)

                        ID329_tree = self._adaptor.createWithPayload(ID329)
                        self._adaptor.addChild(root_0, ID329_tree)



                    else:
                        break #loop99
                # sql.g:311:29: ( call_args )?
                alt100 = 2
                LA100_0 = self.input.LA(1)

                if (LA100_0 == LPAREN) :
                    alt100 = 1
                if alt100 == 1:
                    # sql.g:311:29: call_args
                    pass 
                    self._state.following.append(self.FOLLOW_call_args_in_open_statement2460)
                    call_args330 = self.call_args()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, call_args330.tree)



                # sql.g:311:40: ( FOR select_statement )?
                alt101 = 2
                LA101_0 = self.input.LA(1)

                if (LA101_0 == FOR) :
                    alt101 = 1
                if alt101 == 1:
                    # sql.g:311:42: FOR select_statement
                    pass 
                    FOR331=self.match(self.input, FOR, self.FOLLOW_FOR_in_open_statement2465)

                    FOR331_tree = self._adaptor.createWithPayload(FOR331)
                    self._adaptor.addChild(root_0, FOR331_tree)

                    self._state.following.append(self.FOLLOW_select_statement_in_open_statement2467)
                    select_statement332 = self.select_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, select_statement332.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "open_statement"

    class pragma_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.pragma_return, self).__init__()

            self.tree = None




    # $ANTLR start "pragma"
    # sql.g:314:1: pragma : PRAGMA swallow_to_semi ;
    def pragma(self, ):

        retval = self.pragma_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PRAGMA333 = None
        swallow_to_semi334 = None


        PRAGMA333_tree = None

        try:
            try:
                # sql.g:314:8: ( PRAGMA swallow_to_semi )
                # sql.g:315:9: PRAGMA swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                PRAGMA333=self.match(self.input, PRAGMA, self.FOLLOW_PRAGMA_in_pragma2491)

                PRAGMA333_tree = self._adaptor.createWithPayload(PRAGMA333)
                self._adaptor.addChild(root_0, PRAGMA333_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_pragma2493)
                swallow_to_semi334 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi334.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "pragma"

    class raise_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.raise_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "raise_statement"
    # sql.g:318:1: raise_statement : RAISE ( ID ( DOT ID )* )? ;
    def raise_statement(self, ):

        retval = self.raise_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RAISE335 = None
        ID336 = None
        DOT337 = None
        ID338 = None

        RAISE335_tree = None
        ID336_tree = None
        DOT337_tree = None
        ID338_tree = None

        try:
            try:
                # sql.g:318:17: ( RAISE ( ID ( DOT ID )* )? )
                # sql.g:319:9: RAISE ( ID ( DOT ID )* )?
                pass 
                root_0 = self._adaptor.nil()

                RAISE335=self.match(self.input, RAISE, self.FOLLOW_RAISE_in_raise_statement2514)

                RAISE335_tree = self._adaptor.createWithPayload(RAISE335)
                self._adaptor.addChild(root_0, RAISE335_tree)

                # sql.g:319:15: ( ID ( DOT ID )* )?
                alt103 = 2
                LA103_0 = self.input.LA(1)

                if (LA103_0 == ID) :
                    alt103 = 1
                if alt103 == 1:
                    # sql.g:319:17: ID ( DOT ID )*
                    pass 
                    ID336=self.match(self.input, ID, self.FOLLOW_ID_in_raise_statement2518)

                    ID336_tree = self._adaptor.createWithPayload(ID336)
                    self._adaptor.addChild(root_0, ID336_tree)

                    # sql.g:319:20: ( DOT ID )*
                    while True: #loop102
                        alt102 = 2
                        LA102_0 = self.input.LA(1)

                        if (LA102_0 == DOT) :
                            alt102 = 1


                        if alt102 == 1:
                            # sql.g:319:22: DOT ID
                            pass 
                            DOT337=self.match(self.input, DOT, self.FOLLOW_DOT_in_raise_statement2522)

                            DOT337_tree = self._adaptor.createWithPayload(DOT337)
                            self._adaptor.addChild(root_0, DOT337_tree)

                            ID338=self.match(self.input, ID, self.FOLLOW_ID_in_raise_statement2524)

                            ID338_tree = self._adaptor.createWithPayload(ID338)
                            self._adaptor.addChild(root_0, ID338_tree)



                        else:
                            break #loop102






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "raise_statement"

    class return_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.return_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "return_statement"
    # sql.g:322:1: return_statement : RETURN ( expression )? ;
    def return_statement(self, ):

        retval = self.return_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RETURN339 = None
        expression340 = None


        RETURN339_tree = None

        try:
            try:
                # sql.g:322:18: ( RETURN ( expression )? )
                # sql.g:323:9: RETURN ( expression )?
                pass 
                root_0 = self._adaptor.nil()

                RETURN339=self.match(self.input, RETURN, self.FOLLOW_RETURN_in_return_statement2551)

                RETURN339_tree = self._adaptor.createWithPayload(RETURN339)
                self._adaptor.addChild(root_0, RETURN339_tree)

                # sql.g:323:16: ( expression )?
                alt104 = 2
                LA104_0 = self.input.LA(1)

                if (LA104_0 == ID or LA104_0 == LPAREN or (NOT <= LA104_0 <= NULL) or LA104_0 == COLON or (MINUS <= LA104_0 <= PLUS) or LA104_0 == SQL or (INTEGER <= LA104_0 <= QUOTED_STRING) or (INSERTING <= LA104_0 <= DELETING)) :
                    alt104 = 1
                if alt104 == 1:
                    # sql.g:323:16: expression
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_return_statement2553)
                    expression340 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression340.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "return_statement"

    class plsql_block_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.plsql_block_return, self).__init__()

            self.tree = None




    # $ANTLR start "plsql_block"
    # sql.g:326:1: plsql_block : ( DECLARE declare_section )? body ;
    def plsql_block(self, ):

        retval = self.plsql_block_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DECLARE341 = None
        declare_section342 = None

        body343 = None


        DECLARE341_tree = None

        try:
            try:
                # sql.g:326:13: ( ( DECLARE declare_section )? body )
                # sql.g:327:9: ( DECLARE declare_section )? body
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:327:9: ( DECLARE declare_section )?
                alt105 = 2
                LA105_0 = self.input.LA(1)

                if (LA105_0 == DECLARE) :
                    alt105 = 1
                if alt105 == 1:
                    # sql.g:327:11: DECLARE declare_section
                    pass 
                    DECLARE341=self.match(self.input, DECLARE, self.FOLLOW_DECLARE_in_plsql_block2577)

                    DECLARE341_tree = self._adaptor.createWithPayload(DECLARE341)
                    self._adaptor.addChild(root_0, DECLARE341_tree)

                    self._state.following.append(self.FOLLOW_declare_section_in_plsql_block2579)
                    declare_section342 = self.declare_section()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, declare_section342.tree)



                self._state.following.append(self.FOLLOW_body_in_plsql_block2584)
                body343 = self.body()

                self._state.following.pop()
                self._adaptor.addChild(root_0, body343.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "plsql_block"

    class label_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.label_return, self).__init__()

            self.tree = None




    # $ANTLR start "label"
    # sql.g:330:1: label : LLABEL label RLABEL ;
    def label(self, ):

        retval = self.label_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LLABEL344 = None
        RLABEL346 = None
        label345 = None


        LLABEL344_tree = None
        RLABEL346_tree = None

        try:
            try:
                # sql.g:330:7: ( LLABEL label RLABEL )
                # sql.g:331:9: LLABEL label RLABEL
                pass 
                root_0 = self._adaptor.nil()

                LLABEL344=self.match(self.input, LLABEL, self.FOLLOW_LLABEL_in_label2605)

                LLABEL344_tree = self._adaptor.createWithPayload(LLABEL344)
                self._adaptor.addChild(root_0, LLABEL344_tree)

                self._state.following.append(self.FOLLOW_label_in_label2607)
                label345 = self.label()

                self._state.following.pop()
                self._adaptor.addChild(root_0, label345.tree)
                RLABEL346=self.match(self.input, RLABEL, self.FOLLOW_RLABEL_in_label2609)

                RLABEL346_tree = self._adaptor.createWithPayload(RLABEL346)
                self._adaptor.addChild(root_0, RLABEL346_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "label"

    class qual_id_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.qual_id_return, self).__init__()

            self.tree = None




    # $ANTLR start "qual_id"
    # sql.g:334:1: qual_id : ( COLON )? ID ( DOT ( COLON )? ID )* ;
    def qual_id(self, ):

        retval = self.qual_id_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COLON347 = None
        ID348 = None
        DOT349 = None
        COLON350 = None
        ID351 = None

        COLON347_tree = None
        ID348_tree = None
        DOT349_tree = None
        COLON350_tree = None
        ID351_tree = None

        try:
            try:
                # sql.g:334:9: ( ( COLON )? ID ( DOT ( COLON )? ID )* )
                # sql.g:335:2: ( COLON )? ID ( DOT ( COLON )? ID )*
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:335:2: ( COLON )?
                alt106 = 2
                LA106_0 = self.input.LA(1)

                if (LA106_0 == COLON) :
                    alt106 = 1
                if alt106 == 1:
                    # sql.g:335:2: COLON
                    pass 
                    COLON347=self.match(self.input, COLON, self.FOLLOW_COLON_in_qual_id2623)

                    COLON347_tree = self._adaptor.createWithPayload(COLON347)
                    self._adaptor.addChild(root_0, COLON347_tree)




                ID348=self.match(self.input, ID, self.FOLLOW_ID_in_qual_id2626)

                ID348_tree = self._adaptor.createWithPayload(ID348)
                self._adaptor.addChild(root_0, ID348_tree)

                # sql.g:335:12: ( DOT ( COLON )? ID )*
                while True: #loop108
                    alt108 = 2
                    LA108_0 = self.input.LA(1)

                    if (LA108_0 == DOT) :
                        alt108 = 1


                    if alt108 == 1:
                        # sql.g:335:14: DOT ( COLON )? ID
                        pass 
                        DOT349=self.match(self.input, DOT, self.FOLLOW_DOT_in_qual_id2630)

                        DOT349_tree = self._adaptor.createWithPayload(DOT349)
                        self._adaptor.addChild(root_0, DOT349_tree)

                        # sql.g:335:18: ( COLON )?
                        alt107 = 2
                        LA107_0 = self.input.LA(1)

                        if (LA107_0 == COLON) :
                            alt107 = 1
                        if alt107 == 1:
                            # sql.g:335:18: COLON
                            pass 
                            COLON350=self.match(self.input, COLON, self.FOLLOW_COLON_in_qual_id2632)

                            COLON350_tree = self._adaptor.createWithPayload(COLON350)
                            self._adaptor.addChild(root_0, COLON350_tree)




                        ID351=self.match(self.input, ID, self.FOLLOW_ID_in_qual_id2635)

                        ID351_tree = self._adaptor.createWithPayload(ID351)
                        self._adaptor.addChild(root_0, ID351_tree)



                    else:
                        break #loop108



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "qual_id"

    class sql_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.sql_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "sql_statement"
    # sql.g:338:1: sql_statement : ( commit_statement | delete_statement | insert_statement | lock_table_statement | rollback_statement | savepoint_statement | select_statement | set_transaction_statement | update_statement );
    def sql_statement(self, ):

        retval = self.sql_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        commit_statement352 = None

        delete_statement353 = None

        insert_statement354 = None

        lock_table_statement355 = None

        rollback_statement356 = None

        savepoint_statement357 = None

        select_statement358 = None

        set_transaction_statement359 = None

        update_statement360 = None



        try:
            try:
                # sql.g:339:5: ( commit_statement | delete_statement | insert_statement | lock_table_statement | rollback_statement | savepoint_statement | select_statement | set_transaction_statement | update_statement )
                alt109 = 9
                LA109 = self.input.LA(1)
                if LA109 == COMMIT:
                    alt109 = 1
                elif LA109 == DELETE:
                    alt109 = 2
                elif LA109 == INSERT:
                    alt109 = 3
                elif LA109 == LOCK:
                    alt109 = 4
                elif LA109 == ROLLBACK:
                    alt109 = 5
                elif LA109 == SAVEPOINT:
                    alt109 = 6
                elif LA109 == SELECT:
                    alt109 = 7
                elif LA109 == SET:
                    alt109 = 8
                elif LA109 == UPDATE:
                    alt109 = 9
                else:
                    nvae = NoViableAltException("", 109, 0, self.input)

                    raise nvae

                if alt109 == 1:
                    # sql.g:339:7: commit_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_commit_statement_in_sql_statement2655)
                    commit_statement352 = self.commit_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, commit_statement352.tree)


                elif alt109 == 2:
                    # sql.g:340:7: delete_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_delete_statement_in_sql_statement2663)
                    delete_statement353 = self.delete_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, delete_statement353.tree)


                elif alt109 == 3:
                    # sql.g:341:7: insert_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_insert_statement_in_sql_statement2671)
                    insert_statement354 = self.insert_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, insert_statement354.tree)


                elif alt109 == 4:
                    # sql.g:342:7: lock_table_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_lock_table_statement_in_sql_statement2679)
                    lock_table_statement355 = self.lock_table_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, lock_table_statement355.tree)


                elif alt109 == 5:
                    # sql.g:343:7: rollback_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_rollback_statement_in_sql_statement2687)
                    rollback_statement356 = self.rollback_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, rollback_statement356.tree)


                elif alt109 == 6:
                    # sql.g:344:7: savepoint_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_savepoint_statement_in_sql_statement2695)
                    savepoint_statement357 = self.savepoint_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, savepoint_statement357.tree)


                elif alt109 == 7:
                    # sql.g:345:7: select_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_select_statement_in_sql_statement2703)
                    select_statement358 = self.select_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, select_statement358.tree)


                elif alt109 == 8:
                    # sql.g:346:7: set_transaction_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_set_transaction_statement_in_sql_statement2711)
                    set_transaction_statement359 = self.set_transaction_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, set_transaction_statement359.tree)


                elif alt109 == 9:
                    # sql.g:347:7: update_statement
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_update_statement_in_sql_statement2719)
                    update_statement360 = self.update_statement()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, update_statement360.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "sql_statement"

    class commit_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.commit_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "commit_statement"
    # sql.g:350:1: commit_statement : COMMIT ( swallow_to_semi )? ;
    def commit_statement(self, ):

        retval = self.commit_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COMMIT361 = None
        swallow_to_semi362 = None


        COMMIT361_tree = None

        try:
            try:
                # sql.g:350:18: ( COMMIT ( swallow_to_semi )? )
                # sql.g:351:9: COMMIT ( swallow_to_semi )?
                pass 
                root_0 = self._adaptor.nil()

                COMMIT361=self.match(self.input, COMMIT, self.FOLLOW_COMMIT_in_commit_statement2740)

                COMMIT361_tree = self._adaptor.createWithPayload(COMMIT361)
                self._adaptor.addChild(root_0, COMMIT361_tree)

                # sql.g:351:16: ( swallow_to_semi )?
                alt110 = 2
                LA110_0 = self.input.LA(1)

                if (LA110_0 == ID) :
                    LA110_1 = self.input.LA(2)

                    if ((DIVIDE <= LA110_1 <= PROCEDURE) or (FUNCTION <= LA110_1 <= ML_COMMENT)) :
                        alt110 = 1
                    elif (LA110_1 == ID) :
                        LA110_4 = self.input.LA(3)

                        if (not (((self.input.LT(1).text.lower() == "save")))) :
                            alt110 = 1
                elif (LA110_0 == DIVIDE or LA110_0 == PROCEDURE or (FUNCTION <= LA110_0 <= ML_COMMENT)) :
                    alt110 = 1
                if alt110 == 1:
                    # sql.g:351:16: swallow_to_semi
                    pass 
                    self._state.following.append(self.FOLLOW_swallow_to_semi_in_commit_statement2742)
                    swallow_to_semi362 = self.swallow_to_semi()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, swallow_to_semi362.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "commit_statement"

    class delete_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.delete_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "delete_statement"
    # sql.g:354:1: delete_statement : DELETE swallow_to_semi ;
    def delete_statement(self, ):

        retval = self.delete_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DELETE363 = None
        swallow_to_semi364 = None


        DELETE363_tree = None

        try:
            try:
                # sql.g:354:18: ( DELETE swallow_to_semi )
                # sql.g:355:9: DELETE swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                DELETE363=self.match(self.input, DELETE, self.FOLLOW_DELETE_in_delete_statement2764)

                DELETE363_tree = self._adaptor.createWithPayload(DELETE363)
                self._adaptor.addChild(root_0, DELETE363_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_delete_statement2766)
                swallow_to_semi364 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi364.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "delete_statement"

    class insert_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.insert_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "insert_statement"
    # sql.g:358:1: insert_statement : INSERT swallow_to_semi ;
    def insert_statement(self, ):

        retval = self.insert_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        INSERT365 = None
        swallow_to_semi366 = None


        INSERT365_tree = None

        try:
            try:
                # sql.g:358:18: ( INSERT swallow_to_semi )
                # sql.g:359:9: INSERT swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                INSERT365=self.match(self.input, INSERT, self.FOLLOW_INSERT_in_insert_statement2787)

                INSERT365_tree = self._adaptor.createWithPayload(INSERT365)
                self._adaptor.addChild(root_0, INSERT365_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_insert_statement2789)
                swallow_to_semi366 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi366.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "insert_statement"

    class lock_table_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.lock_table_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "lock_table_statement"
    # sql.g:362:1: lock_table_statement : LOCK TABLE swallow_to_semi ;
    def lock_table_statement(self, ):

        retval = self.lock_table_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LOCK367 = None
        TABLE368 = None
        swallow_to_semi369 = None


        LOCK367_tree = None
        TABLE368_tree = None

        try:
            try:
                # sql.g:362:22: ( LOCK TABLE swallow_to_semi )
                # sql.g:363:9: LOCK TABLE swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                LOCK367=self.match(self.input, LOCK, self.FOLLOW_LOCK_in_lock_table_statement2810)

                LOCK367_tree = self._adaptor.createWithPayload(LOCK367)
                self._adaptor.addChild(root_0, LOCK367_tree)

                TABLE368=self.match(self.input, TABLE, self.FOLLOW_TABLE_in_lock_table_statement2812)

                TABLE368_tree = self._adaptor.createWithPayload(TABLE368)
                self._adaptor.addChild(root_0, TABLE368_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_lock_table_statement2814)
                swallow_to_semi369 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi369.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "lock_table_statement"

    class rollback_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.rollback_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "rollback_statement"
    # sql.g:366:1: rollback_statement : ROLLBACK ( swallow_to_semi )? ;
    def rollback_statement(self, ):

        retval = self.rollback_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ROLLBACK370 = None
        swallow_to_semi371 = None


        ROLLBACK370_tree = None

        try:
            try:
                # sql.g:366:20: ( ROLLBACK ( swallow_to_semi )? )
                # sql.g:367:9: ROLLBACK ( swallow_to_semi )?
                pass 
                root_0 = self._adaptor.nil()

                ROLLBACK370=self.match(self.input, ROLLBACK, self.FOLLOW_ROLLBACK_in_rollback_statement2835)

                ROLLBACK370_tree = self._adaptor.createWithPayload(ROLLBACK370)
                self._adaptor.addChild(root_0, ROLLBACK370_tree)

                # sql.g:367:18: ( swallow_to_semi )?
                alt111 = 2
                LA111_0 = self.input.LA(1)

                if (LA111_0 == ID) :
                    LA111_1 = self.input.LA(2)

                    if ((DIVIDE <= LA111_1 <= PROCEDURE) or (FUNCTION <= LA111_1 <= ML_COMMENT)) :
                        alt111 = 1
                    elif (LA111_1 == ID) :
                        LA111_4 = self.input.LA(3)

                        if (not (((self.input.LT(1).text.lower() == "save")))) :
                            alt111 = 1
                elif (LA111_0 == DIVIDE or LA111_0 == PROCEDURE or (FUNCTION <= LA111_0 <= ML_COMMENT)) :
                    alt111 = 1
                if alt111 == 1:
                    # sql.g:367:18: swallow_to_semi
                    pass 
                    self._state.following.append(self.FOLLOW_swallow_to_semi_in_rollback_statement2837)
                    swallow_to_semi371 = self.swallow_to_semi()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, swallow_to_semi371.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "rollback_statement"

    class savepoint_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.savepoint_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "savepoint_statement"
    # sql.g:370:1: savepoint_statement : SAVEPOINT ID ;
    def savepoint_statement(self, ):

        retval = self.savepoint_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SAVEPOINT372 = None
        ID373 = None

        SAVEPOINT372_tree = None
        ID373_tree = None

        try:
            try:
                # sql.g:370:21: ( SAVEPOINT ID )
                # sql.g:371:9: SAVEPOINT ID
                pass 
                root_0 = self._adaptor.nil()

                SAVEPOINT372=self.match(self.input, SAVEPOINT, self.FOLLOW_SAVEPOINT_in_savepoint_statement2859)

                SAVEPOINT372_tree = self._adaptor.createWithPayload(SAVEPOINT372)
                self._adaptor.addChild(root_0, SAVEPOINT372_tree)

                ID373=self.match(self.input, ID, self.FOLLOW_ID_in_savepoint_statement2861)

                ID373_tree = self._adaptor.createWithPayload(ID373)
                self._adaptor.addChild(root_0, ID373_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "savepoint_statement"

    class select_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.select_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "select_statement"
    # sql.g:374:1: select_statement : SELECT swallow_to_semi ;
    def select_statement(self, ):

        retval = self.select_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SELECT374 = None
        swallow_to_semi375 = None


        SELECT374_tree = None

        try:
            try:
                # sql.g:374:18: ( SELECT swallow_to_semi )
                # sql.g:375:9: SELECT swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                SELECT374=self.match(self.input, SELECT, self.FOLLOW_SELECT_in_select_statement2882)

                SELECT374_tree = self._adaptor.createWithPayload(SELECT374)
                self._adaptor.addChild(root_0, SELECT374_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_select_statement2884)
                swallow_to_semi375 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi375.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "select_statement"

    class set_transaction_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.set_transaction_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "set_transaction_statement"
    # sql.g:378:1: set_transaction_statement : SET TRANSACTION swallow_to_semi ;
    def set_transaction_statement(self, ):

        retval = self.set_transaction_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SET376 = None
        TRANSACTION377 = None
        swallow_to_semi378 = None


        SET376_tree = None
        TRANSACTION377_tree = None

        try:
            try:
                # sql.g:378:27: ( SET TRANSACTION swallow_to_semi )
                # sql.g:379:9: SET TRANSACTION swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                SET376=self.match(self.input, SET, self.FOLLOW_SET_in_set_transaction_statement2905)

                SET376_tree = self._adaptor.createWithPayload(SET376)
                self._adaptor.addChild(root_0, SET376_tree)

                TRANSACTION377=self.match(self.input, TRANSACTION, self.FOLLOW_TRANSACTION_in_set_transaction_statement2907)

                TRANSACTION377_tree = self._adaptor.createWithPayload(TRANSACTION377)
                self._adaptor.addChild(root_0, TRANSACTION377_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_set_transaction_statement2909)
                swallow_to_semi378 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi378.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "set_transaction_statement"

    class update_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.update_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "update_statement"
    # sql.g:382:1: update_statement : UPDATE swallow_to_semi ;
    def update_statement(self, ):

        retval = self.update_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        UPDATE379 = None
        swallow_to_semi380 = None


        UPDATE379_tree = None

        try:
            try:
                # sql.g:382:18: ( UPDATE swallow_to_semi )
                # sql.g:383:9: UPDATE swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                UPDATE379=self.match(self.input, UPDATE, self.FOLLOW_UPDATE_in_update_statement2930)

                UPDATE379_tree = self._adaptor.createWithPayload(UPDATE379)
                self._adaptor.addChild(root_0, UPDATE379_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_update_statement2932)
                swallow_to_semi380 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi380.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "update_statement"

    class swallow_to_semi_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.swallow_to_semi_return, self).__init__()

            self.tree = None




    # $ANTLR start "swallow_to_semi"
    # sql.g:386:1: swallow_to_semi : (~ ( SEMI ) )+ ;
    def swallow_to_semi(self, ):

        retval = self.swallow_to_semi_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set381 = None

        set381_tree = None

        try:
            try:
                # sql.g:386:17: ( (~ ( SEMI ) )+ )
                # sql.g:387:9: (~ ( SEMI ) )+
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:387:9: (~ ( SEMI ) )+
                cnt112 = 0
                while True: #loop112
                    alt112 = 2
                    LA112_0 = self.input.LA(1)

                    if (LA112_0 == ID) :
                        LA112_2 = self.input.LA(2)

                        if ((DIVIDE <= LA112_2 <= PROCEDURE) or (FUNCTION <= LA112_2 <= ML_COMMENT)) :
                            alt112 = 1
                        elif (LA112_2 == ID) :
                            LA112_4 = self.input.LA(3)

                            if (not (((self.input.LT(1).text.lower() == "save")))) :
                                alt112 = 1




                    elif (LA112_0 == DIVIDE or LA112_0 == PROCEDURE or (FUNCTION <= LA112_0 <= ML_COMMENT)) :
                        alt112 = 1


                    if alt112 == 1:
                        # sql.g:387:9: ~ ( SEMI )
                        pass 
                        set381 = self.input.LT(1)
                        if self.input.LA(1) == DIVIDE or (PROCEDURE <= self.input.LA(1) <= ML_COMMENT):
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set381))
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        if cnt112 >= 1:
                            break #loop112

                        eee = EarlyExitException(112, self.input)
                        raise eee

                    cnt112 += 1



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "swallow_to_semi"

    class while_loop_statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.while_loop_statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "while_loop_statement"
    # sql.g:390:1: while_loop_statement : WHILE expression LOOP ( statement SEMI )+ END LOOP ( label_name )? ;
    def while_loop_statement(self, ):

        retval = self.while_loop_statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        WHILE382 = None
        LOOP384 = None
        SEMI386 = None
        END387 = None
        LOOP388 = None
        expression383 = None

        statement385 = None

        label_name389 = None


        WHILE382_tree = None
        LOOP384_tree = None
        SEMI386_tree = None
        END387_tree = None
        LOOP388_tree = None

        try:
            try:
                # sql.g:390:22: ( WHILE expression LOOP ( statement SEMI )+ END LOOP ( label_name )? )
                # sql.g:391:9: WHILE expression LOOP ( statement SEMI )+ END LOOP ( label_name )?
                pass 
                root_0 = self._adaptor.nil()

                WHILE382=self.match(self.input, WHILE, self.FOLLOW_WHILE_in_while_loop_statement2980)

                WHILE382_tree = self._adaptor.createWithPayload(WHILE382)
                self._adaptor.addChild(root_0, WHILE382_tree)

                self._state.following.append(self.FOLLOW_expression_in_while_loop_statement2982)
                expression383 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression383.tree)
                LOOP384=self.match(self.input, LOOP, self.FOLLOW_LOOP_in_while_loop_statement2984)

                LOOP384_tree = self._adaptor.createWithPayload(LOOP384)
                self._adaptor.addChild(root_0, LOOP384_tree)

                # sql.g:391:31: ( statement SEMI )+
                cnt113 = 0
                while True: #loop113
                    alt113 = 2
                    LA113_0 = self.input.LA(1)

                    if (LA113_0 == ID or LA113_0 == RETURN or LA113_0 == NULL or LA113_0 == BEGIN or (COLON <= LA113_0 <= CASE) or (CLOSE <= LA113_0 <= EXECUTE) or (EXIT <= LA113_0 <= FETCH) or (FOR <= LA113_0 <= FORALL) or (GOTO <= LA113_0 <= IF) or LA113_0 == OPEN or (RAISE <= LA113_0 <= LLABEL) or (COMMIT <= LA113_0 <= SET) or (UPDATE <= LA113_0 <= WHILE)) :
                        alt113 = 1


                    if alt113 == 1:
                        # sql.g:391:33: statement SEMI
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_while_loop_statement2988)
                        statement385 = self.statement()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, statement385.tree)
                        SEMI386=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_while_loop_statement2990)

                        SEMI386_tree = self._adaptor.createWithPayload(SEMI386)
                        self._adaptor.addChild(root_0, SEMI386_tree)



                    else:
                        if cnt113 >= 1:
                            break #loop113

                        eee = EarlyExitException(113, self.input)
                        raise eee

                    cnt113 += 1
                END387=self.match(self.input, END, self.FOLLOW_END_in_while_loop_statement2995)

                END387_tree = self._adaptor.createWithPayload(END387)
                self._adaptor.addChild(root_0, END387_tree)

                LOOP388=self.match(self.input, LOOP, self.FOLLOW_LOOP_in_while_loop_statement2997)

                LOOP388_tree = self._adaptor.createWithPayload(LOOP388)
                self._adaptor.addChild(root_0, LOOP388_tree)

                # sql.g:391:60: ( label_name )?
                alt114 = 2
                LA114_0 = self.input.LA(1)

                if (LA114_0 == ID) :
                    alt114 = 1
                if alt114 == 1:
                    # sql.g:391:60: label_name
                    pass 
                    self._state.following.append(self.FOLLOW_label_name_in_while_loop_statement2999)
                    label_name389 = self.label_name()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, label_name389.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "while_loop_statement"

    class match_parens_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.match_parens_return, self).__init__()

            self.tree = None




    # $ANTLR start "match_parens"
    # sql.g:394:1: match_parens : ( ( options {greedy=false; } : ~ ( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT ) )* | RPAREN match_parens LPAREN );
    def match_parens(self, ):

        retval = self.match_parens_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set390 = None
        RPAREN391 = None
        LPAREN393 = None
        match_parens392 = None


        set390_tree = None
        RPAREN391_tree = None
        LPAREN393_tree = None

        try:
            try:
                # sql.g:395:5: ( ( options {greedy=false; } : ~ ( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT ) )* | RPAREN match_parens LPAREN )
                alt116 = 2
                LA116_0 = self.input.LA(1)

                if (LA116_0 == DIVIDE or (PROCEDURE <= LA116_0 <= COMMA) or (NOCOPY <= LA116_0 <= CURSOR) or (NOT <= LA116_0 <= RESULT_CACHE) or (BEGIN <= LA116_0 <= ML_COMMENT)) :
                    alt116 = 1
                elif (LA116_0 == RPAREN) :
                    alt116 = 2
                else:
                    nvae = NoViableAltException("", 116, 0, self.input)

                    raise nvae

                if alt116 == 1:
                    # sql.g:395:7: ( options {greedy=false; } : ~ ( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT ) )*
                    pass 
                    root_0 = self._adaptor.nil()

                    # sql.g:395:7: ( options {greedy=false; } : ~ ( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT ) )*
                    while True: #loop115
                        alt115 = 2
                        LA115_0 = self.input.LA(1)

                        if (LA115_0 == DIVIDE or (PROCEDURE <= LA115_0 <= RETURN) or LA115_0 == COMMA or (NOCOPY <= LA115_0 <= CURSOR) or (NOT <= LA115_0 <= RESULT_CACHE) or (BEGIN <= LA115_0 <= ML_COMMENT)) :
                            alt115 = 1
                        elif (LA115_0 == LPAREN) :
                            alt115 = 2


                        if alt115 == 1:
                            # sql.g:395:35: ~ ( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT )
                            pass 
                            set390 = self.input.LT(1)
                            if self.input.LA(1) == DIVIDE or (PROCEDURE <= self.input.LA(1) <= RETURN) or self.input.LA(1) == COMMA or (NOCOPY <= self.input.LA(1) <= CURSOR) or (NOT <= self.input.LA(1) <= RESULT_CACHE) or (BEGIN <= self.input.LA(1) <= ML_COMMENT):
                                self.input.consume()
                                self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set390))
                                self._state.errorRecovery = False

                            else:
                                mse = MismatchedSetException(None, self.input)
                                raise mse




                        else:
                            break #loop115


                elif alt116 == 2:
                    # sql.g:396:7: RPAREN match_parens LPAREN
                    pass 
                    root_0 = self._adaptor.nil()

                    RPAREN391=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_match_parens3068)

                    RPAREN391_tree = self._adaptor.createWithPayload(RPAREN391)
                    self._adaptor.addChild(root_0, RPAREN391_tree)

                    self._state.following.append(self.FOLLOW_match_parens_in_match_parens3070)
                    match_parens392 = self.match_parens()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, match_parens392.tree)
                    LPAREN393=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_match_parens3072)

                    LPAREN393_tree = self._adaptor.createWithPayload(LPAREN393)
                    self._adaptor.addChild(root_0, LPAREN393_tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "match_parens"

    class label_name_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.label_name_return, self).__init__()

            self.tree = None




    # $ANTLR start "label_name"
    # sql.g:399:1: label_name : ID ;
    def label_name(self, ):

        retval = self.label_name_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID394 = None

        ID394_tree = None

        try:
            try:
                # sql.g:399:11: ( ID )
                # sql.g:399:13: ID
                pass 
                root_0 = self._adaptor.nil()

                ID394=self.match(self.input, ID, self.FOLLOW_ID_in_label_name3084)

                ID394_tree = self._adaptor.createWithPayload(ID394)
                self._adaptor.addChild(root_0, ID394_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "label_name"

    class expression_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.expression_return, self).__init__()

            self.tree = None




    # $ANTLR start "expression"
    # sql.g:401:1: expression : or_expr ;
    def expression(self, ):

        retval = self.expression_return()
        retval.start = self.input.LT(1)

        root_0 = None

        or_expr395 = None



        try:
            try:
                # sql.g:402:5: ( or_expr )
                # sql.g:402:7: or_expr
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_or_expr_in_expression3096)
                or_expr395 = self.or_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, or_expr395.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "expression"

    class or_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.or_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "or_expr"
    # sql.g:405:1: or_expr : and_expr ( OR and_expr )* ;
    def or_expr(self, ):

        retval = self.or_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        OR397 = None
        and_expr396 = None

        and_expr398 = None


        OR397_tree = None

        try:
            try:
                # sql.g:406:5: ( and_expr ( OR and_expr )* )
                # sql.g:406:7: and_expr ( OR and_expr )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_and_expr_in_or_expr3113)
                and_expr396 = self.and_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, and_expr396.tree)
                # sql.g:406:16: ( OR and_expr )*
                while True: #loop117
                    alt117 = 2
                    LA117_0 = self.input.LA(1)

                    if (LA117_0 == OR) :
                        alt117 = 1


                    if alt117 == 1:
                        # sql.g:406:18: OR and_expr
                        pass 
                        OR397=self.match(self.input, OR, self.FOLLOW_OR_in_or_expr3117)

                        OR397_tree = self._adaptor.createWithPayload(OR397)
                        self._adaptor.addChild(root_0, OR397_tree)

                        self._state.following.append(self.FOLLOW_and_expr_in_or_expr3119)
                        and_expr398 = self.and_expr()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, and_expr398.tree)


                    else:
                        break #loop117



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "or_expr"

    class and_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.and_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "and_expr"
    # sql.g:409:1: and_expr : not_expr ( AND not_expr )* ;
    def and_expr(self, ):

        retval = self.and_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AND400 = None
        not_expr399 = None

        not_expr401 = None


        AND400_tree = None

        try:
            try:
                # sql.g:410:5: ( not_expr ( AND not_expr )* )
                # sql.g:410:7: not_expr ( AND not_expr )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_not_expr_in_and_expr3139)
                not_expr399 = self.not_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, not_expr399.tree)
                # sql.g:410:16: ( AND not_expr )*
                while True: #loop118
                    alt118 = 2
                    LA118_0 = self.input.LA(1)

                    if (LA118_0 == AND) :
                        alt118 = 1


                    if alt118 == 1:
                        # sql.g:410:18: AND not_expr
                        pass 
                        AND400=self.match(self.input, AND, self.FOLLOW_AND_in_and_expr3143)

                        AND400_tree = self._adaptor.createWithPayload(AND400)
                        self._adaptor.addChild(root_0, AND400_tree)

                        self._state.following.append(self.FOLLOW_not_expr_in_and_expr3145)
                        not_expr401 = self.not_expr()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, not_expr401.tree)


                    else:
                        break #loop118



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "and_expr"

    class not_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.not_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "not_expr"
    # sql.g:413:1: not_expr : ( NOT )? compare_expr ;
    def not_expr(self, ):

        retval = self.not_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NOT402 = None
        compare_expr403 = None


        NOT402_tree = None

        try:
            try:
                # sql.g:414:5: ( ( NOT )? compare_expr )
                # sql.g:414:7: ( NOT )? compare_expr
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:414:7: ( NOT )?
                alt119 = 2
                LA119_0 = self.input.LA(1)

                if (LA119_0 == NOT) :
                    alt119 = 1
                if alt119 == 1:
                    # sql.g:414:7: NOT
                    pass 
                    NOT402=self.match(self.input, NOT, self.FOLLOW_NOT_in_not_expr3165)

                    NOT402_tree = self._adaptor.createWithPayload(NOT402)
                    self._adaptor.addChild(root_0, NOT402_tree)




                self._state.following.append(self.FOLLOW_compare_expr_in_not_expr3168)
                compare_expr403 = self.compare_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, compare_expr403.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "not_expr"

    class compare_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.compare_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_expr"
    # sql.g:417:1: compare_expr : is_null_expr ( ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ ) is_null_expr )? ;
    def compare_expr(self, ):

        retval = self.compare_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set405 = None
        is_null_expr404 = None

        is_null_expr406 = None


        set405_tree = None

        try:
            try:
                # sql.g:418:5: ( is_null_expr ( ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ ) is_null_expr )? )
                # sql.g:418:7: is_null_expr ( ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ ) is_null_expr )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_is_null_expr_in_compare_expr3185)
                is_null_expr404 = self.is_null_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, is_null_expr404.tree)
                # sql.g:418:20: ( ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ ) is_null_expr )?
                alt120 = 2
                LA120_0 = self.input.LA(1)

                if ((EQ <= LA120_0 <= GEQ)) :
                    alt120 = 1
                if alt120 == 1:
                    # sql.g:418:22: ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ ) is_null_expr
                    pass 
                    set405 = self.input.LT(1)
                    if (EQ <= self.input.LA(1) <= GEQ):
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set405))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse


                    self._state.following.append(self.FOLLOW_is_null_expr_in_compare_expr3215)
                    is_null_expr406 = self.is_null_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, is_null_expr406.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_expr"

    class is_null_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.is_null_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "is_null_expr"
    # sql.g:421:1: is_null_expr : like_expr ( IS ( NOT )? NULL )? ;
    def is_null_expr(self, ):

        retval = self.is_null_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        IS408 = None
        NOT409 = None
        NULL410 = None
        like_expr407 = None


        IS408_tree = None
        NOT409_tree = None
        NULL410_tree = None

        try:
            try:
                # sql.g:422:5: ( like_expr ( IS ( NOT )? NULL )? )
                # sql.g:422:7: like_expr ( IS ( NOT )? NULL )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_like_expr_in_is_null_expr3235)
                like_expr407 = self.like_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, like_expr407.tree)
                # sql.g:422:17: ( IS ( NOT )? NULL )?
                alt122 = 2
                LA122_0 = self.input.LA(1)

                if (LA122_0 == IS) :
                    alt122 = 1
                if alt122 == 1:
                    # sql.g:422:19: IS ( NOT )? NULL
                    pass 
                    IS408=self.match(self.input, IS, self.FOLLOW_IS_in_is_null_expr3239)

                    IS408_tree = self._adaptor.createWithPayload(IS408)
                    self._adaptor.addChild(root_0, IS408_tree)

                    # sql.g:422:22: ( NOT )?
                    alt121 = 2
                    LA121_0 = self.input.LA(1)

                    if (LA121_0 == NOT) :
                        alt121 = 1
                    if alt121 == 1:
                        # sql.g:422:22: NOT
                        pass 
                        NOT409=self.match(self.input, NOT, self.FOLLOW_NOT_in_is_null_expr3241)

                        NOT409_tree = self._adaptor.createWithPayload(NOT409)
                        self._adaptor.addChild(root_0, NOT409_tree)




                    NULL410=self.match(self.input, NULL, self.FOLLOW_NULL_in_is_null_expr3244)

                    NULL410_tree = self._adaptor.createWithPayload(NULL410)
                    self._adaptor.addChild(root_0, NULL410_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "is_null_expr"

    class like_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.like_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "like_expr"
    # sql.g:425:1: like_expr : between_expr ( ( NOT )? LIKE between_expr )? ;
    def like_expr(self, ):

        retval = self.like_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NOT412 = None
        LIKE413 = None
        between_expr411 = None

        between_expr414 = None


        NOT412_tree = None
        LIKE413_tree = None

        try:
            try:
                # sql.g:426:5: ( between_expr ( ( NOT )? LIKE between_expr )? )
                # sql.g:426:7: between_expr ( ( NOT )? LIKE between_expr )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_between_expr_in_like_expr3263)
                between_expr411 = self.between_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, between_expr411.tree)
                # sql.g:426:20: ( ( NOT )? LIKE between_expr )?
                alt124 = 2
                LA124_0 = self.input.LA(1)

                if (LA124_0 == NOT or LA124_0 == LIKE) :
                    alt124 = 1
                if alt124 == 1:
                    # sql.g:426:22: ( NOT )? LIKE between_expr
                    pass 
                    # sql.g:426:22: ( NOT )?
                    alt123 = 2
                    LA123_0 = self.input.LA(1)

                    if (LA123_0 == NOT) :
                        alt123 = 1
                    if alt123 == 1:
                        # sql.g:426:22: NOT
                        pass 
                        NOT412=self.match(self.input, NOT, self.FOLLOW_NOT_in_like_expr3267)

                        NOT412_tree = self._adaptor.createWithPayload(NOT412)
                        self._adaptor.addChild(root_0, NOT412_tree)




                    LIKE413=self.match(self.input, LIKE, self.FOLLOW_LIKE_in_like_expr3270)

                    LIKE413_tree = self._adaptor.createWithPayload(LIKE413)
                    self._adaptor.addChild(root_0, LIKE413_tree)

                    self._state.following.append(self.FOLLOW_between_expr_in_like_expr3272)
                    between_expr414 = self.between_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, between_expr414.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "like_expr"

    class between_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.between_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "between_expr"
    # sql.g:429:1: between_expr : in_expr ( ( NOT )? BETWEEN in_expr AND in_expr )? ;
    def between_expr(self, ):

        retval = self.between_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NOT416 = None
        BETWEEN417 = None
        AND419 = None
        in_expr415 = None

        in_expr418 = None

        in_expr420 = None


        NOT416_tree = None
        BETWEEN417_tree = None
        AND419_tree = None

        try:
            try:
                # sql.g:430:5: ( in_expr ( ( NOT )? BETWEEN in_expr AND in_expr )? )
                # sql.g:430:7: in_expr ( ( NOT )? BETWEEN in_expr AND in_expr )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_in_expr_in_between_expr3292)
                in_expr415 = self.in_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, in_expr415.tree)
                # sql.g:430:15: ( ( NOT )? BETWEEN in_expr AND in_expr )?
                alt126 = 2
                LA126_0 = self.input.LA(1)

                if (LA126_0 == NOT) :
                    LA126_1 = self.input.LA(2)

                    if (LA126_1 == BETWEEN) :
                        alt126 = 1
                elif (LA126_0 == BETWEEN) :
                    alt126 = 1
                if alt126 == 1:
                    # sql.g:430:17: ( NOT )? BETWEEN in_expr AND in_expr
                    pass 
                    # sql.g:430:17: ( NOT )?
                    alt125 = 2
                    LA125_0 = self.input.LA(1)

                    if (LA125_0 == NOT) :
                        alt125 = 1
                    if alt125 == 1:
                        # sql.g:430:17: NOT
                        pass 
                        NOT416=self.match(self.input, NOT, self.FOLLOW_NOT_in_between_expr3296)

                        NOT416_tree = self._adaptor.createWithPayload(NOT416)
                        self._adaptor.addChild(root_0, NOT416_tree)




                    BETWEEN417=self.match(self.input, BETWEEN, self.FOLLOW_BETWEEN_in_between_expr3299)

                    BETWEEN417_tree = self._adaptor.createWithPayload(BETWEEN417)
                    self._adaptor.addChild(root_0, BETWEEN417_tree)

                    self._state.following.append(self.FOLLOW_in_expr_in_between_expr3301)
                    in_expr418 = self.in_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, in_expr418.tree)
                    AND419=self.match(self.input, AND, self.FOLLOW_AND_in_between_expr3303)

                    AND419_tree = self._adaptor.createWithPayload(AND419)
                    self._adaptor.addChild(root_0, AND419_tree)

                    self._state.following.append(self.FOLLOW_in_expr_in_between_expr3305)
                    in_expr420 = self.in_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, in_expr420.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "between_expr"

    class in_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.in_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "in_expr"
    # sql.g:433:1: in_expr : add_expr ( ( NOT )? IN LPAREN add_expr ( COMMA add_expr )* RPAREN )? ;
    def in_expr(self, ):

        retval = self.in_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NOT422 = None
        IN423 = None
        LPAREN424 = None
        COMMA426 = None
        RPAREN428 = None
        add_expr421 = None

        add_expr425 = None

        add_expr427 = None


        NOT422_tree = None
        IN423_tree = None
        LPAREN424_tree = None
        COMMA426_tree = None
        RPAREN428_tree = None

        try:
            try:
                # sql.g:434:5: ( add_expr ( ( NOT )? IN LPAREN add_expr ( COMMA add_expr )* RPAREN )? )
                # sql.g:434:7: add_expr ( ( NOT )? IN LPAREN add_expr ( COMMA add_expr )* RPAREN )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_add_expr_in_in_expr3325)
                add_expr421 = self.add_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, add_expr421.tree)
                # sql.g:434:16: ( ( NOT )? IN LPAREN add_expr ( COMMA add_expr )* RPAREN )?
                alt129 = 2
                LA129_0 = self.input.LA(1)

                if (LA129_0 == NOT) :
                    LA129_1 = self.input.LA(2)

                    if (LA129_1 == IN) :
                        alt129 = 1
                elif (LA129_0 == IN) :
                    alt129 = 1
                if alt129 == 1:
                    # sql.g:434:18: ( NOT )? IN LPAREN add_expr ( COMMA add_expr )* RPAREN
                    pass 
                    # sql.g:434:18: ( NOT )?
                    alt127 = 2
                    LA127_0 = self.input.LA(1)

                    if (LA127_0 == NOT) :
                        alt127 = 1
                    if alt127 == 1:
                        # sql.g:434:18: NOT
                        pass 
                        NOT422=self.match(self.input, NOT, self.FOLLOW_NOT_in_in_expr3329)

                        NOT422_tree = self._adaptor.createWithPayload(NOT422)
                        self._adaptor.addChild(root_0, NOT422_tree)




                    IN423=self.match(self.input, IN, self.FOLLOW_IN_in_in_expr3332)

                    IN423_tree = self._adaptor.createWithPayload(IN423)
                    self._adaptor.addChild(root_0, IN423_tree)

                    LPAREN424=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_in_expr3334)

                    LPAREN424_tree = self._adaptor.createWithPayload(LPAREN424)
                    self._adaptor.addChild(root_0, LPAREN424_tree)

                    self._state.following.append(self.FOLLOW_add_expr_in_in_expr3336)
                    add_expr425 = self.add_expr()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, add_expr425.tree)
                    # sql.g:434:42: ( COMMA add_expr )*
                    while True: #loop128
                        alt128 = 2
                        LA128_0 = self.input.LA(1)

                        if (LA128_0 == COMMA) :
                            alt128 = 1


                        if alt128 == 1:
                            # sql.g:434:44: COMMA add_expr
                            pass 
                            COMMA426=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_in_expr3340)

                            COMMA426_tree = self._adaptor.createWithPayload(COMMA426)
                            self._adaptor.addChild(root_0, COMMA426_tree)

                            self._state.following.append(self.FOLLOW_add_expr_in_in_expr3342)
                            add_expr427 = self.add_expr()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, add_expr427.tree)


                        else:
                            break #loop128
                    RPAREN428=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_in_expr3347)

                    RPAREN428_tree = self._adaptor.createWithPayload(RPAREN428)
                    self._adaptor.addChild(root_0, RPAREN428_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "in_expr"

    class numeric_expression_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.numeric_expression_return, self).__init__()

            self.tree = None




    # $ANTLR start "numeric_expression"
    # sql.g:437:1: numeric_expression : add_expr ;
    def numeric_expression(self, ):

        retval = self.numeric_expression_return()
        retval.start = self.input.LT(1)

        root_0 = None

        add_expr429 = None



        try:
            try:
                # sql.g:438:5: ( add_expr )
                # sql.g:438:7: add_expr
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_add_expr_in_numeric_expression3367)
                add_expr429 = self.add_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, add_expr429.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "numeric_expression"

    class add_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.add_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "add_expr"
    # sql.g:441:1: add_expr : mul_expr ( ( MINUS | PLUS | DOUBLEVERTBAR ) mul_expr )* ;
    def add_expr(self, ):

        retval = self.add_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set431 = None
        mul_expr430 = None

        mul_expr432 = None


        set431_tree = None

        try:
            try:
                # sql.g:442:5: ( mul_expr ( ( MINUS | PLUS | DOUBLEVERTBAR ) mul_expr )* )
                # sql.g:442:7: mul_expr ( ( MINUS | PLUS | DOUBLEVERTBAR ) mul_expr )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_mul_expr_in_add_expr3384)
                mul_expr430 = self.mul_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, mul_expr430.tree)
                # sql.g:442:16: ( ( MINUS | PLUS | DOUBLEVERTBAR ) mul_expr )*
                while True: #loop130
                    alt130 = 2
                    LA130_0 = self.input.LA(1)

                    if ((MINUS <= LA130_0 <= DOUBLEVERTBAR)) :
                        alt130 = 1


                    if alt130 == 1:
                        # sql.g:442:18: ( MINUS | PLUS | DOUBLEVERTBAR ) mul_expr
                        pass 
                        set431 = self.input.LT(1)
                        if (MINUS <= self.input.LA(1) <= DOUBLEVERTBAR):
                            self.input.consume()
                            self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set431))
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse


                        self._state.following.append(self.FOLLOW_mul_expr_in_add_expr3402)
                        mul_expr432 = self.mul_expr()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, mul_expr432.tree)


                    else:
                        break #loop130



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "add_expr"

    class mul_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.mul_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "mul_expr"
    # sql.g:445:1: mul_expr : unary_sign_expr ( ( ASTERISK | DIVIDE | kMOD ) unary_sign_expr )* ;
    def mul_expr(self, ):

        retval = self.mul_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ASTERISK434 = None
        DIVIDE435 = None
        unary_sign_expr433 = None

        kMOD436 = None

        unary_sign_expr437 = None


        ASTERISK434_tree = None
        DIVIDE435_tree = None

        try:
            try:
                # sql.g:446:5: ( unary_sign_expr ( ( ASTERISK | DIVIDE | kMOD ) unary_sign_expr )* )
                # sql.g:446:7: unary_sign_expr ( ( ASTERISK | DIVIDE | kMOD ) unary_sign_expr )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_unary_sign_expr_in_mul_expr3422)
                unary_sign_expr433 = self.unary_sign_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, unary_sign_expr433.tree)
                # sql.g:446:23: ( ( ASTERISK | DIVIDE | kMOD ) unary_sign_expr )*
                while True: #loop132
                    alt132 = 2
                    LA132_0 = self.input.LA(1)

                    if (LA132_0 == DIVIDE or LA132_0 == ID or LA132_0 == ASTERISK) :
                        alt132 = 1


                    if alt132 == 1:
                        # sql.g:446:25: ( ASTERISK | DIVIDE | kMOD ) unary_sign_expr
                        pass 
                        # sql.g:446:25: ( ASTERISK | DIVIDE | kMOD )
                        alt131 = 3
                        LA131 = self.input.LA(1)
                        if LA131 == ASTERISK:
                            alt131 = 1
                        elif LA131 == DIVIDE:
                            alt131 = 2
                        elif LA131 == ID:
                            alt131 = 3
                        else:
                            nvae = NoViableAltException("", 131, 0, self.input)

                            raise nvae

                        if alt131 == 1:
                            # sql.g:446:27: ASTERISK
                            pass 
                            ASTERISK434=self.match(self.input, ASTERISK, self.FOLLOW_ASTERISK_in_mul_expr3428)

                            ASTERISK434_tree = self._adaptor.createWithPayload(ASTERISK434)
                            self._adaptor.addChild(root_0, ASTERISK434_tree)



                        elif alt131 == 2:
                            # sql.g:446:38: DIVIDE
                            pass 
                            DIVIDE435=self.match(self.input, DIVIDE, self.FOLLOW_DIVIDE_in_mul_expr3432)

                            DIVIDE435_tree = self._adaptor.createWithPayload(DIVIDE435)
                            self._adaptor.addChild(root_0, DIVIDE435_tree)



                        elif alt131 == 3:
                            # sql.g:446:47: kMOD
                            pass 
                            self._state.following.append(self.FOLLOW_kMOD_in_mul_expr3436)
                            kMOD436 = self.kMOD()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, kMOD436.tree)



                        self._state.following.append(self.FOLLOW_unary_sign_expr_in_mul_expr3440)
                        unary_sign_expr437 = self.unary_sign_expr()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, unary_sign_expr437.tree)


                    else:
                        break #loop132



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "mul_expr"

    class unary_sign_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.unary_sign_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "unary_sign_expr"
    # sql.g:449:1: unary_sign_expr : ( MINUS | PLUS )? exponent_expr ;
    def unary_sign_expr(self, ):

        retval = self.unary_sign_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set438 = None
        exponent_expr439 = None


        set438_tree = None

        try:
            try:
                # sql.g:450:5: ( ( MINUS | PLUS )? exponent_expr )
                # sql.g:450:7: ( MINUS | PLUS )? exponent_expr
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:450:7: ( MINUS | PLUS )?
                alt133 = 2
                LA133_0 = self.input.LA(1)

                if ((MINUS <= LA133_0 <= PLUS)) :
                    alt133 = 1
                if alt133 == 1:
                    # sql.g:
                    pass 
                    set438 = self.input.LT(1)
                    if (MINUS <= self.input.LA(1) <= PLUS):
                        self.input.consume()
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set438))
                        self._state.errorRecovery = False

                    else:
                        mse = MismatchedSetException(None, self.input)
                        raise mse





                self._state.following.append(self.FOLLOW_exponent_expr_in_unary_sign_expr3471)
                exponent_expr439 = self.exponent_expr()

                self._state.following.pop()
                self._adaptor.addChild(root_0, exponent_expr439.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "unary_sign_expr"

    class exponent_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.exponent_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "exponent_expr"
    # sql.g:453:1: exponent_expr : atom ( EXPONENT atom )? ;
    def exponent_expr(self, ):

        retval = self.exponent_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        EXPONENT441 = None
        atom440 = None

        atom442 = None


        EXPONENT441_tree = None

        try:
            try:
                # sql.g:454:5: ( atom ( EXPONENT atom )? )
                # sql.g:454:7: atom ( EXPONENT atom )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_atom_in_exponent_expr3488)
                atom440 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom440.tree)
                # sql.g:454:12: ( EXPONENT atom )?
                alt134 = 2
                LA134_0 = self.input.LA(1)

                if (LA134_0 == EXPONENT) :
                    alt134 = 1
                if alt134 == 1:
                    # sql.g:454:14: EXPONENT atom
                    pass 
                    EXPONENT441=self.match(self.input, EXPONENT, self.FOLLOW_EXPONENT_in_exponent_expr3492)

                    EXPONENT441_tree = self._adaptor.createWithPayload(EXPONENT441)
                    self._adaptor.addChild(root_0, EXPONENT441_tree)

                    self._state.following.append(self.FOLLOW_atom_in_exponent_expr3494)
                    atom442 = self.atom()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, atom442.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "exponent_expr"

    class atom_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.atom_return, self).__init__()

            self.tree = None




    # $ANTLR start "atom"
    # sql.g:457:1: atom : ( variable_or_function_call ( PERCENT attribute )? | SQL PERCENT attribute | string_literal | numeric_atom | boolean_atom | NULL | LPAREN expression RPAREN );
    def atom(self, ):

        retval = self.atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PERCENT444 = None
        SQL446 = None
        PERCENT447 = None
        NULL452 = None
        LPAREN453 = None
        RPAREN455 = None
        variable_or_function_call443 = None

        attribute445 = None

        attribute448 = None

        string_literal449 = None

        numeric_atom450 = None

        boolean_atom451 = None

        expression454 = None


        PERCENT444_tree = None
        SQL446_tree = None
        PERCENT447_tree = None
        NULL452_tree = None
        LPAREN453_tree = None
        RPAREN455_tree = None

        try:
            try:
                # sql.g:458:5: ( variable_or_function_call ( PERCENT attribute )? | SQL PERCENT attribute | string_literal | numeric_atom | boolean_atom | NULL | LPAREN expression RPAREN )
                alt136 = 7
                alt136 = self.dfa136.predict(self.input)
                if alt136 == 1:
                    # sql.g:458:7: variable_or_function_call ( PERCENT attribute )?
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_variable_or_function_call_in_atom3514)
                    variable_or_function_call443 = self.variable_or_function_call()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, variable_or_function_call443.tree)
                    # sql.g:458:33: ( PERCENT attribute )?
                    alt135 = 2
                    LA135_0 = self.input.LA(1)

                    if (LA135_0 == PERCENT) :
                        alt135 = 1
                    if alt135 == 1:
                        # sql.g:458:35: PERCENT attribute
                        pass 
                        PERCENT444=self.match(self.input, PERCENT, self.FOLLOW_PERCENT_in_atom3518)

                        PERCENT444_tree = self._adaptor.createWithPayload(PERCENT444)
                        self._adaptor.addChild(root_0, PERCENT444_tree)

                        self._state.following.append(self.FOLLOW_attribute_in_atom3520)
                        attribute445 = self.attribute()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, attribute445.tree)





                elif alt136 == 2:
                    # sql.g:459:7: SQL PERCENT attribute
                    pass 
                    root_0 = self._adaptor.nil()

                    SQL446=self.match(self.input, SQL, self.FOLLOW_SQL_in_atom3531)

                    SQL446_tree = self._adaptor.createWithPayload(SQL446)
                    self._adaptor.addChild(root_0, SQL446_tree)

                    PERCENT447=self.match(self.input, PERCENT, self.FOLLOW_PERCENT_in_atom3533)

                    PERCENT447_tree = self._adaptor.createWithPayload(PERCENT447)
                    self._adaptor.addChild(root_0, PERCENT447_tree)

                    self._state.following.append(self.FOLLOW_attribute_in_atom3535)
                    attribute448 = self.attribute()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, attribute448.tree)


                elif alt136 == 3:
                    # sql.g:460:7: string_literal
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_string_literal_in_atom3543)
                    string_literal449 = self.string_literal()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, string_literal449.tree)


                elif alt136 == 4:
                    # sql.g:461:7: numeric_atom
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_numeric_atom_in_atom3551)
                    numeric_atom450 = self.numeric_atom()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, numeric_atom450.tree)


                elif alt136 == 5:
                    # sql.g:462:7: boolean_atom
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_boolean_atom_in_atom3559)
                    boolean_atom451 = self.boolean_atom()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, boolean_atom451.tree)


                elif alt136 == 6:
                    # sql.g:463:7: NULL
                    pass 
                    root_0 = self._adaptor.nil()

                    NULL452=self.match(self.input, NULL, self.FOLLOW_NULL_in_atom3567)

                    NULL452_tree = self._adaptor.createWithPayload(NULL452)
                    self._adaptor.addChild(root_0, NULL452_tree)



                elif alt136 == 7:
                    # sql.g:464:7: LPAREN expression RPAREN
                    pass 
                    root_0 = self._adaptor.nil()

                    LPAREN453=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_atom3575)

                    LPAREN453_tree = self._adaptor.createWithPayload(LPAREN453)
                    self._adaptor.addChild(root_0, LPAREN453_tree)

                    self._state.following.append(self.FOLLOW_expression_in_atom3577)
                    expression454 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression454.tree)
                    RPAREN455=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_atom3579)

                    RPAREN455_tree = self._adaptor.createWithPayload(RPAREN455)
                    self._adaptor.addChild(root_0, RPAREN455_tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "atom"

    class variable_or_function_call_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.variable_or_function_call_return, self).__init__()

            self.tree = None




    # $ANTLR start "variable_or_function_call"
    # sql.g:467:1: variable_or_function_call : call ( DOT call )* ( DOT delete_call )? ;
    def variable_or_function_call(self, ):

        retval = self.variable_or_function_call_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DOT457 = None
        DOT459 = None
        call456 = None

        call458 = None

        delete_call460 = None


        DOT457_tree = None
        DOT459_tree = None

        try:
            try:
                # sql.g:468:5: ( call ( DOT call )* ( DOT delete_call )? )
                # sql.g:468:7: call ( DOT call )* ( DOT delete_call )?
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_call_in_variable_or_function_call3600)
                call456 = self.call()

                self._state.following.pop()
                self._adaptor.addChild(root_0, call456.tree)
                # sql.g:468:12: ( DOT call )*
                while True: #loop137
                    alt137 = 2
                    LA137_0 = self.input.LA(1)

                    if (LA137_0 == DOT) :
                        LA137_1 = self.input.LA(2)

                        if (LA137_1 == ID or LA137_1 == COLON) :
                            alt137 = 1




                    if alt137 == 1:
                        # sql.g:468:14: DOT call
                        pass 
                        DOT457=self.match(self.input, DOT, self.FOLLOW_DOT_in_variable_or_function_call3604)

                        DOT457_tree = self._adaptor.createWithPayload(DOT457)
                        self._adaptor.addChild(root_0, DOT457_tree)

                        self._state.following.append(self.FOLLOW_call_in_variable_or_function_call3606)
                        call458 = self.call()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, call458.tree)


                    else:
                        break #loop137
                # sql.g:468:26: ( DOT delete_call )?
                alt138 = 2
                LA138_0 = self.input.LA(1)

                if (LA138_0 == DOT) :
                    alt138 = 1
                if alt138 == 1:
                    # sql.g:468:28: DOT delete_call
                    pass 
                    DOT459=self.match(self.input, DOT, self.FOLLOW_DOT_in_variable_or_function_call3613)

                    DOT459_tree = self._adaptor.createWithPayload(DOT459)
                    self._adaptor.addChild(root_0, DOT459_tree)

                    self._state.following.append(self.FOLLOW_delete_call_in_variable_or_function_call3615)
                    delete_call460 = self.delete_call()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, delete_call460.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "variable_or_function_call"

    class attribute_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.attribute_return, self).__init__()

            self.tree = None




    # $ANTLR start "attribute"
    # sql.g:471:1: attribute : ( BULK_ROWCOUNT LPAREN expression RPAREN | kFOUND | ISOPEN | NOTFOUND | kROWCOUNT );
    def attribute(self, ):

        retval = self.attribute_return()
        retval.start = self.input.LT(1)

        root_0 = None

        BULK_ROWCOUNT461 = None
        LPAREN462 = None
        RPAREN464 = None
        ISOPEN466 = None
        NOTFOUND467 = None
        expression463 = None

        kFOUND465 = None

        kROWCOUNT468 = None


        BULK_ROWCOUNT461_tree = None
        LPAREN462_tree = None
        RPAREN464_tree = None
        ISOPEN466_tree = None
        NOTFOUND467_tree = None

        try:
            try:
                # sql.g:472:5: ( BULK_ROWCOUNT LPAREN expression RPAREN | kFOUND | ISOPEN | NOTFOUND | kROWCOUNT )
                alt139 = 5
                LA139 = self.input.LA(1)
                if LA139 == BULK_ROWCOUNT:
                    alt139 = 1
                elif LA139 == ID:
                    LA139_2 = self.input.LA(2)

                    if ((self.input.LT(1).text.lower() == "found")) :
                        alt139 = 2
                    elif ((self.input.LT(1).text.lower() == "rowcount")) :
                        alt139 = 5
                    else:
                        nvae = NoViableAltException("", 139, 2, self.input)

                        raise nvae

                elif LA139 == ISOPEN:
                    alt139 = 3
                elif LA139 == NOTFOUND:
                    alt139 = 4
                else:
                    nvae = NoViableAltException("", 139, 0, self.input)

                    raise nvae

                if alt139 == 1:
                    # sql.g:472:7: BULK_ROWCOUNT LPAREN expression RPAREN
                    pass 
                    root_0 = self._adaptor.nil()

                    BULK_ROWCOUNT461=self.match(self.input, BULK_ROWCOUNT, self.FOLLOW_BULK_ROWCOUNT_in_attribute3635)

                    BULK_ROWCOUNT461_tree = self._adaptor.createWithPayload(BULK_ROWCOUNT461)
                    self._adaptor.addChild(root_0, BULK_ROWCOUNT461_tree)

                    LPAREN462=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_attribute3637)

                    LPAREN462_tree = self._adaptor.createWithPayload(LPAREN462)
                    self._adaptor.addChild(root_0, LPAREN462_tree)

                    self._state.following.append(self.FOLLOW_expression_in_attribute3639)
                    expression463 = self.expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expression463.tree)
                    RPAREN464=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_attribute3641)

                    RPAREN464_tree = self._adaptor.createWithPayload(RPAREN464)
                    self._adaptor.addChild(root_0, RPAREN464_tree)



                elif alt139 == 2:
                    # sql.g:473:7: kFOUND
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_kFOUND_in_attribute3649)
                    kFOUND465 = self.kFOUND()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kFOUND465.tree)


                elif alt139 == 3:
                    # sql.g:474:7: ISOPEN
                    pass 
                    root_0 = self._adaptor.nil()

                    ISOPEN466=self.match(self.input, ISOPEN, self.FOLLOW_ISOPEN_in_attribute3657)

                    ISOPEN466_tree = self._adaptor.createWithPayload(ISOPEN466)
                    self._adaptor.addChild(root_0, ISOPEN466_tree)



                elif alt139 == 4:
                    # sql.g:475:7: NOTFOUND
                    pass 
                    root_0 = self._adaptor.nil()

                    NOTFOUND467=self.match(self.input, NOTFOUND, self.FOLLOW_NOTFOUND_in_attribute3665)

                    NOTFOUND467_tree = self._adaptor.createWithPayload(NOTFOUND467)
                    self._adaptor.addChild(root_0, NOTFOUND467_tree)



                elif alt139 == 5:
                    # sql.g:476:7: kROWCOUNT
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_kROWCOUNT_in_attribute3673)
                    kROWCOUNT468 = self.kROWCOUNT()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kROWCOUNT468.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "attribute"

    class call_args_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.call_args_return, self).__init__()

            self.tree = None




    # $ANTLR start "call_args"
    # sql.g:479:1: call_args : LPAREN ( parameter ( COMMA parameter )* )? RPAREN ;
    def call_args(self, ):

        retval = self.call_args_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LPAREN469 = None
        COMMA471 = None
        RPAREN473 = None
        parameter470 = None

        parameter472 = None


        LPAREN469_tree = None
        COMMA471_tree = None
        RPAREN473_tree = None

        try:
            try:
                # sql.g:480:5: ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN )
                # sql.g:480:7: LPAREN ( parameter ( COMMA parameter )* )? RPAREN
                pass 
                root_0 = self._adaptor.nil()

                LPAREN469=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_call_args3690)

                LPAREN469_tree = self._adaptor.createWithPayload(LPAREN469)
                self._adaptor.addChild(root_0, LPAREN469_tree)

                # sql.g:480:14: ( parameter ( COMMA parameter )* )?
                alt141 = 2
                LA141_0 = self.input.LA(1)

                if (LA141_0 == ID or LA141_0 == LPAREN or (NOT <= LA141_0 <= NULL) or LA141_0 == COLON or (MINUS <= LA141_0 <= PLUS) or LA141_0 == SQL or (INTEGER <= LA141_0 <= QUOTED_STRING) or (INSERTING <= LA141_0 <= DELETING)) :
                    alt141 = 1
                if alt141 == 1:
                    # sql.g:480:16: parameter ( COMMA parameter )*
                    pass 
                    self._state.following.append(self.FOLLOW_parameter_in_call_args3694)
                    parameter470 = self.parameter()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, parameter470.tree)
                    # sql.g:480:26: ( COMMA parameter )*
                    while True: #loop140
                        alt140 = 2
                        LA140_0 = self.input.LA(1)

                        if (LA140_0 == COMMA) :
                            alt140 = 1


                        if alt140 == 1:
                            # sql.g:480:28: COMMA parameter
                            pass 
                            COMMA471=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_call_args3698)

                            COMMA471_tree = self._adaptor.createWithPayload(COMMA471)
                            self._adaptor.addChild(root_0, COMMA471_tree)

                            self._state.following.append(self.FOLLOW_parameter_in_call_args3700)
                            parameter472 = self.parameter()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, parameter472.tree)


                        else:
                            break #loop140



                RPAREN473=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_call_args3708)

                RPAREN473_tree = self._adaptor.createWithPayload(RPAREN473)
                self._adaptor.addChild(root_0, RPAREN473_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "call_args"

    class boolean_atom_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.boolean_atom_return, self).__init__()

            self.tree = None




    # $ANTLR start "boolean_atom"
    # sql.g:483:1: boolean_atom : ( boolean_literal | collection_exists | conditional_predicate );
    def boolean_atom(self, ):

        retval = self.boolean_atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        boolean_literal474 = None

        collection_exists475 = None

        conditional_predicate476 = None



        try:
            try:
                # sql.g:484:5: ( boolean_literal | collection_exists | conditional_predicate )
                alt142 = 3
                LA142 = self.input.LA(1)
                if LA142 == TRUE or LA142 == FALSE:
                    alt142 = 1
                elif LA142 == ID:
                    alt142 = 2
                elif LA142 == INSERTING or LA142 == UPDATING or LA142 == DELETING:
                    alt142 = 3
                else:
                    nvae = NoViableAltException("", 142, 0, self.input)

                    raise nvae

                if alt142 == 1:
                    # sql.g:484:7: boolean_literal
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_boolean_literal_in_boolean_atom3725)
                    boolean_literal474 = self.boolean_literal()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, boolean_literal474.tree)


                elif alt142 == 2:
                    # sql.g:485:7: collection_exists
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_collection_exists_in_boolean_atom3733)
                    collection_exists475 = self.collection_exists()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, collection_exists475.tree)


                elif alt142 == 3:
                    # sql.g:486:7: conditional_predicate
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_conditional_predicate_in_boolean_atom3741)
                    conditional_predicate476 = self.conditional_predicate()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, conditional_predicate476.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "boolean_atom"

    class numeric_atom_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.numeric_atom_return, self).__init__()

            self.tree = None




    # $ANTLR start "numeric_atom"
    # sql.g:489:1: numeric_atom : numeric_literal ;
    def numeric_atom(self, ):

        retval = self.numeric_atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        numeric_literal477 = None



        try:
            try:
                # sql.g:490:5: ( numeric_literal )
                # sql.g:490:7: numeric_literal
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_numeric_literal_in_numeric_atom3758)
                numeric_literal477 = self.numeric_literal()

                self._state.following.pop()
                self._adaptor.addChild(root_0, numeric_literal477.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "numeric_atom"

    class numeric_literal_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.numeric_literal_return, self).__init__()

            self.tree = None




    # $ANTLR start "numeric_literal"
    # sql.g:493:1: numeric_literal : ( INTEGER | REAL_NUMBER );
    def numeric_literal(self, ):

        retval = self.numeric_literal_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set478 = None

        set478_tree = None

        try:
            try:
                # sql.g:494:5: ( INTEGER | REAL_NUMBER )
                # sql.g:
                pass 
                root_0 = self._adaptor.nil()

                set478 = self.input.LT(1)
                if (INTEGER <= self.input.LA(1) <= REAL_NUMBER):
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set478))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "numeric_literal"

    class boolean_literal_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.boolean_literal_return, self).__init__()

            self.tree = None




    # $ANTLR start "boolean_literal"
    # sql.g:498:1: boolean_literal : ( TRUE | FALSE );
    def boolean_literal(self, ):

        retval = self.boolean_literal_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set479 = None

        set479_tree = None

        try:
            try:
                # sql.g:499:5: ( TRUE | FALSE )
                # sql.g:
                pass 
                root_0 = self._adaptor.nil()

                set479 = self.input.LT(1)
                if (TRUE <= self.input.LA(1) <= FALSE):
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set479))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "boolean_literal"

    class string_literal_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.string_literal_return, self).__init__()

            self.tree = None




    # $ANTLR start "string_literal"
    # sql.g:503:1: string_literal : QUOTED_STRING ;
    def string_literal(self, ):

        retval = self.string_literal_return()
        retval.start = self.input.LT(1)

        root_0 = None

        QUOTED_STRING480 = None

        QUOTED_STRING480_tree = None

        try:
            try:
                # sql.g:504:5: ( QUOTED_STRING )
                # sql.g:504:7: QUOTED_STRING
                pass 
                root_0 = self._adaptor.nil()

                QUOTED_STRING480=self.match(self.input, QUOTED_STRING, self.FOLLOW_QUOTED_STRING_in_string_literal3825)

                QUOTED_STRING480_tree = self._adaptor.createWithPayload(QUOTED_STRING480)
                self._adaptor.addChild(root_0, QUOTED_STRING480_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "string_literal"

    class collection_exists_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.collection_exists_return, self).__init__()

            self.tree = None




    # $ANTLR start "collection_exists"
    # sql.g:507:1: collection_exists : ID DOT EXISTS LPAREN expression RPAREN ;
    def collection_exists(self, ):

        retval = self.collection_exists_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID481 = None
        DOT482 = None
        EXISTS483 = None
        LPAREN484 = None
        RPAREN486 = None
        expression485 = None


        ID481_tree = None
        DOT482_tree = None
        EXISTS483_tree = None
        LPAREN484_tree = None
        RPAREN486_tree = None

        try:
            try:
                # sql.g:508:5: ( ID DOT EXISTS LPAREN expression RPAREN )
                # sql.g:508:7: ID DOT EXISTS LPAREN expression RPAREN
                pass 
                root_0 = self._adaptor.nil()

                ID481=self.match(self.input, ID, self.FOLLOW_ID_in_collection_exists3842)

                ID481_tree = self._adaptor.createWithPayload(ID481)
                self._adaptor.addChild(root_0, ID481_tree)

                DOT482=self.match(self.input, DOT, self.FOLLOW_DOT_in_collection_exists3844)

                DOT482_tree = self._adaptor.createWithPayload(DOT482)
                self._adaptor.addChild(root_0, DOT482_tree)

                EXISTS483=self.match(self.input, EXISTS, self.FOLLOW_EXISTS_in_collection_exists3846)

                EXISTS483_tree = self._adaptor.createWithPayload(EXISTS483)
                self._adaptor.addChild(root_0, EXISTS483_tree)

                LPAREN484=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_collection_exists3848)

                LPAREN484_tree = self._adaptor.createWithPayload(LPAREN484)
                self._adaptor.addChild(root_0, LPAREN484_tree)

                self._state.following.append(self.FOLLOW_expression_in_collection_exists3850)
                expression485 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression485.tree)
                RPAREN486=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_collection_exists3852)

                RPAREN486_tree = self._adaptor.createWithPayload(RPAREN486)
                self._adaptor.addChild(root_0, RPAREN486_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "collection_exists"

    class conditional_predicate_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.conditional_predicate_return, self).__init__()

            self.tree = None




    # $ANTLR start "conditional_predicate"
    # sql.g:511:1: conditional_predicate : ( INSERTING | UPDATING ( LPAREN QUOTED_STRING RPAREN )? | DELETING );
    def conditional_predicate(self, ):

        retval = self.conditional_predicate_return()
        retval.start = self.input.LT(1)

        root_0 = None

        INSERTING487 = None
        UPDATING488 = None
        LPAREN489 = None
        QUOTED_STRING490 = None
        RPAREN491 = None
        DELETING492 = None

        INSERTING487_tree = None
        UPDATING488_tree = None
        LPAREN489_tree = None
        QUOTED_STRING490_tree = None
        RPAREN491_tree = None
        DELETING492_tree = None

        try:
            try:
                # sql.g:512:5: ( INSERTING | UPDATING ( LPAREN QUOTED_STRING RPAREN )? | DELETING )
                alt144 = 3
                LA144 = self.input.LA(1)
                if LA144 == INSERTING:
                    alt144 = 1
                elif LA144 == UPDATING:
                    alt144 = 2
                elif LA144 == DELETING:
                    alt144 = 3
                else:
                    nvae = NoViableAltException("", 144, 0, self.input)

                    raise nvae

                if alt144 == 1:
                    # sql.g:512:7: INSERTING
                    pass 
                    root_0 = self._adaptor.nil()

                    INSERTING487=self.match(self.input, INSERTING, self.FOLLOW_INSERTING_in_conditional_predicate3869)

                    INSERTING487_tree = self._adaptor.createWithPayload(INSERTING487)
                    self._adaptor.addChild(root_0, INSERTING487_tree)



                elif alt144 == 2:
                    # sql.g:513:7: UPDATING ( LPAREN QUOTED_STRING RPAREN )?
                    pass 
                    root_0 = self._adaptor.nil()

                    UPDATING488=self.match(self.input, UPDATING, self.FOLLOW_UPDATING_in_conditional_predicate3877)

                    UPDATING488_tree = self._adaptor.createWithPayload(UPDATING488)
                    self._adaptor.addChild(root_0, UPDATING488_tree)

                    # sql.g:513:16: ( LPAREN QUOTED_STRING RPAREN )?
                    alt143 = 2
                    LA143_0 = self.input.LA(1)

                    if (LA143_0 == LPAREN) :
                        alt143 = 1
                    if alt143 == 1:
                        # sql.g:513:18: LPAREN QUOTED_STRING RPAREN
                        pass 
                        LPAREN489=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_conditional_predicate3881)

                        LPAREN489_tree = self._adaptor.createWithPayload(LPAREN489)
                        self._adaptor.addChild(root_0, LPAREN489_tree)

                        QUOTED_STRING490=self.match(self.input, QUOTED_STRING, self.FOLLOW_QUOTED_STRING_in_conditional_predicate3883)

                        QUOTED_STRING490_tree = self._adaptor.createWithPayload(QUOTED_STRING490)
                        self._adaptor.addChild(root_0, QUOTED_STRING490_tree)

                        RPAREN491=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_conditional_predicate3885)

                        RPAREN491_tree = self._adaptor.createWithPayload(RPAREN491)
                        self._adaptor.addChild(root_0, RPAREN491_tree)






                elif alt144 == 3:
                    # sql.g:514:7: DELETING
                    pass 
                    root_0 = self._adaptor.nil()

                    DELETING492=self.match(self.input, DELETING, self.FOLLOW_DELETING_in_conditional_predicate3896)

                    DELETING492_tree = self._adaptor.createWithPayload(DELETING492)
                    self._adaptor.addChild(root_0, DELETING492_tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "conditional_predicate"

    class parameter_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.parameter_return, self).__init__()

            self.tree = None




    # $ANTLR start "parameter"
    # sql.g:517:1: parameter : ( ID ARROW )? expression ;
    def parameter(self, ):

        retval = self.parameter_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID493 = None
        ARROW494 = None
        expression495 = None


        ID493_tree = None
        ARROW494_tree = None

        try:
            try:
                # sql.g:518:5: ( ( ID ARROW )? expression )
                # sql.g:518:7: ( ID ARROW )? expression
                pass 
                root_0 = self._adaptor.nil()

                # sql.g:518:7: ( ID ARROW )?
                alt145 = 2
                LA145_0 = self.input.LA(1)

                if (LA145_0 == ID) :
                    LA145_1 = self.input.LA(2)

                    if (LA145_1 == ARROW) :
                        alt145 = 1
                if alt145 == 1:
                    # sql.g:518:9: ID ARROW
                    pass 
                    ID493=self.match(self.input, ID, self.FOLLOW_ID_in_parameter3915)

                    ID493_tree = self._adaptor.createWithPayload(ID493)
                    self._adaptor.addChild(root_0, ID493_tree)

                    ARROW494=self.match(self.input, ARROW, self.FOLLOW_ARROW_in_parameter3917)

                    ARROW494_tree = self._adaptor.createWithPayload(ARROW494)
                    self._adaptor.addChild(root_0, ARROW494_tree)




                self._state.following.append(self.FOLLOW_expression_in_parameter3922)
                expression495 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression495.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "parameter"

    class index_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.index_return, self).__init__()

            self.tree = None




    # $ANTLR start "index"
    # sql.g:521:1: index : expression ;
    def index(self, ):

        retval = self.index_return()
        retval.start = self.input.LT(1)

        root_0 = None

        expression496 = None



        try:
            try:
                # sql.g:522:5: ( expression )
                # sql.g:522:7: expression
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_expression_in_index3939)
                expression496 = self.expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, expression496.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "index"

    class create_package_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.create_package_return, self).__init__()

            self.tree = None




    # $ANTLR start "create_package"
    # sql.g:525:1: create_package : CREATE ( OR kREPLACE )? PACKAGE (schema_name= ID DOT )? package_name= ID ( invoker_rights_clause )? ( IS | AS ) ( declare_section )? END ( ID )? SEMI ;
    def create_package(self, ):

        retval = self.create_package_return()
        retval.start = self.input.LT(1)

        root_0 = None

        schema_name = None
        package_name = None
        CREATE497 = None
        OR498 = None
        PACKAGE500 = None
        DOT501 = None
        set503 = None
        END505 = None
        ID506 = None
        SEMI507 = None
        kREPLACE499 = None

        invoker_rights_clause502 = None

        declare_section504 = None


        schema_name_tree = None
        package_name_tree = None
        CREATE497_tree = None
        OR498_tree = None
        PACKAGE500_tree = None
        DOT501_tree = None
        set503_tree = None
        END505_tree = None
        ID506_tree = None
        SEMI507_tree = None

        try:
            try:
                # sql.g:525:16: ( CREATE ( OR kREPLACE )? PACKAGE (schema_name= ID DOT )? package_name= ID ( invoker_rights_clause )? ( IS | AS ) ( declare_section )? END ( ID )? SEMI )
                # sql.g:526:9: CREATE ( OR kREPLACE )? PACKAGE (schema_name= ID DOT )? package_name= ID ( invoker_rights_clause )? ( IS | AS ) ( declare_section )? END ( ID )? SEMI
                pass 
                root_0 = self._adaptor.nil()

                CREATE497=self.match(self.input, CREATE, self.FOLLOW_CREATE_in_create_package3960)

                CREATE497_tree = self._adaptor.createWithPayload(CREATE497)
                self._adaptor.addChild(root_0, CREATE497_tree)

                # sql.g:526:16: ( OR kREPLACE )?
                alt146 = 2
                LA146_0 = self.input.LA(1)

                if (LA146_0 == OR) :
                    alt146 = 1
                if alt146 == 1:
                    # sql.g:526:18: OR kREPLACE
                    pass 
                    OR498=self.match(self.input, OR, self.FOLLOW_OR_in_create_package3964)

                    OR498_tree = self._adaptor.createWithPayload(OR498)
                    self._adaptor.addChild(root_0, OR498_tree)

                    self._state.following.append(self.FOLLOW_kREPLACE_in_create_package3966)
                    kREPLACE499 = self.kREPLACE()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kREPLACE499.tree)



                PACKAGE500=self.match(self.input, PACKAGE, self.FOLLOW_PACKAGE_in_create_package3971)

                PACKAGE500_tree = self._adaptor.createWithPayload(PACKAGE500)
                self._adaptor.addChild(root_0, PACKAGE500_tree)

                # sql.g:526:41: (schema_name= ID DOT )?
                alt147 = 2
                LA147_0 = self.input.LA(1)

                if (LA147_0 == ID) :
                    LA147_1 = self.input.LA(2)

                    if (LA147_1 == DOT) :
                        alt147 = 1
                if alt147 == 1:
                    # sql.g:526:43: schema_name= ID DOT
                    pass 
                    schema_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_package3977)

                    schema_name_tree = self._adaptor.createWithPayload(schema_name)
                    self._adaptor.addChild(root_0, schema_name_tree)

                    DOT501=self.match(self.input, DOT, self.FOLLOW_DOT_in_create_package3979)

                    DOT501_tree = self._adaptor.createWithPayload(DOT501)
                    self._adaptor.addChild(root_0, DOT501_tree)




                package_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_package3986)

                package_name_tree = self._adaptor.createWithPayload(package_name)
                self._adaptor.addChild(root_0, package_name_tree)

                # sql.g:527:9: ( invoker_rights_clause )?
                alt148 = 2
                LA148_0 = self.input.LA(1)

                if (LA148_0 == AUTHID) :
                    alt148 = 1
                if alt148 == 1:
                    # sql.g:527:11: invoker_rights_clause
                    pass 
                    self._state.following.append(self.FOLLOW_invoker_rights_clause_in_create_package3998)
                    invoker_rights_clause502 = self.invoker_rights_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, invoker_rights_clause502.tree)



                set503 = self.input.LT(1)
                if self.input.LA(1) == IS or self.input.LA(1) == AS:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set503))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:528:21: ( declare_section )?
                alt149 = 2
                LA149_0 = self.input.LA(1)

                if ((PROCEDURE <= LA149_0 <= FUNCTION) or LA149_0 == CURSOR or LA149_0 == SUBTYPE or LA149_0 == PRAGMA) :
                    alt149 = 1
                if alt149 == 1:
                    # sql.g:528:23: declare_section
                    pass 
                    self._state.following.append(self.FOLLOW_declare_section_in_create_package4023)
                    declare_section504 = self.declare_section()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, declare_section504.tree)



                END505=self.match(self.input, END, self.FOLLOW_END_in_create_package4028)

                END505_tree = self._adaptor.createWithPayload(END505)
                self._adaptor.addChild(root_0, END505_tree)

                # sql.g:528:46: ( ID )?
                alt150 = 2
                LA150_0 = self.input.LA(1)

                if (LA150_0 == ID) :
                    alt150 = 1
                if alt150 == 1:
                    # sql.g:528:48: ID
                    pass 
                    ID506=self.match(self.input, ID, self.FOLLOW_ID_in_create_package4032)

                    ID506_tree = self._adaptor.createWithPayload(ID506)
                    self._adaptor.addChild(root_0, ID506_tree)




                SEMI507=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_create_package4037)

                SEMI507_tree = self._adaptor.createWithPayload(SEMI507)
                self._adaptor.addChild(root_0, SEMI507_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "create_package"

    class create_package_body_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.create_package_body_return, self).__init__()

            self.tree = None




    # $ANTLR start "create_package_body"
    # sql.g:531:1: create_package_body : CREATE ( OR kREPLACE )? PACKAGE BODY (schema_name= ID DOT )? package_name= ID ( IS | AS ) ( declare_section )? (initialize_section= body | END (package_name2= ID )? ) SEMI ;
    def create_package_body(self, ):

        retval = self.create_package_body_return()
        retval.start = self.input.LT(1)

        root_0 = None

        schema_name = None
        package_name = None
        package_name2 = None
        CREATE508 = None
        OR509 = None
        PACKAGE511 = None
        BODY512 = None
        DOT513 = None
        set514 = None
        END516 = None
        SEMI517 = None
        initialize_section = None

        kREPLACE510 = None

        declare_section515 = None


        schema_name_tree = None
        package_name_tree = None
        package_name2_tree = None
        CREATE508_tree = None
        OR509_tree = None
        PACKAGE511_tree = None
        BODY512_tree = None
        DOT513_tree = None
        set514_tree = None
        END516_tree = None
        SEMI517_tree = None

        try:
            try:
                # sql.g:531:21: ( CREATE ( OR kREPLACE )? PACKAGE BODY (schema_name= ID DOT )? package_name= ID ( IS | AS ) ( declare_section )? (initialize_section= body | END (package_name2= ID )? ) SEMI )
                # sql.g:532:9: CREATE ( OR kREPLACE )? PACKAGE BODY (schema_name= ID DOT )? package_name= ID ( IS | AS ) ( declare_section )? (initialize_section= body | END (package_name2= ID )? ) SEMI
                pass 
                root_0 = self._adaptor.nil()

                CREATE508=self.match(self.input, CREATE, self.FOLLOW_CREATE_in_create_package_body4058)

                CREATE508_tree = self._adaptor.createWithPayload(CREATE508)
                self._adaptor.addChild(root_0, CREATE508_tree)

                # sql.g:532:16: ( OR kREPLACE )?
                alt151 = 2
                LA151_0 = self.input.LA(1)

                if (LA151_0 == OR) :
                    alt151 = 1
                if alt151 == 1:
                    # sql.g:532:18: OR kREPLACE
                    pass 
                    OR509=self.match(self.input, OR, self.FOLLOW_OR_in_create_package_body4062)

                    OR509_tree = self._adaptor.createWithPayload(OR509)
                    self._adaptor.addChild(root_0, OR509_tree)

                    self._state.following.append(self.FOLLOW_kREPLACE_in_create_package_body4064)
                    kREPLACE510 = self.kREPLACE()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kREPLACE510.tree)



                PACKAGE511=self.match(self.input, PACKAGE, self.FOLLOW_PACKAGE_in_create_package_body4069)

                PACKAGE511_tree = self._adaptor.createWithPayload(PACKAGE511)
                self._adaptor.addChild(root_0, PACKAGE511_tree)

                BODY512=self.match(self.input, BODY, self.FOLLOW_BODY_in_create_package_body4071)

                BODY512_tree = self._adaptor.createWithPayload(BODY512)
                self._adaptor.addChild(root_0, BODY512_tree)

                # sql.g:532:46: (schema_name= ID DOT )?
                alt152 = 2
                LA152_0 = self.input.LA(1)

                if (LA152_0 == ID) :
                    LA152_1 = self.input.LA(2)

                    if (LA152_1 == DOT) :
                        alt152 = 1
                if alt152 == 1:
                    # sql.g:532:48: schema_name= ID DOT
                    pass 
                    schema_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_package_body4077)

                    schema_name_tree = self._adaptor.createWithPayload(schema_name)
                    self._adaptor.addChild(root_0, schema_name_tree)

                    DOT513=self.match(self.input, DOT, self.FOLLOW_DOT_in_create_package_body4079)

                    DOT513_tree = self._adaptor.createWithPayload(DOT513)
                    self._adaptor.addChild(root_0, DOT513_tree)




                package_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_package_body4086)

                package_name_tree = self._adaptor.createWithPayload(package_name)
                self._adaptor.addChild(root_0, package_name_tree)

                set514 = self.input.LT(1)
                if self.input.LA(1) == IS or self.input.LA(1) == AS:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set514))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:533:21: ( declare_section )?
                alt153 = 2
                LA153_0 = self.input.LA(1)

                if ((PROCEDURE <= LA153_0 <= FUNCTION) or LA153_0 == CURSOR or LA153_0 == SUBTYPE or LA153_0 == PRAGMA) :
                    alt153 = 1
                if alt153 == 1:
                    # sql.g:533:23: declare_section
                    pass 
                    self._state.following.append(self.FOLLOW_declare_section_in_create_package_body4108)
                    declare_section515 = self.declare_section()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, declare_section515.tree)



                # sql.g:534:9: (initialize_section= body | END (package_name2= ID )? )
                alt155 = 2
                LA155_0 = self.input.LA(1)

                if (LA155_0 == BEGIN) :
                    alt155 = 1
                elif (LA155_0 == END) :
                    alt155 = 2
                else:
                    nvae = NoViableAltException("", 155, 0, self.input)

                    raise nvae

                if alt155 == 1:
                    # sql.g:534:11: initialize_section= body
                    pass 
                    self._state.following.append(self.FOLLOW_body_in_create_package_body4125)
                    initialize_section = self.body()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, initialize_section.tree)


                elif alt155 == 2:
                    # sql.g:534:37: END (package_name2= ID )?
                    pass 
                    END516=self.match(self.input, END, self.FOLLOW_END_in_create_package_body4129)

                    END516_tree = self._adaptor.createWithPayload(END516)
                    self._adaptor.addChild(root_0, END516_tree)

                    # sql.g:534:41: (package_name2= ID )?
                    alt154 = 2
                    LA154_0 = self.input.LA(1)

                    if (LA154_0 == ID) :
                        alt154 = 1
                    if alt154 == 1:
                        # sql.g:534:43: package_name2= ID
                        pass 
                        package_name2=self.match(self.input, ID, self.FOLLOW_ID_in_create_package_body4135)

                        package_name2_tree = self._adaptor.createWithPayload(package_name2)
                        self._adaptor.addChild(root_0, package_name2_tree)







                SEMI517=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_create_package_body4150)

                SEMI517_tree = self._adaptor.createWithPayload(SEMI517)
                self._adaptor.addChild(root_0, SEMI517_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "create_package_body"

    class create_procedure_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.create_procedure_return, self).__init__()

            self.tree = None




    # $ANTLR start "create_procedure"
    # sql.g:538:1: create_procedure : CREATE ( OR kREPLACE )? PROCEDURE (schema_name= ID DOT )? procedure_name= ID ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )? ( invoker_rights_clause )? ( IS | AS ) ( ( declare_section )? body | call_spec | EXTERNAL ) SEMI ;
    def create_procedure(self, ):

        retval = self.create_procedure_return()
        retval.start = self.input.LT(1)

        root_0 = None

        schema_name = None
        procedure_name = None
        CREATE518 = None
        OR519 = None
        PROCEDURE521 = None
        DOT522 = None
        LPAREN523 = None
        COMMA525 = None
        RPAREN527 = None
        set529 = None
        EXTERNAL533 = None
        SEMI534 = None
        kREPLACE520 = None

        parameter_declaration524 = None

        parameter_declaration526 = None

        invoker_rights_clause528 = None

        declare_section530 = None

        body531 = None

        call_spec532 = None


        schema_name_tree = None
        procedure_name_tree = None
        CREATE518_tree = None
        OR519_tree = None
        PROCEDURE521_tree = None
        DOT522_tree = None
        LPAREN523_tree = None
        COMMA525_tree = None
        RPAREN527_tree = None
        set529_tree = None
        EXTERNAL533_tree = None
        SEMI534_tree = None

        try:
            try:
                # sql.g:538:18: ( CREATE ( OR kREPLACE )? PROCEDURE (schema_name= ID DOT )? procedure_name= ID ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )? ( invoker_rights_clause )? ( IS | AS ) ( ( declare_section )? body | call_spec | EXTERNAL ) SEMI )
                # sql.g:539:9: CREATE ( OR kREPLACE )? PROCEDURE (schema_name= ID DOT )? procedure_name= ID ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )? ( invoker_rights_clause )? ( IS | AS ) ( ( declare_section )? body | call_spec | EXTERNAL ) SEMI
                pass 
                root_0 = self._adaptor.nil()

                CREATE518=self.match(self.input, CREATE, self.FOLLOW_CREATE_in_create_procedure4171)

                CREATE518_tree = self._adaptor.createWithPayload(CREATE518)
                self._adaptor.addChild(root_0, CREATE518_tree)

                # sql.g:539:16: ( OR kREPLACE )?
                alt156 = 2
                LA156_0 = self.input.LA(1)

                if (LA156_0 == OR) :
                    alt156 = 1
                if alt156 == 1:
                    # sql.g:539:18: OR kREPLACE
                    pass 
                    OR519=self.match(self.input, OR, self.FOLLOW_OR_in_create_procedure4175)

                    OR519_tree = self._adaptor.createWithPayload(OR519)
                    self._adaptor.addChild(root_0, OR519_tree)

                    self._state.following.append(self.FOLLOW_kREPLACE_in_create_procedure4177)
                    kREPLACE520 = self.kREPLACE()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kREPLACE520.tree)



                PROCEDURE521=self.match(self.input, PROCEDURE, self.FOLLOW_PROCEDURE_in_create_procedure4182)

                PROCEDURE521_tree = self._adaptor.createWithPayload(PROCEDURE521)
                self._adaptor.addChild(root_0, PROCEDURE521_tree)

                # sql.g:539:43: (schema_name= ID DOT )?
                alt157 = 2
                LA157_0 = self.input.LA(1)

                if (LA157_0 == ID) :
                    LA157_1 = self.input.LA(2)

                    if (LA157_1 == DOT) :
                        alt157 = 1
                if alt157 == 1:
                    # sql.g:539:45: schema_name= ID DOT
                    pass 
                    schema_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_procedure4188)

                    schema_name_tree = self._adaptor.createWithPayload(schema_name)
                    self._adaptor.addChild(root_0, schema_name_tree)

                    DOT522=self.match(self.input, DOT, self.FOLLOW_DOT_in_create_procedure4190)

                    DOT522_tree = self._adaptor.createWithPayload(DOT522)
                    self._adaptor.addChild(root_0, DOT522_tree)




                procedure_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_procedure4197)

                procedure_name_tree = self._adaptor.createWithPayload(procedure_name)
                self._adaptor.addChild(root_0, procedure_name_tree)

                # sql.g:540:9: ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )?
                alt159 = 2
                LA159_0 = self.input.LA(1)

                if (LA159_0 == LPAREN) :
                    alt159 = 1
                if alt159 == 1:
                    # sql.g:540:11: LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN
                    pass 
                    LPAREN523=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_create_procedure4209)

                    LPAREN523_tree = self._adaptor.createWithPayload(LPAREN523)
                    self._adaptor.addChild(root_0, LPAREN523_tree)

                    self._state.following.append(self.FOLLOW_parameter_declaration_in_create_procedure4211)
                    parameter_declaration524 = self.parameter_declaration()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, parameter_declaration524.tree)
                    # sql.g:540:40: ( COMMA parameter_declaration )*
                    while True: #loop158
                        alt158 = 2
                        LA158_0 = self.input.LA(1)

                        if (LA158_0 == COMMA) :
                            alt158 = 1


                        if alt158 == 1:
                            # sql.g:540:42: COMMA parameter_declaration
                            pass 
                            COMMA525=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_create_procedure4215)

                            COMMA525_tree = self._adaptor.createWithPayload(COMMA525)
                            self._adaptor.addChild(root_0, COMMA525_tree)

                            self._state.following.append(self.FOLLOW_parameter_declaration_in_create_procedure4217)
                            parameter_declaration526 = self.parameter_declaration()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, parameter_declaration526.tree)


                        else:
                            break #loop158
                    RPAREN527=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_create_procedure4222)

                    RPAREN527_tree = self._adaptor.createWithPayload(RPAREN527)
                    self._adaptor.addChild(root_0, RPAREN527_tree)




                # sql.g:541:9: ( invoker_rights_clause )?
                alt160 = 2
                LA160_0 = self.input.LA(1)

                if (LA160_0 == AUTHID) :
                    alt160 = 1
                if alt160 == 1:
                    # sql.g:541:9: invoker_rights_clause
                    pass 
                    self._state.following.append(self.FOLLOW_invoker_rights_clause_in_create_procedure4235)
                    invoker_rights_clause528 = self.invoker_rights_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, invoker_rights_clause528.tree)



                set529 = self.input.LT(1)
                if self.input.LA(1) == IS or self.input.LA(1) == AS:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set529))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:543:9: ( ( declare_section )? body | call_spec | EXTERNAL )
                alt162 = 3
                LA162 = self.input.LA(1)
                if LA162 == PROCEDURE or LA162 == ID or LA162 == FUNCTION or LA162 == CURSOR or LA162 == SUBTYPE or LA162 == BEGIN or LA162 == PRAGMA:
                    alt162 = 1
                elif LA162 == LANGUAGE:
                    alt162 = 2
                elif LA162 == EXTERNAL:
                    alt162 = 3
                else:
                    nvae = NoViableAltException("", 162, 0, self.input)

                    raise nvae

                if alt162 == 1:
                    # sql.g:543:11: ( declare_section )? body
                    pass 
                    # sql.g:543:11: ( declare_section )?
                    alt161 = 2
                    LA161_0 = self.input.LA(1)

                    if ((PROCEDURE <= LA161_0 <= FUNCTION) or LA161_0 == CURSOR or LA161_0 == SUBTYPE or LA161_0 == PRAGMA) :
                        alt161 = 1
                    if alt161 == 1:
                        # sql.g:543:11: declare_section
                        pass 
                        self._state.following.append(self.FOLLOW_declare_section_in_create_procedure4266)
                        declare_section530 = self.declare_section()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, declare_section530.tree)



                    self._state.following.append(self.FOLLOW_body_in_create_procedure4269)
                    body531 = self.body()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, body531.tree)


                elif alt162 == 2:
                    # sql.g:544:11: call_spec
                    pass 
                    self._state.following.append(self.FOLLOW_call_spec_in_create_procedure4281)
                    call_spec532 = self.call_spec()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, call_spec532.tree)


                elif alt162 == 3:
                    # sql.g:545:11: EXTERNAL
                    pass 
                    EXTERNAL533=self.match(self.input, EXTERNAL, self.FOLLOW_EXTERNAL_in_create_procedure4293)

                    EXTERNAL533_tree = self._adaptor.createWithPayload(EXTERNAL533)
                    self._adaptor.addChild(root_0, EXTERNAL533_tree)




                SEMI534=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_create_procedure4305)

                SEMI534_tree = self._adaptor.createWithPayload(SEMI534)
                self._adaptor.addChild(root_0, SEMI534_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "create_procedure"

    class create_function_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.create_function_return, self).__init__()

            self.tree = None




    # $ANTLR start "create_function"
    # sql.g:549:1: create_function : CREATE ( OR kREPLACE )? FUNCTION (schema_name= ID DOT )? function_name= ID ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )? RETURN datatype ( invoker_rights_clause )? ( IS | AS ) ( ( declare_section )? body | call_spec | EXTERNAL ) SEMI ;
    def create_function(self, ):

        retval = self.create_function_return()
        retval.start = self.input.LT(1)

        root_0 = None

        schema_name = None
        function_name = None
        CREATE535 = None
        OR536 = None
        FUNCTION538 = None
        DOT539 = None
        LPAREN540 = None
        COMMA542 = None
        RPAREN544 = None
        RETURN545 = None
        set548 = None
        EXTERNAL552 = None
        SEMI553 = None
        kREPLACE537 = None

        parameter_declaration541 = None

        parameter_declaration543 = None

        datatype546 = None

        invoker_rights_clause547 = None

        declare_section549 = None

        body550 = None

        call_spec551 = None


        schema_name_tree = None
        function_name_tree = None
        CREATE535_tree = None
        OR536_tree = None
        FUNCTION538_tree = None
        DOT539_tree = None
        LPAREN540_tree = None
        COMMA542_tree = None
        RPAREN544_tree = None
        RETURN545_tree = None
        set548_tree = None
        EXTERNAL552_tree = None
        SEMI553_tree = None

        try:
            try:
                # sql.g:549:17: ( CREATE ( OR kREPLACE )? FUNCTION (schema_name= ID DOT )? function_name= ID ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )? RETURN datatype ( invoker_rights_clause )? ( IS | AS ) ( ( declare_section )? body | call_spec | EXTERNAL ) SEMI )
                # sql.g:550:9: CREATE ( OR kREPLACE )? FUNCTION (schema_name= ID DOT )? function_name= ID ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )? RETURN datatype ( invoker_rights_clause )? ( IS | AS ) ( ( declare_section )? body | call_spec | EXTERNAL ) SEMI
                pass 
                root_0 = self._adaptor.nil()

                CREATE535=self.match(self.input, CREATE, self.FOLLOW_CREATE_in_create_function4326)

                CREATE535_tree = self._adaptor.createWithPayload(CREATE535)
                self._adaptor.addChild(root_0, CREATE535_tree)

                # sql.g:550:16: ( OR kREPLACE )?
                alt163 = 2
                LA163_0 = self.input.LA(1)

                if (LA163_0 == OR) :
                    alt163 = 1
                if alt163 == 1:
                    # sql.g:550:18: OR kREPLACE
                    pass 
                    OR536=self.match(self.input, OR, self.FOLLOW_OR_in_create_function4330)

                    OR536_tree = self._adaptor.createWithPayload(OR536)
                    self._adaptor.addChild(root_0, OR536_tree)

                    self._state.following.append(self.FOLLOW_kREPLACE_in_create_function4332)
                    kREPLACE537 = self.kREPLACE()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, kREPLACE537.tree)



                FUNCTION538=self.match(self.input, FUNCTION, self.FOLLOW_FUNCTION_in_create_function4337)

                FUNCTION538_tree = self._adaptor.createWithPayload(FUNCTION538)
                self._adaptor.addChild(root_0, FUNCTION538_tree)

                # sql.g:550:42: (schema_name= ID DOT )?
                alt164 = 2
                LA164_0 = self.input.LA(1)

                if (LA164_0 == ID) :
                    LA164_1 = self.input.LA(2)

                    if (LA164_1 == DOT) :
                        alt164 = 1
                if alt164 == 1:
                    # sql.g:550:44: schema_name= ID DOT
                    pass 
                    schema_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_function4343)

                    schema_name_tree = self._adaptor.createWithPayload(schema_name)
                    self._adaptor.addChild(root_0, schema_name_tree)

                    DOT539=self.match(self.input, DOT, self.FOLLOW_DOT_in_create_function4345)

                    DOT539_tree = self._adaptor.createWithPayload(DOT539)
                    self._adaptor.addChild(root_0, DOT539_tree)




                function_name=self.match(self.input, ID, self.FOLLOW_ID_in_create_function4352)

                function_name_tree = self._adaptor.createWithPayload(function_name)
                self._adaptor.addChild(root_0, function_name_tree)

                # sql.g:551:9: ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )?
                alt166 = 2
                LA166_0 = self.input.LA(1)

                if (LA166_0 == LPAREN) :
                    alt166 = 1
                if alt166 == 1:
                    # sql.g:551:11: LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN
                    pass 
                    LPAREN540=self.match(self.input, LPAREN, self.FOLLOW_LPAREN_in_create_function4364)

                    LPAREN540_tree = self._adaptor.createWithPayload(LPAREN540)
                    self._adaptor.addChild(root_0, LPAREN540_tree)

                    self._state.following.append(self.FOLLOW_parameter_declaration_in_create_function4366)
                    parameter_declaration541 = self.parameter_declaration()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, parameter_declaration541.tree)
                    # sql.g:551:40: ( COMMA parameter_declaration )*
                    while True: #loop165
                        alt165 = 2
                        LA165_0 = self.input.LA(1)

                        if (LA165_0 == COMMA) :
                            alt165 = 1


                        if alt165 == 1:
                            # sql.g:551:42: COMMA parameter_declaration
                            pass 
                            COMMA542=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_create_function4370)

                            COMMA542_tree = self._adaptor.createWithPayload(COMMA542)
                            self._adaptor.addChild(root_0, COMMA542_tree)

                            self._state.following.append(self.FOLLOW_parameter_declaration_in_create_function4372)
                            parameter_declaration543 = self.parameter_declaration()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, parameter_declaration543.tree)


                        else:
                            break #loop165
                    RPAREN544=self.match(self.input, RPAREN, self.FOLLOW_RPAREN_in_create_function4377)

                    RPAREN544_tree = self._adaptor.createWithPayload(RPAREN544)
                    self._adaptor.addChild(root_0, RPAREN544_tree)




                RETURN545=self.match(self.input, RETURN, self.FOLLOW_RETURN_in_create_function4390)

                RETURN545_tree = self._adaptor.createWithPayload(RETURN545)
                self._adaptor.addChild(root_0, RETURN545_tree)

                self._state.following.append(self.FOLLOW_datatype_in_create_function4392)
                datatype546 = self.datatype()

                self._state.following.pop()
                self._adaptor.addChild(root_0, datatype546.tree)
                # sql.g:553:9: ( invoker_rights_clause )?
                alt167 = 2
                LA167_0 = self.input.LA(1)

                if (LA167_0 == AUTHID) :
                    alt167 = 1
                if alt167 == 1:
                    # sql.g:553:9: invoker_rights_clause
                    pass 
                    self._state.following.append(self.FOLLOW_invoker_rights_clause_in_create_function4402)
                    invoker_rights_clause547 = self.invoker_rights_clause()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, invoker_rights_clause547.tree)



                set548 = self.input.LT(1)
                if self.input.LA(1) == IS or self.input.LA(1) == AS:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set548))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                # sql.g:555:9: ( ( declare_section )? body | call_spec | EXTERNAL )
                alt169 = 3
                LA169 = self.input.LA(1)
                if LA169 == PROCEDURE or LA169 == ID or LA169 == FUNCTION or LA169 == CURSOR or LA169 == SUBTYPE or LA169 == BEGIN or LA169 == PRAGMA:
                    alt169 = 1
                elif LA169 == LANGUAGE:
                    alt169 = 2
                elif LA169 == EXTERNAL:
                    alt169 = 3
                else:
                    nvae = NoViableAltException("", 169, 0, self.input)

                    raise nvae

                if alt169 == 1:
                    # sql.g:555:11: ( declare_section )? body
                    pass 
                    # sql.g:555:11: ( declare_section )?
                    alt168 = 2
                    LA168_0 = self.input.LA(1)

                    if ((PROCEDURE <= LA168_0 <= FUNCTION) or LA168_0 == CURSOR or LA168_0 == SUBTYPE or LA168_0 == PRAGMA) :
                        alt168 = 1
                    if alt168 == 1:
                        # sql.g:555:11: declare_section
                        pass 
                        self._state.following.append(self.FOLLOW_declare_section_in_create_function4433)
                        declare_section549 = self.declare_section()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, declare_section549.tree)



                    self._state.following.append(self.FOLLOW_body_in_create_function4436)
                    body550 = self.body()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, body550.tree)


                elif alt169 == 2:
                    # sql.g:556:11: call_spec
                    pass 
                    self._state.following.append(self.FOLLOW_call_spec_in_create_function4448)
                    call_spec551 = self.call_spec()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, call_spec551.tree)


                elif alt169 == 3:
                    # sql.g:557:11: EXTERNAL
                    pass 
                    EXTERNAL552=self.match(self.input, EXTERNAL, self.FOLLOW_EXTERNAL_in_create_function4460)

                    EXTERNAL552_tree = self._adaptor.createWithPayload(EXTERNAL552)
                    self._adaptor.addChild(root_0, EXTERNAL552_tree)




                SEMI553=self.match(self.input, SEMI, self.FOLLOW_SEMI_in_create_function4472)

                SEMI553_tree = self._adaptor.createWithPayload(SEMI553)
                self._adaptor.addChild(root_0, SEMI553_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "create_function"

    class invoker_rights_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.invoker_rights_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "invoker_rights_clause"
    # sql.g:561:1: invoker_rights_clause : AUTHID ( CURRENT_USER | DEFINER ) ;
    def invoker_rights_clause(self, ):

        retval = self.invoker_rights_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AUTHID554 = None
        set555 = None

        AUTHID554_tree = None
        set555_tree = None

        try:
            try:
                # sql.g:561:23: ( AUTHID ( CURRENT_USER | DEFINER ) )
                # sql.g:562:9: AUTHID ( CURRENT_USER | DEFINER )
                pass 
                root_0 = self._adaptor.nil()

                AUTHID554=self.match(self.input, AUTHID, self.FOLLOW_AUTHID_in_invoker_rights_clause4493)

                AUTHID554_tree = self._adaptor.createWithPayload(AUTHID554)
                self._adaptor.addChild(root_0, AUTHID554_tree)

                set555 = self.input.LT(1)
                if (CURRENT_USER <= self.input.LA(1) <= DEFINER):
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set555))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "invoker_rights_clause"

    class call_spec_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.call_spec_return, self).__init__()

            self.tree = None




    # $ANTLR start "call_spec"
    # sql.g:565:1: call_spec : LANGUAGE swallow_to_semi ;
    def call_spec(self, ):

        retval = self.call_spec_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LANGUAGE556 = None
        swallow_to_semi557 = None


        LANGUAGE556_tree = None

        try:
            try:
                # sql.g:566:5: ( LANGUAGE swallow_to_semi )
                # sql.g:566:7: LANGUAGE swallow_to_semi
                pass 
                root_0 = self._adaptor.nil()

                LANGUAGE556=self.match(self.input, LANGUAGE, self.FOLLOW_LANGUAGE_in_call_spec4520)

                LANGUAGE556_tree = self._adaptor.createWithPayload(LANGUAGE556)
                self._adaptor.addChild(root_0, LANGUAGE556_tree)

                self._state.following.append(self.FOLLOW_swallow_to_semi_in_call_spec4522)
                swallow_to_semi557 = self.swallow_to_semi()

                self._state.following.pop()
                self._adaptor.addChild(root_0, swallow_to_semi557.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "call_spec"

    class kERRORS_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kERRORS_return, self).__init__()

            self.tree = None




    # $ANTLR start "kERRORS"
    # sql.g:569:1: kERRORS : {...}? ID ;
    def kERRORS(self, ):

        retval = self.kERRORS_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID558 = None

        ID558_tree = None

        try:
            try:
                # sql.g:569:9: ({...}? ID )
                # sql.g:569:11: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((len(self.input.LT(1).text) >= 3 and "errors".startswith(self.input.LT(1).text.lower()))):
                    raise FailedPredicateException(self.input, "kERRORS", " len(self.input.LT(1).text) >= 3 and \"errors\".startswith(self.input.LT(1).text.lower())")

                ID558=self.match(self.input, ID, self.FOLLOW_ID_in_kERRORS4537)

                ID558_tree = self._adaptor.createWithPayload(ID558)
                self._adaptor.addChild(root_0, ID558_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kERRORS"

    class kEXCEPTIONS_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kEXCEPTIONS_return, self).__init__()

            self.tree = None




    # $ANTLR start "kEXCEPTIONS"
    # sql.g:570:1: kEXCEPTIONS : {...}? ID ;
    def kEXCEPTIONS(self, ):

        retval = self.kEXCEPTIONS_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID559 = None

        ID559_tree = None

        try:
            try:
                # sql.g:570:13: ({...}? ID )
                # sql.g:570:15: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "exceptions")):
                    raise FailedPredicateException(self.input, "kEXCEPTIONS", "self.input.LT(1).text.lower() == \"exceptions\"")

                ID559=self.match(self.input, ID, self.FOLLOW_ID_in_kEXCEPTIONS4546)

                ID559_tree = self._adaptor.createWithPayload(ID559)
                self._adaptor.addChild(root_0, ID559_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kEXCEPTIONS"

    class kFOUND_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kFOUND_return, self).__init__()

            self.tree = None




    # $ANTLR start "kFOUND"
    # sql.g:571:1: kFOUND : {...}? ID ;
    def kFOUND(self, ):

        retval = self.kFOUND_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID560 = None

        ID560_tree = None

        try:
            try:
                # sql.g:571:8: ({...}? ID )
                # sql.g:571:10: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "found")):
                    raise FailedPredicateException(self.input, "kFOUND", "self.input.LT(1).text.lower() == \"found\"")

                ID560=self.match(self.input, ID, self.FOLLOW_ID_in_kFOUND4555)

                ID560_tree = self._adaptor.createWithPayload(ID560)
                self._adaptor.addChild(root_0, ID560_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kFOUND"

    class kINDICES_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kINDICES_return, self).__init__()

            self.tree = None




    # $ANTLR start "kINDICES"
    # sql.g:572:1: kINDICES : {...}? ID ;
    def kINDICES(self, ):

        retval = self.kINDICES_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID561 = None

        ID561_tree = None

        try:
            try:
                # sql.g:572:10: ({...}? ID )
                # sql.g:572:12: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "indices")):
                    raise FailedPredicateException(self.input, "kINDICES", "self.input.LT(1).text.lower() == \"indices\"")

                ID561=self.match(self.input, ID, self.FOLLOW_ID_in_kINDICES4564)

                ID561_tree = self._adaptor.createWithPayload(ID561)
                self._adaptor.addChild(root_0, ID561_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kINDICES"

    class kMOD_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kMOD_return, self).__init__()

            self.tree = None




    # $ANTLR start "kMOD"
    # sql.g:573:1: kMOD : {...}? ID ;
    def kMOD(self, ):

        retval = self.kMOD_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID562 = None

        ID562_tree = None

        try:
            try:
                # sql.g:573:6: ({...}? ID )
                # sql.g:573:8: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "mod")):
                    raise FailedPredicateException(self.input, "kMOD", "self.input.LT(1).text.lower() == \"mod\"")

                ID562=self.match(self.input, ID, self.FOLLOW_ID_in_kMOD4573)

                ID562_tree = self._adaptor.createWithPayload(ID562)
                self._adaptor.addChild(root_0, ID562_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kMOD"

    class kNAME_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kNAME_return, self).__init__()

            self.tree = None




    # $ANTLR start "kNAME"
    # sql.g:574:1: kNAME : {...}? ID ;
    def kNAME(self, ):

        retval = self.kNAME_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID563 = None

        ID563_tree = None

        try:
            try:
                # sql.g:574:7: ({...}? ID )
                # sql.g:574:9: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "name")):
                    raise FailedPredicateException(self.input, "kNAME", "self.input.LT(1).text.lower() == \"name\"")

                ID563=self.match(self.input, ID, self.FOLLOW_ID_in_kNAME4582)

                ID563_tree = self._adaptor.createWithPayload(ID563)
                self._adaptor.addChild(root_0, ID563_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kNAME"

    class kOF_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kOF_return, self).__init__()

            self.tree = None




    # $ANTLR start "kOF"
    # sql.g:575:1: kOF : {...}? ID ;
    def kOF(self, ):

        retval = self.kOF_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID564 = None

        ID564_tree = None

        try:
            try:
                # sql.g:575:5: ({...}? ID )
                # sql.g:575:7: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "of")):
                    raise FailedPredicateException(self.input, "kOF", "self.input.LT(1).text.lower() == \"of\"")

                ID564=self.match(self.input, ID, self.FOLLOW_ID_in_kOF4591)

                ID564_tree = self._adaptor.createWithPayload(ID564)
                self._adaptor.addChild(root_0, ID564_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kOF"

    class kREPLACE_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kREPLACE_return, self).__init__()

            self.tree = None




    # $ANTLR start "kREPLACE"
    # sql.g:576:1: kREPLACE : {...}? ID ;
    def kREPLACE(self, ):

        retval = self.kREPLACE_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID565 = None

        ID565_tree = None

        try:
            try:
                # sql.g:576:10: ({...}? ID )
                # sql.g:576:12: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "replace")):
                    raise FailedPredicateException(self.input, "kREPLACE", "self.input.LT(1).text.lower() == \"replace\"")

                ID565=self.match(self.input, ID, self.FOLLOW_ID_in_kREPLACE4600)

                ID565_tree = self._adaptor.createWithPayload(ID565)
                self._adaptor.addChild(root_0, ID565_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kREPLACE"

    class kROWCOUNT_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kROWCOUNT_return, self).__init__()

            self.tree = None




    # $ANTLR start "kROWCOUNT"
    # sql.g:577:1: kROWCOUNT : {...}? ID ;
    def kROWCOUNT(self, ):

        retval = self.kROWCOUNT_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID566 = None

        ID566_tree = None

        try:
            try:
                # sql.g:577:11: ({...}? ID )
                # sql.g:577:13: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "rowcount")):
                    raise FailedPredicateException(self.input, "kROWCOUNT", "self.input.LT(1).text.lower() == \"rowcount\"")

                ID566=self.match(self.input, ID, self.FOLLOW_ID_in_kROWCOUNT4609)

                ID566_tree = self._adaptor.createWithPayload(ID566)
                self._adaptor.addChild(root_0, ID566_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kROWCOUNT"

    class kSAVE_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kSAVE_return, self).__init__()

            self.tree = None




    # $ANTLR start "kSAVE"
    # sql.g:578:1: kSAVE : {...}? ID ;
    def kSAVE(self, ):

        retval = self.kSAVE_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID567 = None

        ID567_tree = None

        try:
            try:
                # sql.g:578:7: ({...}? ID )
                # sql.g:578:9: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "save")):
                    raise FailedPredicateException(self.input, "kSAVE", "self.input.LT(1).text.lower() == \"save\"")

                ID567=self.match(self.input, ID, self.FOLLOW_ID_in_kSAVE4618)

                ID567_tree = self._adaptor.createWithPayload(ID567)
                self._adaptor.addChild(root_0, ID567_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kSAVE"

    class kSHOW_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kSHOW_return, self).__init__()

            self.tree = None




    # $ANTLR start "kSHOW"
    # sql.g:579:1: kSHOW : {...}? ID ;
    def kSHOW(self, ):

        retval = self.kSHOW_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID568 = None

        ID568_tree = None

        try:
            try:
                # sql.g:579:7: ({...}? ID )
                # sql.g:579:9: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "show")):
                    raise FailedPredicateException(self.input, "kSHOW", "self.input.LT(1).text.lower() == \"show\"")

                ID568=self.match(self.input, ID, self.FOLLOW_ID_in_kSHOW4627)

                ID568_tree = self._adaptor.createWithPayload(ID568)
                self._adaptor.addChild(root_0, ID568_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kSHOW"

    class kTYPE_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kTYPE_return, self).__init__()

            self.tree = None




    # $ANTLR start "kTYPE"
    # sql.g:580:1: kTYPE : {...}? ID ;
    def kTYPE(self, ):

        retval = self.kTYPE_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID569 = None

        ID569_tree = None

        try:
            try:
                # sql.g:580:7: ({...}? ID )
                # sql.g:580:9: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "type")):
                    raise FailedPredicateException(self.input, "kTYPE", "self.input.LT(1).text.lower() == \"type\"")

                ID569=self.match(self.input, ID, self.FOLLOW_ID_in_kTYPE4636)

                ID569_tree = self._adaptor.createWithPayload(ID569)
                self._adaptor.addChild(root_0, ID569_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kTYPE"

    class kVALUES_return(ParserRuleReturnScope):
        def __init__(self):
            super(sqlParser.kVALUES_return, self).__init__()

            self.tree = None




    # $ANTLR start "kVALUES"
    # sql.g:581:1: kVALUES : {...}? ID ;
    def kVALUES(self, ):

        retval = self.kVALUES_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID570 = None

        ID570_tree = None

        try:
            try:
                # sql.g:581:9: ({...}? ID )
                # sql.g:581:11: {...}? ID
                pass 
                root_0 = self._adaptor.nil()

                if not ((self.input.LT(1).text.lower() == "values")):
                    raise FailedPredicateException(self.input, "kVALUES", "self.input.LT(1).text.lower() == \"values\"")

                ID570=self.match(self.input, ID, self.FOLLOW_ID_in_kVALUES4645)

                ID570_tree = self._adaptor.createWithPayload(ID570)
                self._adaptor.addChild(root_0, ID570_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException as re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "kVALUES"


    # Delegated rules


    # lookup tables for DFA #13

    DFA13_eot = DFA.unpack(
        "\13\uffff"
        )

    DFA13_eof = DFA.unpack(
        "\13\uffff"
        )

    DFA13_min = DFA.unpack(
        "\1\6\1\uffff\1\7\6\uffff\1\5\1\uffff"
        )

    DFA13_max = DFA.unpack(
        "\1\111\1\uffff\1\40\6\uffff\1\42\1\uffff"
        )

    DFA13_accept = DFA.unpack(
        "\1\uffff\1\10\1\uffff\1\2\1\3\1\5\1\6\1\7\1\4\1\uffff\1\1"
        )

    DFA13_special = DFA.unpack(
        "\13\uffff"
        )

            
    DFA13_transition = [
        DFA.unpack("\1\6\1\2\1\5\11\uffff\1\4\5\uffff\1\3\20\uffff\2\1\36"
        "\uffff\1\7"),
        DFA.unpack(""),
        DFA.unpack("\1\11\16\uffff\2\10\10\uffff\1\10"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\10\4\uffff\1\10\5\uffff\2\10\1\uffff\1\12\1\10\14"
        "\uffff\2\10"),
        DFA.unpack("")
    ]

    # class definition for DFA #13

    class DFA13(DFA):
        pass


    # lookup tables for DFA #93

    DFA93_eot = DFA.unpack(
        "\17\uffff"
        )

    DFA93_eof = DFA.unpack(
        "\17\uffff"
        )

    DFA93_min = DFA.unpack(
        "\1\7\2\uffff\1\0\13\uffff"
        )

    DFA93_max = DFA.unpack(
        "\1\160\2\uffff\1\0\13\uffff"
        )

    DFA93_accept = DFA.unpack(
        "\1\uffff\1\1\13\uffff\1\2\1\3"
        )

    DFA93_special = DFA.unpack(
        "\3\uffff\1\0\13\uffff"
        )

            
    DFA93_transition = [
        DFA.unpack("\1\3\2\uffff\1\1\12\uffff\1\1\31\uffff\1\1\57\uffff"
        "\2\1\3\uffff\1\1\3\uffff\5\1\1\uffff\3\1"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\uffff"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("")
    ]

    # class definition for DFA #93

    class DFA93(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA93_3 = input.LA(1)

                 
                index93_3 = input.index()
                input.rewind()
                s = -1
                if (not ((((self.input.LT(1).text.lower() == "values") or (self.input.LT(1).text.lower() == "indices"))))):
                    s = 1

                elif ((self.input.LT(1).text.lower() == "indices")):
                    s = 13

                elif ((self.input.LT(1).text.lower() == "values")):
                    s = 14

                 
                input.seek(index93_3)
                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 93, _s, input)
            self_.error(nvae)
            raise nvae
    # lookup tables for DFA #136

    DFA136_eot = DFA.unpack(
        "\12\uffff"
        )

    DFA136_eof = DFA.unpack(
        "\2\uffff\1\1\7\uffff"
        )

    DFA136_min = DFA.unpack(
        "\1\7\1\uffff\1\4\6\uffff\1\7"
        )

    DFA136_max = DFA.unpack(
        "\1\160\1\uffff\1\143\6\uffff\1\155"
        )

    DFA136_accept = DFA.unpack(
        "\1\uffff\1\1\1\uffff\1\2\1\3\1\4\1\5\1\6\1\7\1\uffff"
        )

    DFA136_special = DFA.unpack(
        "\12\uffff"
        )

            
    DFA136_transition = [
        DFA.unpack("\1\2\2\uffff\1\10\12\uffff\1\7\31\uffff\1\1\64\uffff"
        "\1\3\3\uffff\2\5\2\6\1\4\1\uffff\3\6"),
        DFA.unpack(""),
        DFA.unpack("\2\1\1\uffff\1\1\1\uffff\5\1\5\uffff\2\1\14\uffff\1"
        "\11\1\1\10\uffff\2\1\1\uffff\1\1\1\uffff\2\1\11\uffff\2\1\1\uffff"
        "\2\1\2\uffff\3\1\11\uffff\7\1\1\uffff\1\1\1\uffff\14\1"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\1\47\uffff\2\1\74\uffff\1\6")
    ]

    # class definition for DFA #136

    class DFA136(DFA):
        pass


 

    FOLLOW_create_object_in_sqlplus_file47 = frozenset([4, 114])
    FOLLOW_DIVIDE_in_sqlplus_file51 = frozenset([7])
    FOLLOW_show_errors_in_sqlplus_file53 = frozenset([4, 114])
    FOLLOW_DIVIDE_in_sqlplus_file58 = frozenset([4, 114])
    FOLLOW_EOF_in_sqlplus_file64 = frozenset([1])
    FOLLOW_kSHOW_in_show_errors85 = frozenset([7])
    FOLLOW_kERRORS_in_show_errors87 = frozenset([1, 5])
    FOLLOW_SEMI_in_show_errors89 = frozenset([1])
    FOLLOW_create_package_in_create_object107 = frozenset([1])
    FOLLOW_create_package_body_in_create_object115 = frozenset([1])
    FOLLOW_create_function_in_create_object123 = frozenset([1])
    FOLLOW_create_procedure_in_create_object131 = frozenset([1])
    FOLLOW_PROCEDURE_in_procedure_heading152 = frozenset([7])
    FOLLOW_ID_in_procedure_heading154 = frozenset([1, 10])
    FOLLOW_parameter_declarations_in_procedure_heading156 = frozenset([1])
    FOLLOW_FUNCTION_in_function_heading178 = frozenset([7])
    FOLLOW_ID_in_function_heading180 = frozenset([9, 10])
    FOLLOW_parameter_declarations_in_function_heading182 = frozenset([9])
    FOLLOW_RETURN_in_function_heading185 = frozenset([7, 32])
    FOLLOW_datatype_in_function_heading187 = frozenset([1])
    FOLLOW_LPAREN_in_parameter_declarations212 = frozenset([7])
    FOLLOW_parameter_declaration_in_parameter_declarations215 = frozenset([11, 12])
    FOLLOW_COMMA_in_parameter_declarations219 = frozenset([7])
    FOLLOW_parameter_declaration_in_parameter_declarations222 = frozenset([11, 12])
    FOLLOW_RPAREN_in_parameter_declarations227 = frozenset([1])
    FOLLOW_ID_in_parameter_declaration250 = frozenset([7, 13, 14, 32])
    FOLLOW_IN_in_parameter_declaration254 = frozenset([7, 32])
    FOLLOW_OUT_in_parameter_declaration262 = frozenset([7, 15, 32])
    FOLLOW_IN_in_parameter_declaration266 = frozenset([14])
    FOLLOW_OUT_in_parameter_declaration268 = frozenset([7, 15, 32])
    FOLLOW_NOCOPY_in_parameter_declaration272 = frozenset([7, 32])
    FOLLOW_datatype_in_parameter_declaration280 = frozenset([1, 16, 17])
    FOLLOW_set_in_parameter_declaration292 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_parameter_declaration302 = frozenset([1])
    FOLLOW_type_definition_in_declare_section324 = frozenset([5])
    FOLLOW_SEMI_in_declare_section326 = frozenset([1, 6, 7, 8, 18, 24, 73])
    FOLLOW_subtype_definition_in_declare_section334 = frozenset([5])
    FOLLOW_SEMI_in_declare_section336 = frozenset([1, 5, 6, 7, 8, 18, 24, 73])
    FOLLOW_cursor_definition_in_declare_section344 = frozenset([5])
    FOLLOW_SEMI_in_declare_section346 = frozenset([1, 5, 6, 7, 8, 18, 24, 73])
    FOLLOW_item_declaration_in_declare_section354 = frozenset([5])
    FOLLOW_SEMI_in_declare_section356 = frozenset([1, 5, 6, 7, 8, 18, 24, 73])
    FOLLOW_function_declaration_or_definition_in_declare_section364 = frozenset([5])
    FOLLOW_SEMI_in_declare_section366 = frozenset([1, 5, 6, 7, 8, 18, 24, 73])
    FOLLOW_procedure_declaration_or_definition_in_declare_section374 = frozenset([5])
    FOLLOW_SEMI_in_declare_section376 = frozenset([1, 5, 6, 7, 8, 18, 24, 73])
    FOLLOW_pragma_in_declare_section384 = frozenset([5])
    FOLLOW_SEMI_in_declare_section386 = frozenset([1, 5, 6, 7, 8, 18, 24, 73])
    FOLLOW_CURSOR_in_cursor_definition414 = frozenset([7])
    FOLLOW_ID_in_cursor_definition416 = frozenset([10, 19])
    FOLLOW_parameter_declarations_in_cursor_definition418 = frozenset([19])
    FOLLOW_IS_in_cursor_definition421 = frozenset([83])
    FOLLOW_select_statement_in_cursor_definition423 = frozenset([1])
    FOLLOW_variable_declaration_in_item_declaration440 = frozenset([1])
    FOLLOW_constant_declaration_in_item_declaration448 = frozenset([1])
    FOLLOW_exception_declaration_in_item_declaration456 = frozenset([1])
    FOLLOW_ID_in_variable_declaration477 = frozenset([7, 32])
    FOLLOW_datatype_in_variable_declaration479 = frozenset([1, 16, 17, 20])
    FOLLOW_NOT_in_variable_declaration487 = frozenset([21])
    FOLLOW_NULL_in_variable_declaration489 = frozenset([16, 17])
    FOLLOW_set_in_variable_declaration494 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_variable_declaration506 = frozenset([1])
    FOLLOW_ID_in_constant_declaration531 = frozenset([22])
    FOLLOW_CONSTANT_in_constant_declaration533 = frozenset([7, 32])
    FOLLOW_datatype_in_constant_declaration535 = frozenset([16, 17, 20])
    FOLLOW_NOT_in_constant_declaration539 = frozenset([21])
    FOLLOW_NULL_in_constant_declaration541 = frozenset([16, 17])
    FOLLOW_set_in_constant_declaration546 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_constant_declaration560 = frozenset([1])
    FOLLOW_ID_in_exception_declaration581 = frozenset([23])
    FOLLOW_EXCEPTION_in_exception_declaration583 = frozenset([1])
    FOLLOW_kTYPE_in_type_definition604 = frozenset([7])
    FOLLOW_ID_in_type_definition606 = frozenset([19])
    FOLLOW_IS_in_type_definition608 = frozenset([25, 26, 28, 29, 32])
    FOLLOW_record_type_definition_in_type_definition612 = frozenset([1])
    FOLLOW_collection_type_definition_in_type_definition616 = frozenset([1])
    FOLLOW_ref_cursor_type_definition_in_type_definition620 = frozenset([1])
    FOLLOW_SUBTYPE_in_subtype_definition643 = frozenset([7])
    FOLLOW_ID_in_subtype_definition645 = frozenset([19])
    FOLLOW_IS_in_subtype_definition647 = frozenset([7, 32])
    FOLLOW_datatype_in_subtype_definition649 = frozenset([1, 20])
    FOLLOW_NOT_in_subtype_definition653 = frozenset([21])
    FOLLOW_NULL_in_subtype_definition655 = frozenset([1])
    FOLLOW_RECORD_in_record_type_definition676 = frozenset([10])
    FOLLOW_LPAREN_in_record_type_definition678 = frozenset([7])
    FOLLOW_record_field_declaration_in_record_type_definition680 = frozenset([11, 12])
    FOLLOW_COMMA_in_record_type_definition684 = frozenset([7])
    FOLLOW_record_field_declaration_in_record_type_definition686 = frozenset([11, 12])
    FOLLOW_RPAREN_in_record_type_definition691 = frozenset([1])
    FOLLOW_ID_in_record_field_declaration705 = frozenset([7, 32])
    FOLLOW_datatype_in_record_field_declaration707 = frozenset([1, 16, 17, 20])
    FOLLOW_NOT_in_record_field_declaration713 = frozenset([21])
    FOLLOW_NULL_in_record_field_declaration715 = frozenset([16, 17])
    FOLLOW_set_in_record_field_declaration720 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_record_field_declaration730 = frozenset([1])
    FOLLOW_varray_type_definition_in_collection_type_definition747 = frozenset([1])
    FOLLOW_nested_table_type_definition_in_collection_type_definition752 = frozenset([1])
    FOLLOW_VARYING_in_varray_type_definition765 = frozenset([10, 27])
    FOLLOW_ARRAY_in_varray_type_definition767 = frozenset([10])
    FOLLOW_VARRAY_in_varray_type_definition772 = frozenset([10])
    FOLLOW_LPAREN_in_varray_type_definition776 = frozenset([104, 105])
    FOLLOW_numeric_literal_in_varray_type_definition778 = frozenset([12])
    FOLLOW_RPAREN_in_varray_type_definition780 = frozenset([7])
    FOLLOW_kOF_in_varray_type_definition782 = frozenset([7, 32])
    FOLLOW_datatype_in_varray_type_definition784 = frozenset([1, 20])
    FOLLOW_NOT_in_varray_type_definition788 = frozenset([21])
    FOLLOW_NULL_in_varray_type_definition790 = frozenset([1])
    FOLLOW_TABLE_in_nested_table_type_definition804 = frozenset([7])
    FOLLOW_kOF_in_nested_table_type_definition806 = frozenset([7, 32])
    FOLLOW_datatype_in_nested_table_type_definition808 = frozenset([1, 20, 30])
    FOLLOW_NOT_in_nested_table_type_definition812 = frozenset([21])
    FOLLOW_NULL_in_nested_table_type_definition814 = frozenset([1, 30])
    FOLLOW_INDEX_in_nested_table_type_definition821 = frozenset([31])
    FOLLOW_BY_in_nested_table_type_definition823 = frozenset([7, 32])
    FOLLOW_associative_index_type_in_nested_table_type_definition825 = frozenset([1])
    FOLLOW_datatype_in_associative_index_type839 = frozenset([1])
    FOLLOW_REF_in_ref_cursor_type_definition850 = frozenset([18])
    FOLLOW_CURSOR_in_ref_cursor_type_definition852 = frozenset([1, 9])
    FOLLOW_RETURN_in_ref_cursor_type_definition856 = frozenset([7, 32])
    FOLLOW_datatype_in_ref_cursor_type_definition858 = frozenset([1])
    FOLLOW_REF_in_datatype877 = frozenset([7])
    FOLLOW_ID_in_datatype882 = frozenset([1, 10, 33, 34])
    FOLLOW_DOT_in_datatype886 = frozenset([7])
    FOLLOW_ID_in_datatype888 = frozenset([1, 10, 34])
    FOLLOW_LPAREN_in_datatype895 = frozenset([104, 105])
    FOLLOW_numeric_literal_in_datatype897 = frozenset([11, 12])
    FOLLOW_COMMA_in_datatype901 = frozenset([104, 105])
    FOLLOW_numeric_literal_in_datatype903 = frozenset([11, 12])
    FOLLOW_RPAREN_in_datatype908 = frozenset([1])
    FOLLOW_PERCENT_in_datatype912 = frozenset([7, 35])
    FOLLOW_kTYPE_in_datatype916 = frozenset([1])
    FOLLOW_ROWTYPE_in_datatype920 = frozenset([1])
    FOLLOW_function_heading_in_function_declaration_or_definition946 = frozenset([1, 19, 36, 37, 38, 39, 40])
    FOLLOW_set_in_function_declaration_or_definition956 = frozenset([1, 19, 36, 37, 38, 39, 40])
    FOLLOW_set_in_function_declaration_or_definition985 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_declare_section_in_function_declaration_or_definition995 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_function_declaration_or_definition998 = frozenset([1])
    FOLLOW_function_heading_in_function_declaration1019 = frozenset([1, 36, 37, 38, 39])
    FOLLOW_set_in_function_declaration1029 = frozenset([1, 36, 37, 38, 39])
    FOLLOW_function_heading_in_function_definition1067 = frozenset([19, 36, 37, 38, 39, 40])
    FOLLOW_set_in_function_definition1077 = frozenset([19, 36, 37, 38, 39, 40])
    FOLLOW_set_in_function_definition1104 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_declare_section_in_function_definition1114 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_function_definition1117 = frozenset([1])
    FOLLOW_procedure_heading_in_procedure_declaration_or_definition1135 = frozenset([1, 19, 40])
    FOLLOW_set_in_procedure_declaration_or_definition1147 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_declare_section_in_procedure_declaration_or_definition1157 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_procedure_declaration_or_definition1160 = frozenset([1])
    FOLLOW_procedure_heading_in_procedure_declaration1177 = frozenset([1])
    FOLLOW_procedure_heading_in_procedure_definition1188 = frozenset([19, 40])
    FOLLOW_set_in_procedure_definition1191 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_declare_section_in_procedure_definition1201 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_procedure_definition1204 = frozenset([1])
    FOLLOW_BEGIN_in_body1218 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_body1220 = frozenset([5])
    FOLLOW_SEMI_in_body1222 = frozenset([5, 6, 7, 8, 9, 18, 21, 23, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_body1226 = frozenset([5])
    FOLLOW_SEMI_in_body1228 = frozenset([5, 6, 7, 8, 9, 18, 21, 23, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_pragma_in_body1232 = frozenset([5])
    FOLLOW_SEMI_in_body1234 = frozenset([5, 6, 7, 8, 9, 18, 21, 23, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_EXCEPTION_in_body1242 = frozenset([43])
    FOLLOW_exception_handler_in_body1244 = frozenset([42, 43])
    FOLLOW_END_in_body1250 = frozenset([1, 7])
    FOLLOW_ID_in_body1252 = frozenset([1])
    FOLLOW_WHEN_in_exception_handler1264 = frozenset([7, 45, 47])
    FOLLOW_qual_id_in_exception_handler1268 = frozenset([44, 46])
    FOLLOW_OR_in_exception_handler1272 = frozenset([7, 47])
    FOLLOW_qual_id_in_exception_handler1274 = frozenset([44, 46])
    FOLLOW_OTHERS_in_exception_handler1281 = frozenset([46])
    FOLLOW_THEN_in_exception_handler1287 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_exception_handler1291 = frozenset([5])
    FOLLOW_SEMI_in_exception_handler1293 = frozenset([1, 5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_label_in_statement1311 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_assign_or_call_statement_in_statement1320 = frozenset([1])
    FOLLOW_case_statement_in_statement1328 = frozenset([1])
    FOLLOW_close_statement_in_statement1336 = frozenset([1])
    FOLLOW_continue_statement_in_statement1344 = frozenset([1])
    FOLLOW_basic_loop_statement_in_statement1352 = frozenset([1])
    FOLLOW_execute_immediate_statement_in_statement1360 = frozenset([1])
    FOLLOW_exit_statement_in_statement1368 = frozenset([1])
    FOLLOW_fetch_statement_in_statement1376 = frozenset([1])
    FOLLOW_for_loop_statement_in_statement1384 = frozenset([1])
    FOLLOW_forall_statement_in_statement1392 = frozenset([1])
    FOLLOW_goto_statement_in_statement1400 = frozenset([1])
    FOLLOW_if_statement_in_statement1408 = frozenset([1])
    FOLLOW_null_statement_in_statement1416 = frozenset([1])
    FOLLOW_open_statement_in_statement1424 = frozenset([1])
    FOLLOW_plsql_block_in_statement1432 = frozenset([1])
    FOLLOW_raise_statement_in_statement1440 = frozenset([1])
    FOLLOW_return_statement_in_statement1448 = frozenset([1])
    FOLLOW_sql_statement_in_statement1456 = frozenset([1])
    FOLLOW_while_loop_statement_in_statement1464 = frozenset([1])
    FOLLOW_call_in_lvalue1487 = frozenset([1, 33])
    FOLLOW_DOT_in_lvalue1491 = frozenset([7, 47])
    FOLLOW_call_in_lvalue1493 = frozenset([1, 33])
    FOLLOW_lvalue_in_assign_or_call_statement1513 = frozenset([1, 16, 33])
    FOLLOW_DOT_in_assign_or_call_statement1517 = frozenset([48])
    FOLLOW_delete_call_in_assign_or_call_statement1519 = frozenset([1])
    FOLLOW_ASSIGN_in_assign_or_call_statement1523 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_assign_or_call_statement1525 = frozenset([1])
    FOLLOW_COLON_in_call1545 = frozenset([7])
    FOLLOW_ID_in_call1548 = frozenset([1, 10])
    FOLLOW_LPAREN_in_call1552 = frozenset([7, 10, 12, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_parameter_in_call1556 = frozenset([11, 12])
    FOLLOW_COMMA_in_call1560 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_parameter_in_call1562 = frozenset([11, 12])
    FOLLOW_RPAREN_in_call1570 = frozenset([1])
    FOLLOW_DELETE_in_delete_call1590 = frozenset([1, 10])
    FOLLOW_LPAREN_in_delete_call1594 = frozenset([7, 10, 12, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_parameter_in_delete_call1596 = frozenset([12])
    FOLLOW_RPAREN_in_delete_call1599 = frozenset([1])
    FOLLOW_LOOP_in_basic_loop_statement1623 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_basic_loop_statement1627 = frozenset([5])
    FOLLOW_SEMI_in_basic_loop_statement1629 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_END_in_basic_loop_statement1634 = frozenset([49])
    FOLLOW_LOOP_in_basic_loop_statement1636 = frozenset([1, 7])
    FOLLOW_label_name_in_basic_loop_statement1638 = frozenset([1])
    FOLLOW_CASE_in_case_statement1660 = frozenset([7, 10, 20, 21, 43, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_case_statement1662 = frozenset([43])
    FOLLOW_WHEN_in_case_statement1675 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_case_statement1677 = frozenset([46])
    FOLLOW_THEN_in_case_statement1679 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_case_statement1683 = frozenset([5])
    FOLLOW_SEMI_in_case_statement1685 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 43, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_ELSE_in_case_statement1703 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_case_statement1705 = frozenset([5])
    FOLLOW_SEMI_in_case_statement1707 = frozenset([42])
    FOLLOW_END_in_case_statement1720 = frozenset([50])
    FOLLOW_CASE_in_case_statement1722 = frozenset([1, 7])
    FOLLOW_label_name_in_case_statement1724 = frozenset([1])
    FOLLOW_CLOSE_in_close_statement1746 = frozenset([7])
    FOLLOW_ID_in_close_statement1748 = frozenset([1, 33])
    FOLLOW_DOT_in_close_statement1752 = frozenset([7])
    FOLLOW_ID_in_close_statement1754 = frozenset([1])
    FOLLOW_CONTINUE_in_continue_statement1778 = frozenset([1, 7, 43])
    FOLLOW_ID_in_continue_statement1784 = frozenset([1, 43])
    FOLLOW_WHEN_in_continue_statement1791 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_continue_statement1793 = frozenset([1])
    FOLLOW_EXECUTE_in_execute_immediate_statement1817 = frozenset([55])
    FOLLOW_IMMEDIATE_in_execute_immediate_statement1819 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_execute_immediate_statement1821 = frozenset([1, 9, 59, 60, 62, 63])
    FOLLOW_into_clause_in_execute_immediate_statement1835 = frozenset([1, 62])
    FOLLOW_bulk_collect_into_clause_in_execute_immediate_statement1839 = frozenset([1, 62])
    FOLLOW_using_clause_in_execute_immediate_statement1842 = frozenset([1])
    FOLLOW_using_clause_in_execute_immediate_statement1855 = frozenset([1, 9, 63])
    FOLLOW_dynamic_returning_clause_in_execute_immediate_statement1857 = frozenset([1])
    FOLLOW_dynamic_returning_clause_in_execute_immediate_statement1870 = frozenset([1])
    FOLLOW_EXIT_in_exit_statement1902 = frozenset([1, 7, 43])
    FOLLOW_ID_in_exit_statement1908 = frozenset([1, 43])
    FOLLOW_WHEN_in_exit_statement1915 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_exit_statement1917 = frozenset([1])
    FOLLOW_FETCH_in_fetch_statement1941 = frozenset([7, 47])
    FOLLOW_qual_id_in_fetch_statement1943 = frozenset([59, 60])
    FOLLOW_into_clause_in_fetch_statement1947 = frozenset([1])
    FOLLOW_bulk_collect_into_clause_in_fetch_statement1951 = frozenset([1, 58])
    FOLLOW_LIMIT_in_fetch_statement1955 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_numeric_expression_in_fetch_statement1957 = frozenset([1])
    FOLLOW_INTO_in_into_clause1987 = frozenset([7, 47])
    FOLLOW_lvalue_in_into_clause1989 = frozenset([1, 11])
    FOLLOW_COMMA_in_into_clause1993 = frozenset([7, 47])
    FOLLOW_lvalue_in_into_clause1995 = frozenset([1, 11])
    FOLLOW_BULK_in_bulk_collect_into_clause2023 = frozenset([61])
    FOLLOW_COLLECT_in_bulk_collect_into_clause2025 = frozenset([59])
    FOLLOW_INTO_in_bulk_collect_into_clause2027 = frozenset([7, 47])
    FOLLOW_lvalue_in_bulk_collect_into_clause2029 = frozenset([1, 11])
    FOLLOW_COMMA_in_bulk_collect_into_clause2033 = frozenset([7, 47])
    FOLLOW_lvalue_in_bulk_collect_into_clause2035 = frozenset([1, 11])
    FOLLOW_USING_in_using_clause2059 = frozenset([7, 10, 13, 14, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_param_modifiers_in_using_clause2061 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_using_clause2064 = frozenset([1, 11])
    FOLLOW_COMMA_in_using_clause2068 = frozenset([7, 10, 13, 14, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_param_modifiers_in_using_clause2070 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_using_clause2073 = frozenset([1, 11])
    FOLLOW_IN_in_param_modifiers2090 = frozenset([1, 14])
    FOLLOW_OUT_in_param_modifiers2092 = frozenset([1])
    FOLLOW_OUT_in_param_modifiers2097 = frozenset([1])
    FOLLOW_set_in_dynamic_returning_clause2115 = frozenset([59, 60])
    FOLLOW_into_clause_in_dynamic_returning_clause2127 = frozenset([1])
    FOLLOW_bulk_collect_into_clause_in_dynamic_returning_clause2131 = frozenset([1])
    FOLLOW_FOR_in_for_loop_statement2154 = frozenset([7])
    FOLLOW_ID_in_for_loop_statement2156 = frozenset([13])
    FOLLOW_IN_in_for_loop_statement2158 = frozenset([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_set_in_for_loop_statement2162 = frozenset([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_LOOP_in_for_loop_statement2170 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_for_loop_statement2174 = frozenset([5])
    FOLLOW_SEMI_in_for_loop_statement2176 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_END_in_for_loop_statement2181 = frozenset([49])
    FOLLOW_LOOP_in_for_loop_statement2183 = frozenset([1, 7])
    FOLLOW_label_name_in_for_loop_statement2185 = frozenset([1])
    FOLLOW_FORALL_in_forall_statement2207 = frozenset([7])
    FOLLOW_ID_in_forall_statement2209 = frozenset([13])
    FOLLOW_IN_in_forall_statement2211 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_bounds_clause_in_forall_statement2213 = frozenset([48, 78, 79, 80, 81, 82, 83, 84, 86])
    FOLLOW_sql_statement_in_forall_statement2215 = frozenset([1, 7])
    FOLLOW_kSAVE_in_forall_statement2219 = frozenset([7])
    FOLLOW_kEXCEPTIONS_in_forall_statement2221 = frozenset([1])
    FOLLOW_numeric_expression_in_bounds_clause2243 = frozenset([66])
    FOLLOW_DOUBLEDOT_in_bounds_clause2245 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_numeric_expression_in_bounds_clause2247 = frozenset([1])
    FOLLOW_kINDICES_in_bounds_clause2255 = frozenset([7])
    FOLLOW_kOF_in_bounds_clause2257 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_atom_in_bounds_clause2259 = frozenset([1, 67])
    FOLLOW_BETWEEN_in_bounds_clause2263 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_numeric_expression_in_bounds_clause2265 = frozenset([68])
    FOLLOW_AND_in_bounds_clause2267 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_numeric_expression_in_bounds_clause2269 = frozenset([1])
    FOLLOW_kVALUES_in_bounds_clause2280 = frozenset([7])
    FOLLOW_kOF_in_bounds_clause2282 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_atom_in_bounds_clause2284 = frozenset([1])
    FOLLOW_GOTO_in_goto_statement2305 = frozenset([7])
    FOLLOW_label_name_in_goto_statement2307 = frozenset([1])
    FOLLOW_IF_in_if_statement2328 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_if_statement2330 = frozenset([46])
    FOLLOW_THEN_in_if_statement2332 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_if_statement2336 = frozenset([5])
    FOLLOW_SEMI_in_if_statement2338 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 64, 65, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_ELSIF_in_if_statement2353 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_if_statement2355 = frozenset([46])
    FOLLOW_THEN_in_if_statement2357 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_if_statement2361 = frozenset([5])
    FOLLOW_SEMI_in_if_statement2363 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 64, 65, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_ELSE_in_if_statement2381 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_if_statement2385 = frozenset([5])
    FOLLOW_SEMI_in_if_statement2387 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_END_in_if_statement2403 = frozenset([70])
    FOLLOW_IF_in_if_statement2405 = frozenset([1])
    FOLLOW_NULL_in_null_statement2426 = frozenset([1])
    FOLLOW_OPEN_in_open_statement2447 = frozenset([7])
    FOLLOW_ID_in_open_statement2449 = frozenset([1, 10, 33, 64])
    FOLLOW_DOT_in_open_statement2453 = frozenset([7])
    FOLLOW_ID_in_open_statement2455 = frozenset([1, 10, 33, 64])
    FOLLOW_call_args_in_open_statement2460 = frozenset([1, 64])
    FOLLOW_FOR_in_open_statement2465 = frozenset([83])
    FOLLOW_select_statement_in_open_statement2467 = frozenset([1])
    FOLLOW_PRAGMA_in_pragma2491 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_pragma2493 = frozenset([1])
    FOLLOW_RAISE_in_raise_statement2514 = frozenset([1, 7])
    FOLLOW_ID_in_raise_statement2518 = frozenset([1, 33])
    FOLLOW_DOT_in_raise_statement2522 = frozenset([7])
    FOLLOW_ID_in_raise_statement2524 = frozenset([1, 33])
    FOLLOW_RETURN_in_return_statement2551 = frozenset([1, 7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_return_statement2553 = frozenset([1])
    FOLLOW_DECLARE_in_plsql_block2577 = frozenset([5, 6, 7, 8, 18, 24, 73])
    FOLLOW_declare_section_in_plsql_block2579 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_plsql_block2584 = frozenset([1])
    FOLLOW_LLABEL_in_label2605 = frozenset([76])
    FOLLOW_label_in_label2607 = frozenset([77])
    FOLLOW_RLABEL_in_label2609 = frozenset([1])
    FOLLOW_COLON_in_qual_id2623 = frozenset([7])
    FOLLOW_ID_in_qual_id2626 = frozenset([1, 33])
    FOLLOW_DOT_in_qual_id2630 = frozenset([7, 47])
    FOLLOW_COLON_in_qual_id2632 = frozenset([7])
    FOLLOW_ID_in_qual_id2635 = frozenset([1, 33])
    FOLLOW_commit_statement_in_sql_statement2655 = frozenset([1])
    FOLLOW_delete_statement_in_sql_statement2663 = frozenset([1])
    FOLLOW_insert_statement_in_sql_statement2671 = frozenset([1])
    FOLLOW_lock_table_statement_in_sql_statement2679 = frozenset([1])
    FOLLOW_rollback_statement_in_sql_statement2687 = frozenset([1])
    FOLLOW_savepoint_statement_in_sql_statement2695 = frozenset([1])
    FOLLOW_select_statement_in_sql_statement2703 = frozenset([1])
    FOLLOW_set_transaction_statement_in_sql_statement2711 = frozenset([1])
    FOLLOW_update_statement_in_sql_statement2719 = frozenset([1])
    FOLLOW_COMMIT_in_commit_statement2740 = frozenset([1, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_commit_statement2742 = frozenset([1])
    FOLLOW_DELETE_in_delete_statement2764 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_delete_statement2766 = frozenset([1])
    FOLLOW_INSERT_in_insert_statement2787 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_insert_statement2789 = frozenset([1])
    FOLLOW_LOCK_in_lock_table_statement2810 = frozenset([29])
    FOLLOW_TABLE_in_lock_table_statement2812 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_lock_table_statement2814 = frozenset([1])
    FOLLOW_ROLLBACK_in_rollback_statement2835 = frozenset([1, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_rollback_statement2837 = frozenset([1])
    FOLLOW_SAVEPOINT_in_savepoint_statement2859 = frozenset([7])
    FOLLOW_ID_in_savepoint_statement2861 = frozenset([1])
    FOLLOW_SELECT_in_select_statement2882 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_select_statement2884 = frozenset([1])
    FOLLOW_SET_in_set_transaction_statement2905 = frozenset([85])
    FOLLOW_TRANSACTION_in_set_transaction_statement2907 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_set_transaction_statement2909 = frozenset([1])
    FOLLOW_UPDATE_in_update_statement2930 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_update_statement2932 = frozenset([1])
    FOLLOW_set_in_swallow_to_semi2953 = frozenset([1, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_WHILE_in_while_loop_statement2980 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_while_loop_statement2982 = frozenset([49])
    FOLLOW_LOOP_in_while_loop_statement2984 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_statement_in_while_loop_statement2988 = frozenset([5])
    FOLLOW_SEMI_in_while_loop_statement2990 = frozenset([5, 6, 7, 8, 9, 18, 21, 24, 41, 42, 47, 48, 49, 50, 52, 53, 54, 56, 57, 64, 65, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87])
    FOLLOW_END_in_while_loop_statement2995 = frozenset([49])
    FOLLOW_LOOP_in_while_loop_statement2997 = frozenset([1, 7])
    FOLLOW_label_name_in_while_loop_statement2999 = frozenset([1])
    FOLLOW_set_in_match_parens3028 = frozenset([1, 4, 6, 7, 8, 9, 11, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_RPAREN_in_match_parens3068 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_match_parens_in_match_parens3070 = frozenset([10])
    FOLLOW_LPAREN_in_match_parens3072 = frozenset([1])
    FOLLOW_ID_in_label_name3084 = frozenset([1])
    FOLLOW_or_expr_in_expression3096 = frozenset([1])
    FOLLOW_and_expr_in_or_expr3113 = frozenset([1, 44])
    FOLLOW_OR_in_or_expr3117 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_and_expr_in_or_expr3119 = frozenset([1, 44])
    FOLLOW_not_expr_in_and_expr3139 = frozenset([1, 68])
    FOLLOW_AND_in_and_expr3143 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_not_expr_in_and_expr3145 = frozenset([1, 68])
    FOLLOW_NOT_in_not_expr3165 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_compare_expr_in_not_expr3168 = frozenset([1])
    FOLLOW_is_null_expr_in_compare_expr3185 = frozenset([1, 88, 89, 90, 91, 92, 93])
    FOLLOW_set_in_compare_expr3189 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_is_null_expr_in_compare_expr3215 = frozenset([1])
    FOLLOW_like_expr_in_is_null_expr3235 = frozenset([1, 19])
    FOLLOW_IS_in_is_null_expr3239 = frozenset([20, 21])
    FOLLOW_NOT_in_is_null_expr3241 = frozenset([21])
    FOLLOW_NULL_in_is_null_expr3244 = frozenset([1])
    FOLLOW_between_expr_in_like_expr3263 = frozenset([1, 20, 94])
    FOLLOW_NOT_in_like_expr3267 = frozenset([94])
    FOLLOW_LIKE_in_like_expr3270 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_between_expr_in_like_expr3272 = frozenset([1])
    FOLLOW_in_expr_in_between_expr3292 = frozenset([1, 20, 67])
    FOLLOW_NOT_in_between_expr3296 = frozenset([67])
    FOLLOW_BETWEEN_in_between_expr3299 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_in_expr_in_between_expr3301 = frozenset([68])
    FOLLOW_AND_in_between_expr3303 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_in_expr_in_between_expr3305 = frozenset([1])
    FOLLOW_add_expr_in_in_expr3325 = frozenset([1, 13, 20])
    FOLLOW_NOT_in_in_expr3329 = frozenset([13])
    FOLLOW_IN_in_in_expr3332 = frozenset([10])
    FOLLOW_LPAREN_in_in_expr3334 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_add_expr_in_in_expr3336 = frozenset([11, 12])
    FOLLOW_COMMA_in_in_expr3340 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_add_expr_in_in_expr3342 = frozenset([11, 12])
    FOLLOW_RPAREN_in_in_expr3347 = frozenset([1])
    FOLLOW_add_expr_in_numeric_expression3367 = frozenset([1])
    FOLLOW_mul_expr_in_add_expr3384 = frozenset([1, 95, 96, 97])
    FOLLOW_set_in_add_expr3388 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_mul_expr_in_add_expr3402 = frozenset([1, 95, 96, 97])
    FOLLOW_unary_sign_expr_in_mul_expr3422 = frozenset([1, 4, 7, 98])
    FOLLOW_ASTERISK_in_mul_expr3428 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_DIVIDE_in_mul_expr3432 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_kMOD_in_mul_expr3436 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_unary_sign_expr_in_mul_expr3440 = frozenset([1, 4, 7, 98])
    FOLLOW_set_in_unary_sign_expr3460 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_exponent_expr_in_unary_sign_expr3471 = frozenset([1])
    FOLLOW_atom_in_exponent_expr3488 = frozenset([1, 99])
    FOLLOW_EXPONENT_in_exponent_expr3492 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_atom_in_exponent_expr3494 = frozenset([1])
    FOLLOW_variable_or_function_call_in_atom3514 = frozenset([1, 34])
    FOLLOW_PERCENT_in_atom3518 = frozenset([7, 101, 102, 103])
    FOLLOW_attribute_in_atom3520 = frozenset([1])
    FOLLOW_SQL_in_atom3531 = frozenset([34])
    FOLLOW_PERCENT_in_atom3533 = frozenset([7, 101, 102, 103])
    FOLLOW_attribute_in_atom3535 = frozenset([1])
    FOLLOW_string_literal_in_atom3543 = frozenset([1])
    FOLLOW_numeric_atom_in_atom3551 = frozenset([1])
    FOLLOW_boolean_atom_in_atom3559 = frozenset([1])
    FOLLOW_NULL_in_atom3567 = frozenset([1])
    FOLLOW_LPAREN_in_atom3575 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_atom3577 = frozenset([12])
    FOLLOW_RPAREN_in_atom3579 = frozenset([1])
    FOLLOW_call_in_variable_or_function_call3600 = frozenset([1, 33])
    FOLLOW_DOT_in_variable_or_function_call3604 = frozenset([7, 47])
    FOLLOW_call_in_variable_or_function_call3606 = frozenset([1, 33])
    FOLLOW_DOT_in_variable_or_function_call3613 = frozenset([48])
    FOLLOW_delete_call_in_variable_or_function_call3615 = frozenset([1])
    FOLLOW_BULK_ROWCOUNT_in_attribute3635 = frozenset([10])
    FOLLOW_LPAREN_in_attribute3637 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_attribute3639 = frozenset([12])
    FOLLOW_RPAREN_in_attribute3641 = frozenset([1])
    FOLLOW_kFOUND_in_attribute3649 = frozenset([1])
    FOLLOW_ISOPEN_in_attribute3657 = frozenset([1])
    FOLLOW_NOTFOUND_in_attribute3665 = frozenset([1])
    FOLLOW_kROWCOUNT_in_attribute3673 = frozenset([1])
    FOLLOW_LPAREN_in_call_args3690 = frozenset([7, 10, 12, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_parameter_in_call_args3694 = frozenset([11, 12])
    FOLLOW_COMMA_in_call_args3698 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_parameter_in_call_args3700 = frozenset([11, 12])
    FOLLOW_RPAREN_in_call_args3708 = frozenset([1])
    FOLLOW_boolean_literal_in_boolean_atom3725 = frozenset([1])
    FOLLOW_collection_exists_in_boolean_atom3733 = frozenset([1])
    FOLLOW_conditional_predicate_in_boolean_atom3741 = frozenset([1])
    FOLLOW_numeric_literal_in_numeric_atom3758 = frozenset([1])
    FOLLOW_set_in_numeric_literal0 = frozenset([1])
    FOLLOW_set_in_boolean_literal0 = frozenset([1])
    FOLLOW_QUOTED_STRING_in_string_literal3825 = frozenset([1])
    FOLLOW_ID_in_collection_exists3842 = frozenset([33])
    FOLLOW_DOT_in_collection_exists3844 = frozenset([109])
    FOLLOW_EXISTS_in_collection_exists3846 = frozenset([10])
    FOLLOW_LPAREN_in_collection_exists3848 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_collection_exists3850 = frozenset([12])
    FOLLOW_RPAREN_in_collection_exists3852 = frozenset([1])
    FOLLOW_INSERTING_in_conditional_predicate3869 = frozenset([1])
    FOLLOW_UPDATING_in_conditional_predicate3877 = frozenset([1, 10])
    FOLLOW_LPAREN_in_conditional_predicate3881 = frozenset([108])
    FOLLOW_QUOTED_STRING_in_conditional_predicate3883 = frozenset([12])
    FOLLOW_RPAREN_in_conditional_predicate3885 = frozenset([1])
    FOLLOW_DELETING_in_conditional_predicate3896 = frozenset([1])
    FOLLOW_ID_in_parameter3915 = frozenset([113])
    FOLLOW_ARROW_in_parameter3917 = frozenset([7, 10, 20, 21, 47, 95, 96, 100, 104, 105, 106, 107, 108, 110, 111, 112])
    FOLLOW_expression_in_parameter3922 = frozenset([1])
    FOLLOW_expression_in_index3939 = frozenset([1])
    FOLLOW_CREATE_in_create_package3960 = frozenset([44, 115])
    FOLLOW_OR_in_create_package3964 = frozenset([7])
    FOLLOW_kREPLACE_in_create_package3966 = frozenset([115])
    FOLLOW_PACKAGE_in_create_package3971 = frozenset([7])
    FOLLOW_ID_in_create_package3977 = frozenset([33])
    FOLLOW_DOT_in_create_package3979 = frozenset([7])
    FOLLOW_ID_in_create_package3986 = frozenset([19, 40, 118])
    FOLLOW_invoker_rights_clause_in_create_package3998 = frozenset([19, 40])
    FOLLOW_set_in_create_package4011 = frozenset([5, 6, 7, 8, 18, 24, 42, 73])
    FOLLOW_declare_section_in_create_package4023 = frozenset([42])
    FOLLOW_END_in_create_package4028 = frozenset([5, 7])
    FOLLOW_ID_in_create_package4032 = frozenset([5])
    FOLLOW_SEMI_in_create_package4037 = frozenset([1])
    FOLLOW_CREATE_in_create_package_body4058 = frozenset([44, 115])
    FOLLOW_OR_in_create_package_body4062 = frozenset([7])
    FOLLOW_kREPLACE_in_create_package_body4064 = frozenset([115])
    FOLLOW_PACKAGE_in_create_package_body4069 = frozenset([116])
    FOLLOW_BODY_in_create_package_body4071 = frozenset([7])
    FOLLOW_ID_in_create_package_body4077 = frozenset([33])
    FOLLOW_DOT_in_create_package_body4079 = frozenset([7])
    FOLLOW_ID_in_create_package_body4086 = frozenset([19, 40])
    FOLLOW_set_in_create_package_body4096 = frozenset([5, 6, 7, 8, 18, 24, 41, 42, 73])
    FOLLOW_declare_section_in_create_package_body4108 = frozenset([5, 6, 7, 8, 18, 24, 41, 42, 73])
    FOLLOW_body_in_create_package_body4125 = frozenset([5])
    FOLLOW_END_in_create_package_body4129 = frozenset([5, 7])
    FOLLOW_ID_in_create_package_body4135 = frozenset([5])
    FOLLOW_SEMI_in_create_package_body4150 = frozenset([1])
    FOLLOW_CREATE_in_create_procedure4171 = frozenset([6, 44])
    FOLLOW_OR_in_create_procedure4175 = frozenset([7])
    FOLLOW_kREPLACE_in_create_procedure4177 = frozenset([6])
    FOLLOW_PROCEDURE_in_create_procedure4182 = frozenset([7])
    FOLLOW_ID_in_create_procedure4188 = frozenset([33])
    FOLLOW_DOT_in_create_procedure4190 = frozenset([7])
    FOLLOW_ID_in_create_procedure4197 = frozenset([10, 19, 40, 118])
    FOLLOW_LPAREN_in_create_procedure4209 = frozenset([7])
    FOLLOW_parameter_declaration_in_create_procedure4211 = frozenset([11, 12])
    FOLLOW_COMMA_in_create_procedure4215 = frozenset([7])
    FOLLOW_parameter_declaration_in_create_procedure4217 = frozenset([11, 12])
    FOLLOW_RPAREN_in_create_procedure4222 = frozenset([19, 40, 118])
    FOLLOW_invoker_rights_clause_in_create_procedure4235 = frozenset([19, 40])
    FOLLOW_set_in_create_procedure4246 = frozenset([5, 6, 7, 8, 18, 24, 41, 73, 117, 121])
    FOLLOW_declare_section_in_create_procedure4266 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_create_procedure4269 = frozenset([5])
    FOLLOW_call_spec_in_create_procedure4281 = frozenset([5])
    FOLLOW_EXTERNAL_in_create_procedure4293 = frozenset([5])
    FOLLOW_SEMI_in_create_procedure4305 = frozenset([1])
    FOLLOW_CREATE_in_create_function4326 = frozenset([8, 44])
    FOLLOW_OR_in_create_function4330 = frozenset([7])
    FOLLOW_kREPLACE_in_create_function4332 = frozenset([8])
    FOLLOW_FUNCTION_in_create_function4337 = frozenset([7])
    FOLLOW_ID_in_create_function4343 = frozenset([33])
    FOLLOW_DOT_in_create_function4345 = frozenset([7])
    FOLLOW_ID_in_create_function4352 = frozenset([9, 10])
    FOLLOW_LPAREN_in_create_function4364 = frozenset([7])
    FOLLOW_parameter_declaration_in_create_function4366 = frozenset([11, 12])
    FOLLOW_COMMA_in_create_function4370 = frozenset([7])
    FOLLOW_parameter_declaration_in_create_function4372 = frozenset([11, 12])
    FOLLOW_RPAREN_in_create_function4377 = frozenset([9])
    FOLLOW_RETURN_in_create_function4390 = frozenset([7, 32])
    FOLLOW_datatype_in_create_function4392 = frozenset([19, 40, 118])
    FOLLOW_invoker_rights_clause_in_create_function4402 = frozenset([19, 40])
    FOLLOW_set_in_create_function4413 = frozenset([5, 6, 7, 8, 18, 24, 41, 73, 117, 121])
    FOLLOW_declare_section_in_create_function4433 = frozenset([5, 6, 7, 8, 18, 24, 41, 73])
    FOLLOW_body_in_create_function4436 = frozenset([5])
    FOLLOW_call_spec_in_create_function4448 = frozenset([5])
    FOLLOW_EXTERNAL_in_create_function4460 = frozenset([5])
    FOLLOW_SEMI_in_create_function4472 = frozenset([1])
    FOLLOW_AUTHID_in_invoker_rights_clause4493 = frozenset([119, 120])
    FOLLOW_set_in_invoker_rights_clause4495 = frozenset([1])
    FOLLOW_LANGUAGE_in_call_spec4520 = frozenset([4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132])
    FOLLOW_swallow_to_semi_in_call_spec4522 = frozenset([1])
    FOLLOW_ID_in_kERRORS4537 = frozenset([1])
    FOLLOW_ID_in_kEXCEPTIONS4546 = frozenset([1])
    FOLLOW_ID_in_kFOUND4555 = frozenset([1])
    FOLLOW_ID_in_kINDICES4564 = frozenset([1])
    FOLLOW_ID_in_kMOD4573 = frozenset([1])
    FOLLOW_ID_in_kNAME4582 = frozenset([1])
    FOLLOW_ID_in_kOF4591 = frozenset([1])
    FOLLOW_ID_in_kREPLACE4600 = frozenset([1])
    FOLLOW_ID_in_kROWCOUNT4609 = frozenset([1])
    FOLLOW_ID_in_kSAVE4618 = frozenset([1])
    FOLLOW_ID_in_kSHOW4627 = frozenset([1])
    FOLLOW_ID_in_kTYPE4636 = frozenset([1])
    FOLLOW_ID_in_kVALUES4645 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("sqlLexer", sqlParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
