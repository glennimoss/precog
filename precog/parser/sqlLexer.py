# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 sql.g 2011-07-27 17:07:16

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
FUNCTION=8
PACKAGE=115
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
LOOP=49
BEGIN=41
SAVEPOINT=82
RETURN=9
RAISE=74
BODY=116
GEQ=93
EQ=88
GOTO=69
SELECT=83
INTO=59
ISOPEN=102
ARRAY=27
DIVIDE=4
EXCEPTION=23
EXIT=56
RBRACK=125
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
THEN=46
IN=13
CONTINUE=53
COMMA=11
IS=19
PLUS=96
QUOTED_STRING=108
EXISTS=109
DOT=33
LIKE=94
INTEGER=104
VARRAY=28
BY=31
PERCENT=34
PARALLEL_ENABLE=38
DOUBLEQUOTED_STRING=122
DEFAULT=17
FORALL=65
SET=84
MINUS=95
SEMI=5
TRUE=106
PROCEDURE=6
NOT_EQ=89
REF=32
VERTBAR=127
LTH=90
OPEN=72
COLON=47
COMMIT=78
BULK_ROWCOUNT=101
CLOSE=52
WHEN=43
ASSIGN=16
IMMEDIATE=55
NUMBER_VALUE=129
DECLARE=75
ARROW=113
DELETING=112
BULK=60
BETWEEN=67
LEQ=91


class sqlLexer(Lexer):

    grammarFileName = "sql.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(sqlLexer, self).__init__(input, state)


        self.dfa9 = self.DFA9(
            self, 9,
            eot = self.DFA9_eot,
            eof = self.DFA9_eof,
            min = self.DFA9_min,
            max = self.DFA9_max,
            accept = self.DFA9_accept,
            special = self.DFA9_special,
            transition = self.DFA9_transition
            )

        self.dfa15 = self.DFA15(
            self, 15,
            eot = self.DFA15_eot,
            eof = self.DFA15_eof,
            min = self.DFA15_min,
            max = self.DFA15_max,
            accept = self.DFA15_accept,
            special = self.DFA15_special,
            transition = self.DFA15_transition
            )




                               
    # needed for things like BETWEEN 1..2 where 1. would be treated as a literal
    def numberDotValid ():
        i = 1
        while input.LA(i) >= '0' and input.LA(i) <= '9':
            i += 1
        return input.LA(i) == '.' and input.LA(i+1) != '.'



    # $ANTLR start "AND"
    def mAND(self, ):

        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # sql.g:584:5: ( 'and' )
            # sql.g:584:7: 'and'
            pass 
            self.match("and")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AND"



    # $ANTLR start "ARRAY"
    def mARRAY(self, ):

        try:
            _type = ARRAY
            _channel = DEFAULT_CHANNEL

            # sql.g:585:7: ( 'array' )
            # sql.g:585:9: 'array'
            pass 
            self.match("array")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ARRAY"



    # $ANTLR start "AS"
    def mAS(self, ):

        try:
            _type = AS
            _channel = DEFAULT_CHANNEL

            # sql.g:586:4: ( 'as' )
            # sql.g:586:6: 'as'
            pass 
            self.match("as")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AS"



    # $ANTLR start "AUTHID"
    def mAUTHID(self, ):

        try:
            _type = AUTHID
            _channel = DEFAULT_CHANNEL

            # sql.g:587:7: ( 'authid' )
            # sql.g:587:9: 'authid'
            pass 
            self.match("authid")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AUTHID"



    # $ANTLR start "BETWEEN"
    def mBETWEEN(self, ):

        try:
            _type = BETWEEN
            _channel = DEFAULT_CHANNEL

            # sql.g:588:9: ( 'between' )
            # sql.g:588:11: 'between'
            pass 
            self.match("between")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BETWEEN"



    # $ANTLR start "BODY"
    def mBODY(self, ):

        try:
            _type = BODY
            _channel = DEFAULT_CHANNEL

            # sql.g:589:6: ( 'body' )
            # sql.g:589:8: 'body'
            pass 
            self.match("body")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BODY"



    # $ANTLR start "BULK"
    def mBULK(self, ):

        try:
            _type = BULK
            _channel = DEFAULT_CHANNEL

            # sql.g:590:5: ( 'bulk' )
            # sql.g:590:7: 'bulk'
            pass 
            self.match("bulk")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BULK"



    # $ANTLR start "BULK_ROWCOUNT"
    def mBULK_ROWCOUNT(self, ):

        try:
            _type = BULK_ROWCOUNT
            _channel = DEFAULT_CHANNEL

            # sql.g:591:14: ( 'bulk_rowcount' )
            # sql.g:591:16: 'bulk_rowcount'
            pass 
            self.match("bulk_rowcount")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BULK_ROWCOUNT"



    # $ANTLR start "BY"
    def mBY(self, ):

        try:
            _type = BY
            _channel = DEFAULT_CHANNEL

            # sql.g:592:4: ( 'by' )
            # sql.g:592:6: 'by'
            pass 
            self.match("by")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BY"



    # $ANTLR start "CASE"
    def mCASE(self, ):

        try:
            _type = CASE
            _channel = DEFAULT_CHANNEL

            # sql.g:593:5: ( 'case' )
            # sql.g:593:7: 'case'
            pass 
            self.match("case")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CASE"



    # $ANTLR start "CREATE"
    def mCREATE(self, ):

        try:
            _type = CREATE
            _channel = DEFAULT_CHANNEL

            # sql.g:594:7: ( 'create' )
            # sql.g:594:9: 'create'
            pass 
            self.match("create")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CREATE"



    # $ANTLR start "COLLECT"
    def mCOLLECT(self, ):

        try:
            _type = COLLECT
            _channel = DEFAULT_CHANNEL

            # sql.g:595:8: ( 'collect' )
            # sql.g:595:10: 'collect'
            pass 
            self.match("collect")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COLLECT"



    # $ANTLR start "COMMIT"
    def mCOMMIT(self, ):

        try:
            _type = COMMIT
            _channel = DEFAULT_CHANNEL

            # sql.g:596:8: ( 'commit' )
            # sql.g:596:10: 'commit'
            pass 
            self.match("commit")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COMMIT"



    # $ANTLR start "CURRENT_USER"
    def mCURRENT_USER(self, ):

        try:
            _type = CURRENT_USER
            _channel = DEFAULT_CHANNEL

            # sql.g:597:13: ( 'current_user' )
            # sql.g:597:15: 'current_user'
            pass 
            self.match("current_user")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CURRENT_USER"



    # $ANTLR start "DEFAULT"
    def mDEFAULT(self, ):

        try:
            _type = DEFAULT
            _channel = DEFAULT_CHANNEL

            # sql.g:598:9: ( 'default' )
            # sql.g:598:11: 'default'
            pass 
            self.match("default")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DEFAULT"



    # $ANTLR start "DEFINER"
    def mDEFINER(self, ):

        try:
            _type = DEFINER
            _channel = DEFAULT_CHANNEL

            # sql.g:599:8: ( 'definer' )
            # sql.g:599:10: 'definer'
            pass 
            self.match("definer")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DEFINER"



    # $ANTLR start "DELETE"
    def mDELETE(self, ):

        try:
            _type = DELETE
            _channel = DEFAULT_CHANNEL

            # sql.g:600:8: ( 'delete' )
            # sql.g:600:10: 'delete'
            pass 
            self.match("delete")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DELETE"



    # $ANTLR start "ELSE"
    def mELSE(self, ):

        try:
            _type = ELSE
            _channel = DEFAULT_CHANNEL

            # sql.g:601:6: ( 'else' )
            # sql.g:601:8: 'else'
            pass 
            self.match("else")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ELSE"



    # $ANTLR start "ELSIF"
    def mELSIF(self, ):

        try:
            _type = ELSIF
            _channel = DEFAULT_CHANNEL

            # sql.g:602:7: ( 'elsif' )
            # sql.g:602:9: 'elsif'
            pass 
            self.match("elsif")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ELSIF"



    # $ANTLR start "EXTERNAL"
    def mEXTERNAL(self, ):

        try:
            _type = EXTERNAL
            _channel = DEFAULT_CHANNEL

            # sql.g:603:9: ( 'external' )
            # sql.g:603:11: 'external'
            pass 
            self.match("external")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXTERNAL"



    # $ANTLR start "FALSE"
    def mFALSE(self, ):

        try:
            _type = FALSE
            _channel = DEFAULT_CHANNEL

            # sql.g:604:7: ( 'false' )
            # sql.g:604:9: 'false'
            pass 
            self.match("false")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FALSE"



    # $ANTLR start "FETCH"
    def mFETCH(self, ):

        try:
            _type = FETCH
            _channel = DEFAULT_CHANNEL

            # sql.g:605:7: ( 'fetch' )
            # sql.g:605:9: 'fetch'
            pass 
            self.match("fetch")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FETCH"



    # $ANTLR start "FOR"
    def mFOR(self, ):

        try:
            _type = FOR
            _channel = DEFAULT_CHANNEL

            # sql.g:606:5: ( 'for' )
            # sql.g:606:7: 'for'
            pass 
            self.match("for")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FOR"



    # $ANTLR start "FORALL"
    def mFORALL(self, ):

        try:
            _type = FORALL
            _channel = DEFAULT_CHANNEL

            # sql.g:607:8: ( 'forall' )
            # sql.g:607:10: 'forall'
            pass 
            self.match("forall")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FORALL"



    # $ANTLR start "GOTO"
    def mGOTO(self, ):

        try:
            _type = GOTO
            _channel = DEFAULT_CHANNEL

            # sql.g:608:6: ( 'goto' )
            # sql.g:608:8: 'goto'
            pass 
            self.match("goto")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "GOTO"



    # $ANTLR start "IF"
    def mIF(self, ):

        try:
            _type = IF
            _channel = DEFAULT_CHANNEL

            # sql.g:609:4: ( 'if' )
            # sql.g:609:6: 'if'
            pass 
            self.match("if")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IF"



    # $ANTLR start "IN"
    def mIN(self, ):

        try:
            _type = IN
            _channel = DEFAULT_CHANNEL

            # sql.g:610:4: ( 'in' )
            # sql.g:610:6: 'in'
            pass 
            self.match("in")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IN"



    # $ANTLR start "INDEX"
    def mINDEX(self, ):

        try:
            _type = INDEX
            _channel = DEFAULT_CHANNEL

            # sql.g:611:7: ( 'index' )
            # sql.g:611:9: 'index'
            pass 
            self.match("index")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INDEX"



    # $ANTLR start "INSERT"
    def mINSERT(self, ):

        try:
            _type = INSERT
            _channel = DEFAULT_CHANNEL

            # sql.g:612:8: ( 'insert' )
            # sql.g:612:10: 'insert'
            pass 
            self.match("insert")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INSERT"



    # $ANTLR start "INTO"
    def mINTO(self, ):

        try:
            _type = INTO
            _channel = DEFAULT_CHANNEL

            # sql.g:613:6: ( 'into' )
            # sql.g:613:8: 'into'
            pass 
            self.match("into")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INTO"



    # $ANTLR start "IS"
    def mIS(self, ):

        try:
            _type = IS
            _channel = DEFAULT_CHANNEL

            # sql.g:614:4: ( 'is' )
            # sql.g:614:6: 'is'
            pass 
            self.match("is")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IS"



    # $ANTLR start "LANGUAGE"
    def mLANGUAGE(self, ):

        try:
            _type = LANGUAGE
            _channel = DEFAULT_CHANNEL

            # sql.g:615:9: ( 'language' )
            # sql.g:615:11: 'language'
            pass 
            self.match("language")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LANGUAGE"



    # $ANTLR start "LIKE"
    def mLIKE(self, ):

        try:
            _type = LIKE
            _channel = DEFAULT_CHANNEL

            # sql.g:616:6: ( 'like' )
            # sql.g:616:8: 'like'
            pass 
            self.match("like")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LIKE"



    # $ANTLR start "LIMIT"
    def mLIMIT(self, ):

        try:
            _type = LIMIT
            _channel = DEFAULT_CHANNEL

            # sql.g:617:7: ( 'limit' )
            # sql.g:617:9: 'limit'
            pass 
            self.match("limit")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LIMIT"



    # $ANTLR start "LOCK"
    def mLOCK(self, ):

        try:
            _type = LOCK
            _channel = DEFAULT_CHANNEL

            # sql.g:618:6: ( 'lock' )
            # sql.g:618:8: 'lock'
            pass 
            self.match("lock")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LOCK"



    # $ANTLR start "NOT"
    def mNOT(self, ):

        try:
            _type = NOT
            _channel = DEFAULT_CHANNEL

            # sql.g:619:5: ( 'not' )
            # sql.g:619:7: 'not'
            pass 
            self.match("not")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOT"



    # $ANTLR start "NOTFOUND"
    def mNOTFOUND(self, ):

        try:
            _type = NOTFOUND
            _channel = DEFAULT_CHANNEL

            # sql.g:620:9: ( 'notfound' )
            # sql.g:620:11: 'notfound'
            pass 
            self.match("notfound")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOTFOUND"



    # $ANTLR start "NULL"
    def mNULL(self, ):

        try:
            _type = NULL
            _channel = DEFAULT_CHANNEL

            # sql.g:621:6: ( 'null' )
            # sql.g:621:8: 'null'
            pass 
            self.match("null")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NULL"



    # $ANTLR start "OPEN"
    def mOPEN(self, ):

        try:
            _type = OPEN
            _channel = DEFAULT_CHANNEL

            # sql.g:622:6: ( 'open' )
            # sql.g:622:8: 'open'
            pass 
            self.match("open")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OPEN"



    # $ANTLR start "OR"
    def mOR(self, ):

        try:
            _type = OR
            _channel = DEFAULT_CHANNEL

            # sql.g:623:4: ( 'or' )
            # sql.g:623:6: 'or'
            pass 
            self.match("or")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OR"



    # $ANTLR start "PACKAGE"
    def mPACKAGE(self, ):

        try:
            _type = PACKAGE
            _channel = DEFAULT_CHANNEL

            # sql.g:624:8: ( 'package' )
            # sql.g:624:10: 'package'
            pass 
            self.match("package")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PACKAGE"



    # $ANTLR start "RAISE"
    def mRAISE(self, ):

        try:
            _type = RAISE
            _channel = DEFAULT_CHANNEL

            # sql.g:625:7: ( 'raise' )
            # sql.g:625:9: 'raise'
            pass 
            self.match("raise")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RAISE"



    # $ANTLR start "ROLLBACK"
    def mROLLBACK(self, ):

        try:
            _type = ROLLBACK
            _channel = DEFAULT_CHANNEL

            # sql.g:626:9: ( 'rollback' )
            # sql.g:626:11: 'rollback'
            pass 
            self.match("rollback")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ROLLBACK"



    # $ANTLR start "SAVEPOINT"
    def mSAVEPOINT(self, ):

        try:
            _type = SAVEPOINT
            _channel = DEFAULT_CHANNEL

            # sql.g:627:11: ( 'savepoint' )
            # sql.g:627:13: 'savepoint'
            pass 
            self.match("savepoint")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SAVEPOINT"



    # $ANTLR start "SELECT"
    def mSELECT(self, ):

        try:
            _type = SELECT
            _channel = DEFAULT_CHANNEL

            # sql.g:628:8: ( 'select' )
            # sql.g:628:10: 'select'
            pass 
            self.match("select")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SELECT"



    # $ANTLR start "SET"
    def mSET(self, ):

        try:
            _type = SET
            _channel = DEFAULT_CHANNEL

            # sql.g:629:5: ( 'set' )
            # sql.g:629:7: 'set'
            pass 
            self.match("set")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SET"



    # $ANTLR start "SQL"
    def mSQL(self, ):

        try:
            _type = SQL
            _channel = DEFAULT_CHANNEL

            # sql.g:630:5: ( 'sql' )
            # sql.g:630:7: 'sql'
            pass 
            self.match("sql")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SQL"



    # $ANTLR start "TABLE"
    def mTABLE(self, ):

        try:
            _type = TABLE
            _channel = DEFAULT_CHANNEL

            # sql.g:631:7: ( 'table' )
            # sql.g:631:9: 'table'
            pass 
            self.match("table")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TABLE"



    # $ANTLR start "TRANSACTION"
    def mTRANSACTION(self, ):

        try:
            _type = TRANSACTION
            _channel = DEFAULT_CHANNEL

            # sql.g:632:13: ( 'transaction' )
            # sql.g:632:15: 'transaction'
            pass 
            self.match("transaction")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TRANSACTION"



    # $ANTLR start "TRUE"
    def mTRUE(self, ):

        try:
            _type = TRUE
            _channel = DEFAULT_CHANNEL

            # sql.g:633:6: ( 'true' )
            # sql.g:633:8: 'true'
            pass 
            self.match("true")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TRUE"



    # $ANTLR start "THEN"
    def mTHEN(self, ):

        try:
            _type = THEN
            _channel = DEFAULT_CHANNEL

            # sql.g:634:6: ( 'then' )
            # sql.g:634:8: 'then'
            pass 
            self.match("then")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "THEN"



    # $ANTLR start "UPDATE"
    def mUPDATE(self, ):

        try:
            _type = UPDATE
            _channel = DEFAULT_CHANNEL

            # sql.g:635:8: ( 'update' )
            # sql.g:635:10: 'update'
            pass 
            self.match("update")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "UPDATE"



    # $ANTLR start "WHILE"
    def mWHILE(self, ):

        try:
            _type = WHILE
            _channel = DEFAULT_CHANNEL

            # sql.g:636:7: ( 'while' )
            # sql.g:636:9: 'while'
            pass 
            self.match("while")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WHILE"



    # $ANTLR start "INSERTING"
    def mINSERTING(self, ):

        try:
            _type = INSERTING
            _channel = DEFAULT_CHANNEL

            # sql.g:638:2: ( 'inserting' )
            # sql.g:638:4: 'inserting'
            pass 
            self.match("inserting")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INSERTING"



    # $ANTLR start "UPDATING"
    def mUPDATING(self, ):

        try:
            _type = UPDATING
            _channel = DEFAULT_CHANNEL

            # sql.g:639:9: ( 'updating' )
            # sql.g:639:11: 'updating'
            pass 
            self.match("updating")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "UPDATING"



    # $ANTLR start "DELETING"
    def mDELETING(self, ):

        try:
            _type = DELETING
            _channel = DEFAULT_CHANNEL

            # sql.g:640:9: ( 'deleting' )
            # sql.g:640:11: 'deleting'
            pass 
            self.match("deleting")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DELETING"



    # $ANTLR start "ISOPEN"
    def mISOPEN(self, ):

        try:
            _type = ISOPEN
            _channel = DEFAULT_CHANNEL

            # sql.g:641:8: ( 'isopen' )
            # sql.g:641:10: 'isopen'
            pass 
            self.match("isopen")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ISOPEN"



    # $ANTLR start "EXISTS"
    def mEXISTS(self, ):

        try:
            _type = EXISTS
            _channel = DEFAULT_CHANNEL

            # sql.g:642:8: ( 'exists' )
            # sql.g:642:10: 'exists'
            pass 
            self.match("exists")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXISTS"



    # $ANTLR start "BEGIN"
    def mBEGIN(self, ):

        try:
            _type = BEGIN
            _channel = DEFAULT_CHANNEL

            # sql.g:644:7: ( 'begin' )
            # sql.g:644:9: 'begin'
            pass 
            self.match("begin")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BEGIN"



    # $ANTLR start "CLOSE"
    def mCLOSE(self, ):

        try:
            _type = CLOSE
            _channel = DEFAULT_CHANNEL

            # sql.g:645:7: ( 'close' )
            # sql.g:645:9: 'close'
            pass 
            self.match("close")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CLOSE"



    # $ANTLR start "CONSTANT"
    def mCONSTANT(self, ):

        try:
            _type = CONSTANT
            _channel = DEFAULT_CHANNEL

            # sql.g:646:10: ( 'constant' )
            # sql.g:646:12: 'constant'
            pass 
            self.match("constant")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CONSTANT"



    # $ANTLR start "CONTINUE"
    def mCONTINUE(self, ):

        try:
            _type = CONTINUE
            _channel = DEFAULT_CHANNEL

            # sql.g:647:9: ( 'continue' )
            # sql.g:647:11: 'continue'
            pass 
            self.match("continue")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CONTINUE"



    # $ANTLR start "CURSOR"
    def mCURSOR(self, ):

        try:
            _type = CURSOR
            _channel = DEFAULT_CHANNEL

            # sql.g:648:8: ( 'cursor' )
            # sql.g:648:10: 'cursor'
            pass 
            self.match("cursor")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CURSOR"



    # $ANTLR start "DECLARE"
    def mDECLARE(self, ):

        try:
            _type = DECLARE
            _channel = DEFAULT_CHANNEL

            # sql.g:649:9: ( 'declare' )
            # sql.g:649:11: 'declare'
            pass 
            self.match("declare")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DECLARE"



    # $ANTLR start "DETERMINISTIC"
    def mDETERMINISTIC(self, ):

        try:
            _type = DETERMINISTIC
            _channel = DEFAULT_CHANNEL

            # sql.g:650:15: ( 'deterministic' )
            # sql.g:650:17: 'deterministic'
            pass 
            self.match("deterministic")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DETERMINISTIC"



    # $ANTLR start "END"
    def mEND(self, ):

        try:
            _type = END
            _channel = DEFAULT_CHANNEL

            # sql.g:651:5: ( 'end' )
            # sql.g:651:7: 'end'
            pass 
            self.match("end")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "END"



    # $ANTLR start "EXCEPTION"
    def mEXCEPTION(self, ):

        try:
            _type = EXCEPTION
            _channel = DEFAULT_CHANNEL

            # sql.g:652:11: ( 'exception' )
            # sql.g:652:13: 'exception'
            pass 
            self.match("exception")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXCEPTION"



    # $ANTLR start "EXECUTE"
    def mEXECUTE(self, ):

        try:
            _type = EXECUTE
            _channel = DEFAULT_CHANNEL

            # sql.g:653:9: ( 'execute' )
            # sql.g:653:11: 'execute'
            pass 
            self.match("execute")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXECUTE"



    # $ANTLR start "EXIT"
    def mEXIT(self, ):

        try:
            _type = EXIT
            _channel = DEFAULT_CHANNEL

            # sql.g:654:6: ( 'exit' )
            # sql.g:654:8: 'exit'
            pass 
            self.match("exit")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXIT"



    # $ANTLR start "FUNCTION"
    def mFUNCTION(self, ):

        try:
            _type = FUNCTION
            _channel = DEFAULT_CHANNEL

            # sql.g:655:10: ( 'function' )
            # sql.g:655:12: 'function'
            pass 
            self.match("function")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FUNCTION"



    # $ANTLR start "IMMEDIATE"
    def mIMMEDIATE(self, ):

        try:
            _type = IMMEDIATE
            _channel = DEFAULT_CHANNEL

            # sql.g:656:11: ( 'immediate' )
            # sql.g:656:13: 'immediate'
            pass 
            self.match("immediate")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IMMEDIATE"



    # $ANTLR start "LOOP"
    def mLOOP(self, ):

        try:
            _type = LOOP
            _channel = DEFAULT_CHANNEL

            # sql.g:657:6: ( 'loop' )
            # sql.g:657:8: 'loop'
            pass 
            self.match("loop")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LOOP"



    # $ANTLR start "NOCOPY"
    def mNOCOPY(self, ):

        try:
            _type = NOCOPY
            _channel = DEFAULT_CHANNEL

            # sql.g:658:8: ( 'nocopy' )
            # sql.g:658:10: 'nocopy'
            pass 
            self.match("nocopy")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOCOPY"



    # $ANTLR start "OTHERS"
    def mOTHERS(self, ):

        try:
            _type = OTHERS
            _channel = DEFAULT_CHANNEL

            # sql.g:659:8: ( 'others' )
            # sql.g:659:10: 'others'
            pass 
            self.match("others")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OTHERS"



    # $ANTLR start "OUT"
    def mOUT(self, ):

        try:
            _type = OUT
            _channel = DEFAULT_CHANNEL

            # sql.g:660:5: ( 'out' )
            # sql.g:660:7: 'out'
            pass 
            self.match("out")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OUT"



    # $ANTLR start "PARALLEL_ENABLE"
    def mPARALLEL_ENABLE(self, ):

        try:
            _type = PARALLEL_ENABLE
            _channel = DEFAULT_CHANNEL

            # sql.g:661:17: ( 'parallel_enable' )
            # sql.g:661:19: 'parallel_enable'
            pass 
            self.match("parallel_enable")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PARALLEL_ENABLE"



    # $ANTLR start "PIPELINED"
    def mPIPELINED(self, ):

        try:
            _type = PIPELINED
            _channel = DEFAULT_CHANNEL

            # sql.g:662:11: ( 'pipelined' )
            # sql.g:662:13: 'pipelined'
            pass 
            self.match("pipelined")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PIPELINED"



    # $ANTLR start "PRAGMA"
    def mPRAGMA(self, ):

        try:
            _type = PRAGMA
            _channel = DEFAULT_CHANNEL

            # sql.g:663:8: ( 'pragma' )
            # sql.g:663:10: 'pragma'
            pass 
            self.match("pragma")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PRAGMA"



    # $ANTLR start "PROCEDURE"
    def mPROCEDURE(self, ):

        try:
            _type = PROCEDURE
            _channel = DEFAULT_CHANNEL

            # sql.g:664:11: ( 'procedure' )
            # sql.g:664:13: 'procedure'
            pass 
            self.match("procedure")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PROCEDURE"



    # $ANTLR start "RECORD"
    def mRECORD(self, ):

        try:
            _type = RECORD
            _channel = DEFAULT_CHANNEL

            # sql.g:665:8: ( 'record' )
            # sql.g:665:10: 'record'
            pass 
            self.match("record")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RECORD"



    # $ANTLR start "REF"
    def mREF(self, ):

        try:
            _type = REF
            _channel = DEFAULT_CHANNEL

            # sql.g:666:5: ( 'ref' )
            # sql.g:666:7: 'ref'
            pass 
            self.match("ref")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "REF"



    # $ANTLR start "RESULT_CACHE"
    def mRESULT_CACHE(self, ):

        try:
            _type = RESULT_CACHE
            _channel = DEFAULT_CHANNEL

            # sql.g:667:14: ( 'result_cache' )
            # sql.g:667:16: 'result_cache'
            pass 
            self.match("result_cache")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RESULT_CACHE"



    # $ANTLR start "RETURN"
    def mRETURN(self, ):

        try:
            _type = RETURN
            _channel = DEFAULT_CHANNEL

            # sql.g:668:8: ( 'return' )
            # sql.g:668:10: 'return'
            pass 
            self.match("return")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RETURN"



    # $ANTLR start "RETURNING"
    def mRETURNING(self, ):

        try:
            _type = RETURNING
            _channel = DEFAULT_CHANNEL

            # sql.g:669:11: ( 'returning' )
            # sql.g:669:13: 'returning'
            pass 
            self.match("returning")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RETURNING"



    # $ANTLR start "ROWTYPE"
    def mROWTYPE(self, ):

        try:
            _type = ROWTYPE
            _channel = DEFAULT_CHANNEL

            # sql.g:670:9: ( 'rowtype' )
            # sql.g:670:11: 'rowtype'
            pass 
            self.match("rowtype")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ROWTYPE"



    # $ANTLR start "SUBTYPE"
    def mSUBTYPE(self, ):

        try:
            _type = SUBTYPE
            _channel = DEFAULT_CHANNEL

            # sql.g:671:9: ( 'subtype' )
            # sql.g:671:11: 'subtype'
            pass 
            self.match("subtype")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SUBTYPE"



    # $ANTLR start "USING"
    def mUSING(self, ):

        try:
            _type = USING
            _channel = DEFAULT_CHANNEL

            # sql.g:672:6: ( 'using' )
            # sql.g:672:8: 'using'
            pass 
            self.match("using")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "USING"



    # $ANTLR start "VARRAY"
    def mVARRAY(self, ):

        try:
            _type = VARRAY
            _channel = DEFAULT_CHANNEL

            # sql.g:673:8: ( 'varray' )
            # sql.g:673:10: 'varray'
            pass 
            self.match("varray")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "VARRAY"



    # $ANTLR start "VARYING"
    def mVARYING(self, ):

        try:
            _type = VARYING
            _channel = DEFAULT_CHANNEL

            # sql.g:674:9: ( 'varying' )
            # sql.g:674:11: 'varying'
            pass 
            self.match("varying")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "VARYING"



    # $ANTLR start "WHEN"
    def mWHEN(self, ):

        try:
            _type = WHEN
            _channel = DEFAULT_CHANNEL

            # sql.g:675:6: ( 'when' )
            # sql.g:675:8: 'when'
            pass 
            self.match("when")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WHEN"



    # $ANTLR start "QUOTED_STRING"
    def mQUOTED_STRING(self, ):

        try:
            _type = QUOTED_STRING
            _channel = DEFAULT_CHANNEL

            # sql.g:678:2: ( ( 'n' )? '\\'' ( '\\'\\'' | ~ ( '\\'' ) )* '\\'' )
            # sql.g:678:4: ( 'n' )? '\\'' ( '\\'\\'' | ~ ( '\\'' ) )* '\\''
            pass 
            # sql.g:678:4: ( 'n' )?
            alt1 = 2
            LA1_0 = self.input.LA(1)

            if (LA1_0 == 110) :
                alt1 = 1
            if alt1 == 1:
                # sql.g:678:6: 'n'
                pass 
                self.match(110)



            self.match(39)
            # sql.g:678:18: ( '\\'\\'' | ~ ( '\\'' ) )*
            while True: #loop2
                alt2 = 3
                LA2_0 = self.input.LA(1)

                if (LA2_0 == 39) :
                    LA2_1 = self.input.LA(2)

                    if (LA2_1 == 39) :
                        alt2 = 1


                elif ((0 <= LA2_0 <= 38) or (40 <= LA2_0 <= 65535)) :
                    alt2 = 2


                if alt2 == 1:
                    # sql.g:678:20: '\\'\\''
                    pass 
                    self.match("''")


                elif alt2 == 2:
                    # sql.g:678:29: ~ ( '\\'' )
                    pass 
                    if (0 <= self.input.LA(1) <= 38) or (40 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop2
            self.match(39)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "QUOTED_STRING"



    # $ANTLR start "ID"
    def mID(self, ):

        try:
            _type = ID
            _channel = DEFAULT_CHANNEL

            # sql.g:682:2: ( ( 'a' .. 'z' ) ( 'a' .. 'z' | '0' .. '9' | '_' | '$' | '#' )* | DOUBLEQUOTED_STRING )
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if ((97 <= LA4_0 <= 122)) :
                alt4 = 1
            elif (LA4_0 == 34) :
                alt4 = 2
            else:
                nvae = NoViableAltException("", 4, 0, self.input)

                raise nvae

            if alt4 == 1:
                # sql.g:682:4: ( 'a' .. 'z' ) ( 'a' .. 'z' | '0' .. '9' | '_' | '$' | '#' )*
                pass 
                # sql.g:682:4: ( 'a' .. 'z' )
                # sql.g:682:6: 'a' .. 'z'
                pass 
                self.matchRange(97, 122)



                # sql.g:683:3: ( 'a' .. 'z' | '0' .. '9' | '_' | '$' | '#' )*
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if ((35 <= LA3_0 <= 36) or (48 <= LA3_0 <= 57) or LA3_0 == 95 or (97 <= LA3_0 <= 122)) :
                        alt3 = 1


                    if alt3 == 1:
                        # sql.g:
                        pass 
                        if (35 <= self.input.LA(1) <= 36) or (48 <= self.input.LA(1) <= 57) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse



                    else:
                        break #loop3


            elif alt4 == 2:
                # sql.g:684:4: DOUBLEQUOTED_STRING
                pass 
                self.mDOUBLEQUOTED_STRING()


            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ID"



    # $ANTLR start "SEMI"
    def mSEMI(self, ):

        try:
            _type = SEMI
            _channel = DEFAULT_CHANNEL

            # sql.g:687:2: ( ';' )
            # sql.g:687:4: ';'
            pass 
            self.match(59)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SEMI"



    # $ANTLR start "COLON"
    def mCOLON(self, ):

        try:
            _type = COLON
            _channel = DEFAULT_CHANNEL

            # sql.g:690:2: ( ':' )
            # sql.g:690:4: ':'
            pass 
            self.match(58)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COLON"



    # $ANTLR start "DOUBLEDOT"
    def mDOUBLEDOT(self, ):

        try:
            _type = DOUBLEDOT
            _channel = DEFAULT_CHANNEL

            # sql.g:693:2: ( POINT POINT )
            # sql.g:693:4: POINT POINT
            pass 
            self.mPOINT()
            self.mPOINT()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOUBLEDOT"



    # $ANTLR start "DOT"
    def mDOT(self, ):

        try:
            _type = DOT
            _channel = DEFAULT_CHANNEL

            # sql.g:696:2: ( POINT )
            # sql.g:696:4: POINT
            pass 
            self.mPOINT()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOT"



    # $ANTLR start "POINT"
    def mPOINT(self, ):

        try:
            # sql.g:700:2: ( '.' )
            # sql.g:700:4: '.'
            pass 
            self.match(46)




        finally:

            pass

    # $ANTLR end "POINT"



    # $ANTLR start "COMMA"
    def mCOMMA(self, ):

        try:
            _type = COMMA
            _channel = DEFAULT_CHANNEL

            # sql.g:703:2: ( ',' )
            # sql.g:703:4: ','
            pass 
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COMMA"



    # $ANTLR start "EXPONENT"
    def mEXPONENT(self, ):

        try:
            _type = EXPONENT
            _channel = DEFAULT_CHANNEL

            # sql.g:706:2: ( '**' )
            # sql.g:706:4: '**'
            pass 
            self.match("**")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXPONENT"



    # $ANTLR start "ASTERISK"
    def mASTERISK(self, ):

        try:
            _type = ASTERISK
            _channel = DEFAULT_CHANNEL

            # sql.g:709:2: ( '*' )
            # sql.g:709:4: '*'
            pass 
            self.match(42)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ASTERISK"



    # $ANTLR start "AT_SIGN"
    def mAT_SIGN(self, ):

        try:
            _type = AT_SIGN
            _channel = DEFAULT_CHANNEL

            # sql.g:712:2: ( '@' )
            # sql.g:712:4: '@'
            pass 
            self.match(64)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AT_SIGN"



    # $ANTLR start "RPAREN"
    def mRPAREN(self, ):

        try:
            _type = RPAREN
            _channel = DEFAULT_CHANNEL

            # sql.g:715:2: ( ')' )
            # sql.g:715:4: ')'
            pass 
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RPAREN"



    # $ANTLR start "LPAREN"
    def mLPAREN(self, ):

        try:
            _type = LPAREN
            _channel = DEFAULT_CHANNEL

            # sql.g:718:2: ( '(' )
            # sql.g:718:4: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LPAREN"



    # $ANTLR start "RBRACK"
    def mRBRACK(self, ):

        try:
            _type = RBRACK
            _channel = DEFAULT_CHANNEL

            # sql.g:721:2: ( ']' )
            # sql.g:721:4: ']'
            pass 
            self.match(93)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RBRACK"



    # $ANTLR start "LBRACK"
    def mLBRACK(self, ):

        try:
            _type = LBRACK
            _channel = DEFAULT_CHANNEL

            # sql.g:724:2: ( '[' )
            # sql.g:724:4: '['
            pass 
            self.match(91)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LBRACK"



    # $ANTLR start "PLUS"
    def mPLUS(self, ):

        try:
            _type = PLUS
            _channel = DEFAULT_CHANNEL

            # sql.g:727:2: ( '+' )
            # sql.g:727:4: '+'
            pass 
            self.match(43)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PLUS"



    # $ANTLR start "MINUS"
    def mMINUS(self, ):

        try:
            _type = MINUS
            _channel = DEFAULT_CHANNEL

            # sql.g:730:2: ( '-' )
            # sql.g:730:4: '-'
            pass 
            self.match(45)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "MINUS"



    # $ANTLR start "DIVIDE"
    def mDIVIDE(self, ):

        try:
            _type = DIVIDE
            _channel = DEFAULT_CHANNEL

            # sql.g:733:2: ( '/' )
            # sql.g:733:4: '/'
            pass 
            self.match(47)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DIVIDE"



    # $ANTLR start "EQ"
    def mEQ(self, ):

        try:
            _type = EQ
            _channel = DEFAULT_CHANNEL

            # sql.g:736:2: ( '=' )
            # sql.g:736:4: '='
            pass 
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EQ"



    # $ANTLR start "PERCENT"
    def mPERCENT(self, ):

        try:
            _type = PERCENT
            _channel = DEFAULT_CHANNEL

            # sql.g:739:2: ( '%' )
            # sql.g:739:4: '%'
            pass 
            self.match(37)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PERCENT"



    # $ANTLR start "LLABEL"
    def mLLABEL(self, ):

        try:
            _type = LLABEL
            _channel = DEFAULT_CHANNEL

            # sql.g:742:2: ( '<<' )
            # sql.g:742:4: '<<'
            pass 
            self.match("<<")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LLABEL"



    # $ANTLR start "RLABEL"
    def mRLABEL(self, ):

        try:
            _type = RLABEL
            _channel = DEFAULT_CHANNEL

            # sql.g:745:2: ( '>>' )
            # sql.g:745:4: '>>'
            pass 
            self.match(">>")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RLABEL"



    # $ANTLR start "ASSIGN"
    def mASSIGN(self, ):

        try:
            _type = ASSIGN
            _channel = DEFAULT_CHANNEL

            # sql.g:748:2: ( ':=' )
            # sql.g:748:4: ':='
            pass 
            self.match(":=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ASSIGN"



    # $ANTLR start "ARROW"
    def mARROW(self, ):

        try:
            _type = ARROW
            _channel = DEFAULT_CHANNEL

            # sql.g:751:2: ( '=>' )
            # sql.g:751:4: '=>'
            pass 
            self.match("=>")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ARROW"



    # $ANTLR start "VERTBAR"
    def mVERTBAR(self, ):

        try:
            _type = VERTBAR
            _channel = DEFAULT_CHANNEL

            # sql.g:754:2: ( '|' )
            # sql.g:754:4: '|'
            pass 
            self.match(124)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "VERTBAR"



    # $ANTLR start "DOUBLEVERTBAR"
    def mDOUBLEVERTBAR(self, ):

        try:
            _type = DOUBLEVERTBAR
            _channel = DEFAULT_CHANNEL

            # sql.g:757:2: ( '||' )
            # sql.g:757:4: '||'
            pass 
            self.match("||")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOUBLEVERTBAR"



    # $ANTLR start "NOT_EQ"
    def mNOT_EQ(self, ):

        try:
            _type = NOT_EQ
            _channel = DEFAULT_CHANNEL

            # sql.g:760:2: ( '<>' | '!=' | '~=' | '^=' )
            alt5 = 4
            LA5 = self.input.LA(1)
            if LA5 == 60:
                alt5 = 1
            elif LA5 == 33:
                alt5 = 2
            elif LA5 == 126:
                alt5 = 3
            elif LA5 == 94:
                alt5 = 4
            else:
                nvae = NoViableAltException("", 5, 0, self.input)

                raise nvae

            if alt5 == 1:
                # sql.g:760:4: '<>'
                pass 
                self.match("<>")


            elif alt5 == 2:
                # sql.g:760:11: '!='
                pass 
                self.match("!=")


            elif alt5 == 3:
                # sql.g:760:18: '~='
                pass 
                self.match("~=")


            elif alt5 == 4:
                # sql.g:760:24: '^='
                pass 
                self.match("^=")


            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOT_EQ"



    # $ANTLR start "LTH"
    def mLTH(self, ):

        try:
            _type = LTH
            _channel = DEFAULT_CHANNEL

            # sql.g:763:2: ( '<' )
            # sql.g:763:4: '<'
            pass 
            self.match(60)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LTH"



    # $ANTLR start "LEQ"
    def mLEQ(self, ):

        try:
            _type = LEQ
            _channel = DEFAULT_CHANNEL

            # sql.g:766:2: ( '<=' )
            # sql.g:766:4: '<='
            pass 
            self.match("<=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LEQ"



    # $ANTLR start "GTH"
    def mGTH(self, ):

        try:
            _type = GTH
            _channel = DEFAULT_CHANNEL

            # sql.g:769:2: ( '>' )
            # sql.g:769:4: '>'
            pass 
            self.match(62)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "GTH"



    # $ANTLR start "GEQ"
    def mGEQ(self, ):

        try:
            _type = GEQ
            _channel = DEFAULT_CHANNEL

            # sql.g:772:2: ( '>=' )
            # sql.g:772:4: '>='
            pass 
            self.match(">=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "GEQ"



    # $ANTLR start "INTEGER"
    def mINTEGER(self, ):

        try:
            _type = INTEGER
            _channel = DEFAULT_CHANNEL

            # sql.g:775:5: ( N )
            # sql.g:775:9: N
            pass 
            self.mN()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INTEGER"



    # $ANTLR start "REAL_NUMBER"
    def mREAL_NUMBER(self, ):

        try:
            _type = REAL_NUMBER
            _channel = DEFAULT_CHANNEL

            # sql.g:778:2: ( NUMBER_VALUE ( 'e' ( PLUS | MINUS )? N )? )
            # sql.g:778:4: NUMBER_VALUE ( 'e' ( PLUS | MINUS )? N )?
            pass 
            self.mNUMBER_VALUE()
            # sql.g:778:17: ( 'e' ( PLUS | MINUS )? N )?
            alt7 = 2
            LA7_0 = self.input.LA(1)

            if (LA7_0 == 101) :
                alt7 = 1
            if alt7 == 1:
                # sql.g:778:19: 'e' ( PLUS | MINUS )? N
                pass 
                self.match(101)
                # sql.g:778:23: ( PLUS | MINUS )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 43 or LA6_0 == 45) :
                    alt6 = 1
                if alt6 == 1:
                    # sql.g:
                    pass 
                    if self.input.LA(1) == 43 or self.input.LA(1) == 45:
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                self.mN()






            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "REAL_NUMBER"



    # $ANTLR start "NUMBER_VALUE"
    def mNUMBER_VALUE(self, ):

        try:
            # sql.g:782:2: ({...}? => N POINT ( N )? | POINT N | N )
            alt9 = 3
            alt9 = self.dfa9.predict(self.input)
            if alt9 == 1:
                # sql.g:782:4: {...}? => N POINT ( N )?
                pass 
                if not ((self.numberDotValid())):
                    raise FailedPredicateException(self.input, "NUMBER_VALUE", "self.numberDotValid()")

                self.mN()
                self.mPOINT()
                # sql.g:782:39: ( N )?
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if ((48 <= LA8_0 <= 57)) :
                    alt8 = 1
                if alt8 == 1:
                    # sql.g:782:39: N
                    pass 
                    self.mN()





            elif alt9 == 2:
                # sql.g:783:4: POINT N
                pass 
                self.mPOINT()
                self.mN()


            elif alt9 == 3:
                # sql.g:784:4: N
                pass 
                self.mN()



        finally:

            pass

    # $ANTLR end "NUMBER_VALUE"



    # $ANTLR start "N"
    def mN(self, ):

        try:
            # sql.g:788:2: ( '0' .. '9' ( '0' .. '9' )* )
            # sql.g:788:4: '0' .. '9' ( '0' .. '9' )*
            pass 
            self.matchRange(48, 57)
            # sql.g:788:15: ( '0' .. '9' )*
            while True: #loop10
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if ((48 <= LA10_0 <= 57)) :
                    alt10 = 1


                if alt10 == 1:
                    # sql.g:788:17: '0' .. '9'
                    pass 
                    self.matchRange(48, 57)


                else:
                    break #loop10




        finally:

            pass

    # $ANTLR end "N"



    # $ANTLR start "DOUBLEQUOTED_STRING"
    def mDOUBLEQUOTED_STRING(self, ):

        try:
            # sql.g:792:2: ( '\"' (~ ( '\"' ) )* '\"' )
            # sql.g:792:4: '\"' (~ ( '\"' ) )* '\"'
            pass 
            self.match(34)
            # sql.g:792:8: (~ ( '\"' ) )*
            while True: #loop11
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if ((0 <= LA11_0 <= 33) or (35 <= LA11_0 <= 65535)) :
                    alt11 = 1


                if alt11 == 1:
                    # sql.g:792:10: ~ ( '\"' )
                    pass 
                    if (0 <= self.input.LA(1) <= 33) or (35 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop11
            self.match(34)




        finally:

            pass

    # $ANTLR end "DOUBLEQUOTED_STRING"



    # $ANTLR start "WS"
    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # sql.g:794:4: ( ( ' ' | '\\r' | '\\t' | '\\n' ) )
            # sql.g:794:6: ( ' ' | '\\r' | '\\t' | '\\n' )
            pass 
            if (9 <= self.input.LA(1) <= 10) or self.input.LA(1) == 13 or self.input.LA(1) == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse

            #action start
            _channel=HIDDEN;
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WS"



    # $ANTLR start "SL_COMMENT"
    def mSL_COMMENT(self, ):

        try:
            _type = SL_COMMENT
            _channel = DEFAULT_CHANNEL

            # sql.g:797:2: ( '--' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # sql.g:797:4: '--' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            pass 
            self.match("--")
            # sql.g:797:9: (~ ( '\\n' | '\\r' ) )*
            while True: #loop12
                alt12 = 2
                LA12_0 = self.input.LA(1)

                if ((0 <= LA12_0 <= 9) or (11 <= LA12_0 <= 12) or (14 <= LA12_0 <= 65535)) :
                    alt12 = 1


                if alt12 == 1:
                    # sql.g:797:9: ~ ( '\\n' | '\\r' )
                    pass 
                    if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop12
            # sql.g:797:23: ( '\\r' )?
            alt13 = 2
            LA13_0 = self.input.LA(1)

            if (LA13_0 == 13) :
                alt13 = 1
            if alt13 == 1:
                # sql.g:797:23: '\\r'
                pass 
                self.match(13)



            self.match(10)
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

            # sql.g:800:2: ( '/*' ( options {greedy=false; } : . )* '*/' )
            # sql.g:800:4: '/*' ( options {greedy=false; } : . )* '*/'
            pass 
            self.match("/*")
            # sql.g:800:9: ( options {greedy=false; } : . )*
            while True: #loop14
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if (LA14_0 == 42) :
                    LA14_1 = self.input.LA(2)

                    if (LA14_1 == 47) :
                        alt14 = 2
                    elif ((0 <= LA14_1 <= 46) or (48 <= LA14_1 <= 65535)) :
                        alt14 = 1


                elif ((0 <= LA14_0 <= 41) or (43 <= LA14_0 <= 65535)) :
                    alt14 = 1


                if alt14 == 1:
                    # sql.g:800:37: .
                    pass 
                    self.matchAny()


                else:
                    break #loop14
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
        # sql.g:1:8: ( AND | ARRAY | AS | AUTHID | BETWEEN | BODY | BULK | BULK_ROWCOUNT | BY | CASE | CREATE | COLLECT | COMMIT | CURRENT_USER | DEFAULT | DEFINER | DELETE | ELSE | ELSIF | EXTERNAL | FALSE | FETCH | FOR | FORALL | GOTO | IF | IN | INDEX | INSERT | INTO | IS | LANGUAGE | LIKE | LIMIT | LOCK | NOT | NOTFOUND | NULL | OPEN | OR | PACKAGE | RAISE | ROLLBACK | SAVEPOINT | SELECT | SET | SQL | TABLE | TRANSACTION | TRUE | THEN | UPDATE | WHILE | INSERTING | UPDATING | DELETING | ISOPEN | EXISTS | BEGIN | CLOSE | CONSTANT | CONTINUE | CURSOR | DECLARE | DETERMINISTIC | END | EXCEPTION | EXECUTE | EXIT | FUNCTION | IMMEDIATE | LOOP | NOCOPY | OTHERS | OUT | PARALLEL_ENABLE | PIPELINED | PRAGMA | PROCEDURE | RECORD | REF | RESULT_CACHE | RETURN | RETURNING | ROWTYPE | SUBTYPE | USING | VARRAY | VARYING | WHEN | QUOTED_STRING | ID | SEMI | COLON | DOUBLEDOT | DOT | COMMA | EXPONENT | ASTERISK | AT_SIGN | RPAREN | LPAREN | RBRACK | LBRACK | PLUS | MINUS | DIVIDE | EQ | PERCENT | LLABEL | RLABEL | ASSIGN | ARROW | VERTBAR | DOUBLEVERTBAR | NOT_EQ | LTH | LEQ | GTH | GEQ | INTEGER | REAL_NUMBER | WS | SL_COMMENT | ML_COMMENT )
        alt15 = 125
        alt15 = self.dfa15.predict(self.input)
        if alt15 == 1:
            # sql.g:1:10: AND
            pass 
            self.mAND()


        elif alt15 == 2:
            # sql.g:1:14: ARRAY
            pass 
            self.mARRAY()


        elif alt15 == 3:
            # sql.g:1:20: AS
            pass 
            self.mAS()


        elif alt15 == 4:
            # sql.g:1:23: AUTHID
            pass 
            self.mAUTHID()


        elif alt15 == 5:
            # sql.g:1:30: BETWEEN
            pass 
            self.mBETWEEN()


        elif alt15 == 6:
            # sql.g:1:38: BODY
            pass 
            self.mBODY()


        elif alt15 == 7:
            # sql.g:1:43: BULK
            pass 
            self.mBULK()


        elif alt15 == 8:
            # sql.g:1:48: BULK_ROWCOUNT
            pass 
            self.mBULK_ROWCOUNT()


        elif alt15 == 9:
            # sql.g:1:62: BY
            pass 
            self.mBY()


        elif alt15 == 10:
            # sql.g:1:65: CASE
            pass 
            self.mCASE()


        elif alt15 == 11:
            # sql.g:1:70: CREATE
            pass 
            self.mCREATE()


        elif alt15 == 12:
            # sql.g:1:77: COLLECT
            pass 
            self.mCOLLECT()


        elif alt15 == 13:
            # sql.g:1:85: COMMIT
            pass 
            self.mCOMMIT()


        elif alt15 == 14:
            # sql.g:1:92: CURRENT_USER
            pass 
            self.mCURRENT_USER()


        elif alt15 == 15:
            # sql.g:1:105: DEFAULT
            pass 
            self.mDEFAULT()


        elif alt15 == 16:
            # sql.g:1:113: DEFINER
            pass 
            self.mDEFINER()


        elif alt15 == 17:
            # sql.g:1:121: DELETE
            pass 
            self.mDELETE()


        elif alt15 == 18:
            # sql.g:1:128: ELSE
            pass 
            self.mELSE()


        elif alt15 == 19:
            # sql.g:1:133: ELSIF
            pass 
            self.mELSIF()


        elif alt15 == 20:
            # sql.g:1:139: EXTERNAL
            pass 
            self.mEXTERNAL()


        elif alt15 == 21:
            # sql.g:1:148: FALSE
            pass 
            self.mFALSE()


        elif alt15 == 22:
            # sql.g:1:154: FETCH
            pass 
            self.mFETCH()


        elif alt15 == 23:
            # sql.g:1:160: FOR
            pass 
            self.mFOR()


        elif alt15 == 24:
            # sql.g:1:164: FORALL
            pass 
            self.mFORALL()


        elif alt15 == 25:
            # sql.g:1:171: GOTO
            pass 
            self.mGOTO()


        elif alt15 == 26:
            # sql.g:1:176: IF
            pass 
            self.mIF()


        elif alt15 == 27:
            # sql.g:1:179: IN
            pass 
            self.mIN()


        elif alt15 == 28:
            # sql.g:1:182: INDEX
            pass 
            self.mINDEX()


        elif alt15 == 29:
            # sql.g:1:188: INSERT
            pass 
            self.mINSERT()


        elif alt15 == 30:
            # sql.g:1:195: INTO
            pass 
            self.mINTO()


        elif alt15 == 31:
            # sql.g:1:200: IS
            pass 
            self.mIS()


        elif alt15 == 32:
            # sql.g:1:203: LANGUAGE
            pass 
            self.mLANGUAGE()


        elif alt15 == 33:
            # sql.g:1:212: LIKE
            pass 
            self.mLIKE()


        elif alt15 == 34:
            # sql.g:1:217: LIMIT
            pass 
            self.mLIMIT()


        elif alt15 == 35:
            # sql.g:1:223: LOCK
            pass 
            self.mLOCK()


        elif alt15 == 36:
            # sql.g:1:228: NOT
            pass 
            self.mNOT()


        elif alt15 == 37:
            # sql.g:1:232: NOTFOUND
            pass 
            self.mNOTFOUND()


        elif alt15 == 38:
            # sql.g:1:241: NULL
            pass 
            self.mNULL()


        elif alt15 == 39:
            # sql.g:1:246: OPEN
            pass 
            self.mOPEN()


        elif alt15 == 40:
            # sql.g:1:251: OR
            pass 
            self.mOR()


        elif alt15 == 41:
            # sql.g:1:254: PACKAGE
            pass 
            self.mPACKAGE()


        elif alt15 == 42:
            # sql.g:1:262: RAISE
            pass 
            self.mRAISE()


        elif alt15 == 43:
            # sql.g:1:268: ROLLBACK
            pass 
            self.mROLLBACK()


        elif alt15 == 44:
            # sql.g:1:277: SAVEPOINT
            pass 
            self.mSAVEPOINT()


        elif alt15 == 45:
            # sql.g:1:287: SELECT
            pass 
            self.mSELECT()


        elif alt15 == 46:
            # sql.g:1:294: SET
            pass 
            self.mSET()


        elif alt15 == 47:
            # sql.g:1:298: SQL
            pass 
            self.mSQL()


        elif alt15 == 48:
            # sql.g:1:302: TABLE
            pass 
            self.mTABLE()


        elif alt15 == 49:
            # sql.g:1:308: TRANSACTION
            pass 
            self.mTRANSACTION()


        elif alt15 == 50:
            # sql.g:1:320: TRUE
            pass 
            self.mTRUE()


        elif alt15 == 51:
            # sql.g:1:325: THEN
            pass 
            self.mTHEN()


        elif alt15 == 52:
            # sql.g:1:330: UPDATE
            pass 
            self.mUPDATE()


        elif alt15 == 53:
            # sql.g:1:337: WHILE
            pass 
            self.mWHILE()


        elif alt15 == 54:
            # sql.g:1:343: INSERTING
            pass 
            self.mINSERTING()


        elif alt15 == 55:
            # sql.g:1:353: UPDATING
            pass 
            self.mUPDATING()


        elif alt15 == 56:
            # sql.g:1:362: DELETING
            pass 
            self.mDELETING()


        elif alt15 == 57:
            # sql.g:1:371: ISOPEN
            pass 
            self.mISOPEN()


        elif alt15 == 58:
            # sql.g:1:378: EXISTS
            pass 
            self.mEXISTS()


        elif alt15 == 59:
            # sql.g:1:385: BEGIN
            pass 
            self.mBEGIN()


        elif alt15 == 60:
            # sql.g:1:391: CLOSE
            pass 
            self.mCLOSE()


        elif alt15 == 61:
            # sql.g:1:397: CONSTANT
            pass 
            self.mCONSTANT()


        elif alt15 == 62:
            # sql.g:1:406: CONTINUE
            pass 
            self.mCONTINUE()


        elif alt15 == 63:
            # sql.g:1:415: CURSOR
            pass 
            self.mCURSOR()


        elif alt15 == 64:
            # sql.g:1:422: DECLARE
            pass 
            self.mDECLARE()


        elif alt15 == 65:
            # sql.g:1:430: DETERMINISTIC
            pass 
            self.mDETERMINISTIC()


        elif alt15 == 66:
            # sql.g:1:444: END
            pass 
            self.mEND()


        elif alt15 == 67:
            # sql.g:1:448: EXCEPTION
            pass 
            self.mEXCEPTION()


        elif alt15 == 68:
            # sql.g:1:458: EXECUTE
            pass 
            self.mEXECUTE()


        elif alt15 == 69:
            # sql.g:1:466: EXIT
            pass 
            self.mEXIT()


        elif alt15 == 70:
            # sql.g:1:471: FUNCTION
            pass 
            self.mFUNCTION()


        elif alt15 == 71:
            # sql.g:1:480: IMMEDIATE
            pass 
            self.mIMMEDIATE()


        elif alt15 == 72:
            # sql.g:1:490: LOOP
            pass 
            self.mLOOP()


        elif alt15 == 73:
            # sql.g:1:495: NOCOPY
            pass 
            self.mNOCOPY()


        elif alt15 == 74:
            # sql.g:1:502: OTHERS
            pass 
            self.mOTHERS()


        elif alt15 == 75:
            # sql.g:1:509: OUT
            pass 
            self.mOUT()


        elif alt15 == 76:
            # sql.g:1:513: PARALLEL_ENABLE
            pass 
            self.mPARALLEL_ENABLE()


        elif alt15 == 77:
            # sql.g:1:529: PIPELINED
            pass 
            self.mPIPELINED()


        elif alt15 == 78:
            # sql.g:1:539: PRAGMA
            pass 
            self.mPRAGMA()


        elif alt15 == 79:
            # sql.g:1:546: PROCEDURE
            pass 
            self.mPROCEDURE()


        elif alt15 == 80:
            # sql.g:1:556: RECORD
            pass 
            self.mRECORD()


        elif alt15 == 81:
            # sql.g:1:563: REF
            pass 
            self.mREF()


        elif alt15 == 82:
            # sql.g:1:567: RESULT_CACHE
            pass 
            self.mRESULT_CACHE()


        elif alt15 == 83:
            # sql.g:1:580: RETURN
            pass 
            self.mRETURN()


        elif alt15 == 84:
            # sql.g:1:587: RETURNING
            pass 
            self.mRETURNING()


        elif alt15 == 85:
            # sql.g:1:597: ROWTYPE
            pass 
            self.mROWTYPE()


        elif alt15 == 86:
            # sql.g:1:605: SUBTYPE
            pass 
            self.mSUBTYPE()


        elif alt15 == 87:
            # sql.g:1:613: USING
            pass 
            self.mUSING()


        elif alt15 == 88:
            # sql.g:1:619: VARRAY
            pass 
            self.mVARRAY()


        elif alt15 == 89:
            # sql.g:1:626: VARYING
            pass 
            self.mVARYING()


        elif alt15 == 90:
            # sql.g:1:634: WHEN
            pass 
            self.mWHEN()


        elif alt15 == 91:
            # sql.g:1:639: QUOTED_STRING
            pass 
            self.mQUOTED_STRING()


        elif alt15 == 92:
            # sql.g:1:653: ID
            pass 
            self.mID()


        elif alt15 == 93:
            # sql.g:1:656: SEMI
            pass 
            self.mSEMI()


        elif alt15 == 94:
            # sql.g:1:661: COLON
            pass 
            self.mCOLON()


        elif alt15 == 95:
            # sql.g:1:667: DOUBLEDOT
            pass 
            self.mDOUBLEDOT()


        elif alt15 == 96:
            # sql.g:1:677: DOT
            pass 
            self.mDOT()


        elif alt15 == 97:
            # sql.g:1:681: COMMA
            pass 
            self.mCOMMA()


        elif alt15 == 98:
            # sql.g:1:687: EXPONENT
            pass 
            self.mEXPONENT()


        elif alt15 == 99:
            # sql.g:1:696: ASTERISK
            pass 
            self.mASTERISK()


        elif alt15 == 100:
            # sql.g:1:705: AT_SIGN
            pass 
            self.mAT_SIGN()


        elif alt15 == 101:
            # sql.g:1:713: RPAREN
            pass 
            self.mRPAREN()


        elif alt15 == 102:
            # sql.g:1:720: LPAREN
            pass 
            self.mLPAREN()


        elif alt15 == 103:
            # sql.g:1:727: RBRACK
            pass 
            self.mRBRACK()


        elif alt15 == 104:
            # sql.g:1:734: LBRACK
            pass 
            self.mLBRACK()


        elif alt15 == 105:
            # sql.g:1:741: PLUS
            pass 
            self.mPLUS()


        elif alt15 == 106:
            # sql.g:1:746: MINUS
            pass 
            self.mMINUS()


        elif alt15 == 107:
            # sql.g:1:752: DIVIDE
            pass 
            self.mDIVIDE()


        elif alt15 == 108:
            # sql.g:1:759: EQ
            pass 
            self.mEQ()


        elif alt15 == 109:
            # sql.g:1:762: PERCENT
            pass 
            self.mPERCENT()


        elif alt15 == 110:
            # sql.g:1:770: LLABEL
            pass 
            self.mLLABEL()


        elif alt15 == 111:
            # sql.g:1:777: RLABEL
            pass 
            self.mRLABEL()


        elif alt15 == 112:
            # sql.g:1:784: ASSIGN
            pass 
            self.mASSIGN()


        elif alt15 == 113:
            # sql.g:1:791: ARROW
            pass 
            self.mARROW()


        elif alt15 == 114:
            # sql.g:1:797: VERTBAR
            pass 
            self.mVERTBAR()


        elif alt15 == 115:
            # sql.g:1:805: DOUBLEVERTBAR
            pass 
            self.mDOUBLEVERTBAR()


        elif alt15 == 116:
            # sql.g:1:819: NOT_EQ
            pass 
            self.mNOT_EQ()


        elif alt15 == 117:
            # sql.g:1:826: LTH
            pass 
            self.mLTH()


        elif alt15 == 118:
            # sql.g:1:830: LEQ
            pass 
            self.mLEQ()


        elif alt15 == 119:
            # sql.g:1:834: GTH
            pass 
            self.mGTH()


        elif alt15 == 120:
            # sql.g:1:838: GEQ
            pass 
            self.mGEQ()


        elif alt15 == 121:
            # sql.g:1:842: INTEGER
            pass 
            self.mINTEGER()


        elif alt15 == 122:
            # sql.g:1:850: REAL_NUMBER
            pass 
            self.mREAL_NUMBER()


        elif alt15 == 123:
            # sql.g:1:862: WS
            pass 
            self.mWS()


        elif alt15 == 124:
            # sql.g:1:865: SL_COMMENT
            pass 
            self.mSL_COMMENT()


        elif alt15 == 125:
            # sql.g:1:876: ML_COMMENT
            pass 
            self.mML_COMMENT()







    # lookup tables for DFA #9

    DFA9_eot = DFA.unpack(
        "\1\uffff\1\4\1\uffff\1\4\2\uffff"
        )

    DFA9_eof = DFA.unpack(
        "\6\uffff"
        )

    DFA9_min = DFA.unpack(
        "\2\56\1\uffff\1\56\2\uffff"
        )

    DFA9_max = DFA.unpack(
        "\2\71\1\uffff\1\71\2\uffff"
        )

    DFA9_accept = DFA.unpack(
        "\2\uffff\1\2\1\uffff\1\3\1\1"
        )

    DFA9_special = DFA.unpack(
        "\1\uffff\1\1\1\uffff\1\0\2\uffff"
        )

            
    DFA9_transition = [
        DFA.unpack("\1\2\1\uffff\12\1"),
        DFA.unpack("\1\5\1\uffff\12\3"),
        DFA.unpack(""),
        DFA.unpack("\1\5\1\uffff\12\3"),
        DFA.unpack(""),
        DFA.unpack("")
    ]

    # class definition for DFA #9

    class DFA9(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA9_3 = input.LA(1)

                 
                index9_3 = input.index()
                input.rewind()
                s = -1
                if (LA9_3 == 46) and ((self.numberDotValid())):
                    s = 5

                elif ((48 <= LA9_3 <= 57)):
                    s = 3

                else:
                    s = 4

                 
                input.seek(index9_3)
                if s >= 0:
                    return s
            elif s == 1: 
                LA9_1 = input.LA(1)

                 
                index9_1 = input.index()
                input.rewind()
                s = -1
                if ((48 <= LA9_1 <= 57)):
                    s = 3

                elif (LA9_1 == 46) and ((self.numberDotValid())):
                    s = 5

                else:
                    s = 4

                 
                input.seek(index9_1)
                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 9, _s, input)
            self_.error(nvae)
            raise nvae
    # lookup tables for DFA #15

    DFA15_eot = DFA.unpack(
        "\1\uffff\22\24\3\uffff\1\137\1\140\1\uffff\1\144\6\uffff\1\146"
        "\1\150\1\152\1\uffff\1\155\1\160\1\162\1\uffff\1\164\1\uffff\2"
        "\24\1\171\4\24\1\177\16\24\1\u0096\1\u009a\1\u009c\7\24\1\u00a7"
        "\23\24\25\uffff\1\164\3\uffff\1\u00c4\1\24\1\uffff\5\24\1\uffff"
        "\20\24\1\u00e0\2\24\1\u00e4\2\24\1\uffff\3\24\1\uffff\1\24\1\uffff"
        "\6\24\1\u00f2\3\24\1\uffff\1\24\1\u00f7\11\24\1\u0101\4\24\1\u0106"
        "\1\u0107\12\24\1\uffff\4\24\1\u0117\1\u0119\1\u011a\15\24\1\u0128"
        "\3\24\1\u012c\2\24\1\uffff\3\24\1\uffff\1\24\1\u0133\2\24\1\u0136"
        "\3\24\1\u013a\1\24\1\u013c\1\u013d\1\24\1\uffff\1\24\1\u0140\1"
        "\u0141\1\24\1\uffff\11\24\1\uffff\4\24\2\uffff\3\24\1\u0153\1\u0154"
        "\3\24\1\u0158\2\24\1\u015b\2\24\1\u015e\1\uffff\1\24\2\uffff\7"
        "\24\1\u0167\5\24\1\uffff\1\u016e\2\24\1\uffff\2\24\1\u0173\1\u0174"
        "\2\24\1\uffff\1\u0177\1\24\1\uffff\3\24\1\uffff\1\u017c\2\uffff"
        "\2\24\2\uffff\6\24\1\u0185\10\24\1\u018e\1\24\2\uffff\1\24\1\u0192"
        "\1\u0193\1\uffff\2\24\1\uffff\1\u0196\1\24\1\uffff\1\24\1\u0199"
        "\1\24\1\u019b\3\24\1\u019f\1\uffff\2\24\1\u01a2\3\24\1\uffff\1"
        "\24\1\u01a7\2\24\2\uffff\1\u01aa\1\24\1\uffff\1\u01ad\1\u01ae\2"
        "\24\1\uffff\1\24\1\u01b2\1\u01b3\3\24\1\u01b7\1\24\1\uffff\2\24"
        "\1\u01bb\1\24\1\u01be\1\24\1\u01c0\1\24\1\uffff\1\24\1\u01c3\1"
        "\24\2\uffff\1\u01c5\1\24\1\uffff\1\u01c7\1\24\1\uffff\1\u01c9\1"
        "\uffff\3\24\1\uffff\1\u01cd\1\u01ce\1\uffff\1\24\1\u01d0\2\24\1"
        "\uffff\1\24\1\u01d4\1\uffff\2\24\2\uffff\3\24\2\uffff\1\u01da\2"
        "\24\1\uffff\2\24\1\u01df\1\uffff\2\24\1\uffff\1\24\1\uffff\1\u01e3"
        "\1\24\1\uffff\1\24\1\uffff\1\u01e6\1\uffff\1\24\1\uffff\1\u01e8"
        "\1\u01e9\1\24\2\uffff\1\u01eb\1\uffff\1\24\1\u01ed\1\24\1\uffff"
        "\1\u01ef\2\24\1\u01f2\1\u01f3\1\uffff\3\24\1\u01f7\1\uffff\3\24"
        "\1\uffff\1\24\1\u01fc\1\uffff\1\24\2\uffff\1\24\1\uffff\1\24\1"
        "\uffff\1\u0200\1\uffff\1\u0201\1\u0202\2\uffff\1\24\1\u0204\1\u0205"
        "\1\uffff\1\24\1\u0207\1\u0208\1\24\1\uffff\3\24\3\uffff\1\24\2"
        "\uffff\1\24\2\uffff\6\24\1\u0215\1\24\1\u0217\2\24\1\u021a\1\uffff"
        "\1\u021b\1\uffff\1\u021c\1\24\3\uffff\1\24\1\u021f\1\uffff"
        )

    DFA15_eof = DFA.unpack(
        "\u0220\uffff"
        )

    DFA15_min = DFA.unpack(
        "\1\11\1\156\1\145\1\141\1\145\1\154\1\141\1\157\1\146\1\141\1\47"
        "\1\160\4\141\1\160\1\150\1\141\3\uffff\1\75\1\56\1\uffff\1\52\6"
        "\uffff\1\55\1\52\1\76\1\uffff\1\74\1\75\1\174\1\uffff\1\56\1\uffff"
        "\1\144\1\162\1\43\1\164\1\147\1\144\1\154\1\43\1\163\1\145\1\154"
        "\1\162\1\157\1\143\1\163\1\143\1\144\1\154\1\164\1\162\1\156\1"
        "\164\3\43\1\155\1\156\1\153\2\143\1\154\1\145\1\43\1\150\1\164"
        "\1\143\1\160\1\141\1\151\1\154\1\143\1\166\2\154\2\142\1\141\1"
        "\145\1\144\1\151\1\145\1\162\25\uffff\1\56\3\uffff\1\43\1\141\1"
        "\uffff\1\150\1\167\1\151\1\171\1\153\1\uffff\1\145\1\141\1\154"
        "\1\155\1\163\1\162\1\163\1\141\1\145\1\154\3\145\1\163\1\145\1"
        "\143\1\43\1\163\1\143\1\43\1\143\1\157\1\uffff\2\145\1\157\1\uffff"
        "\1\160\1\uffff\1\145\1\147\1\145\1\151\1\153\1\160\1\43\1\157\1"
        "\154\1\156\1\uffff\1\145\1\43\1\153\1\141\1\145\1\147\1\143\1\163"
        "\1\154\1\164\1\157\1\43\2\165\2\145\2\43\1\164\1\154\1\156\1\145"
        "\1\156\1\141\1\156\1\154\1\156\1\162\1\uffff\1\171\1\151\1\145"
        "\1\156\3\43\1\164\1\145\1\151\1\164\1\151\1\145\1\157\1\145\1\165"
        "\1\156\1\164\1\141\1\162\1\43\1\146\1\162\1\164\1\43\1\160\1\165"
        "\1\uffff\1\145\1\150\1\154\1\uffff\1\164\1\43\1\170\1\162\1\43"
        "\1\145\1\144\1\165\1\43\1\164\2\43\1\157\1\uffff\1\160\2\43\1\162"
        "\1\uffff\1\141\2\154\1\155\2\145\1\142\1\171\1\162\1\uffff\1\154"
        "\1\162\1\160\1\143\2\uffff\1\171\1\145\1\163\2\43\1\164\1\147\1"
        "\145\1\43\1\141\1\151\1\43\1\144\1\145\1\43\1\uffff\1\162\2\uffff"
        "\1\145\1\143\1\164\1\141\2\156\1\162\1\43\1\154\2\145\1\162\1\155"
        "\1\uffff\1\43\1\156\1\163\1\uffff\2\164\2\43\1\154\1\151\1\uffff"
        "\1\43\1\164\1\uffff\1\156\1\151\1\141\1\uffff\1\43\2\uffff\1\165"
        "\1\171\2\uffff\1\163\1\147\1\154\1\151\1\141\1\144\1\43\1\141\1"
        "\160\1\144\1\164\1\156\1\157\1\164\1\160\1\43\1\141\2\uffff\1\145"
        "\2\43\1\uffff\1\171\1\156\1\uffff\1\43\1\156\1\uffff\1\157\1\43"
        "\1\164\1\43\1\156\1\165\1\164\1\43\1\uffff\1\164\1\162\1\43\1\156"
        "\1\145\1\151\1\uffff\1\141\1\43\1\151\1\145\2\uffff\1\43\1\157"
        "\1\uffff\2\43\1\141\1\147\1\uffff\1\156\2\43\2\145\1\156\1\43\1"
        "\165\1\uffff\1\143\1\145\1\43\1\137\1\43\1\151\1\43\1\145\1\uffff"
        "\1\143\1\43\1\156\2\uffff\1\43\1\147\1\uffff\1\43\1\167\1\uffff"
        "\1\43\1\uffff\1\164\1\145\1\137\1\uffff\2\43\1\uffff\1\147\1\43"
        "\1\156\1\154\1\uffff\1\157\1\43\1\uffff\2\156\2\uffff\1\164\1\145"
        "\1\144\2\uffff\1\43\1\154\1\145\1\uffff\1\162\1\153\1\43\1\uffff"
        "\1\143\1\156\1\uffff\1\156\1\uffff\1\43\1\164\1\uffff\1\147\1\uffff"
        "\1\43\1\uffff\1\143\1\uffff\2\43\1\165\2\uffff\1\43\1\uffff\1\151"
        "\1\43\1\156\1\uffff\1\43\1\147\1\145\2\43\1\uffff\1\137\1\144\1"
        "\145\1\43\1\uffff\1\141\1\147\1\164\1\uffff\1\151\1\43\1\uffff"
        "\1\157\2\uffff\1\163\1\uffff\1\163\1\uffff\1\43\1\uffff\2\43\2"
        "\uffff\1\145\2\43\1\uffff\1\143\2\43\1\157\1\uffff\1\165\1\145"
        "\1\164\3\uffff\1\156\2\uffff\1\150\2\uffff\2\156\1\162\1\151\1"
        "\141\1\145\1\43\1\164\1\43\1\143\1\142\1\43\1\uffff\1\43\1\uffff"
        "\1\43\1\154\3\uffff\1\145\1\43\1\uffff"
        )

    DFA15_max = DFA.unpack(
        "\1\176\1\165\1\171\1\165\1\145\1\170\1\165\1\157\1\163\1\157\2"
        "\165\1\162\1\157\1\165\1\162\1\163\1\150\1\141\3\uffff\1\75\1\71"
        "\1\uffff\1\52\6\uffff\1\55\1\52\1\76\1\uffff\2\76\1\174\1\uffff"
        "\1\145\1\uffff\1\144\1\162\1\172\2\164\1\144\1\154\1\172\1\163"
        "\1\145\1\156\1\162\1\157\1\164\1\163\1\164\1\144\1\154\1\164\1"
        "\162\1\156\1\164\3\172\1\155\1\156\1\155\1\157\1\164\1\154\1\145"
        "\1\172\1\150\1\164\1\162\1\160\1\157\1\151\1\167\1\164\1\166\1"
        "\164\1\154\2\142\1\165\1\145\1\144\2\151\1\162\25\uffff\1\145\3"
        "\uffff\1\172\1\141\1\uffff\1\150\1\167\1\151\1\171\1\153\1\uffff"
        "\1\145\1\141\1\154\1\155\1\164\2\163\1\151\1\145\1\154\1\145\1"
        "\151\1\145\1\164\1\145\1\143\1\172\1\163\1\143\1\172\1\143\1\157"
        "\1\uffff\2\145\1\157\1\uffff\1\160\1\uffff\1\145\1\147\1\145\1"
        "\151\1\153\1\160\1\172\1\157\1\154\1\156\1\uffff\1\145\1\172\1"
        "\153\1\141\1\145\1\147\1\143\1\163\1\154\1\164\1\157\1\172\2\165"
        "\2\145\2\172\1\164\1\154\1\156\1\145\1\156\1\141\1\156\1\154\1"
        "\156\1\171\1\uffff\1\171\1\151\1\145\1\156\3\172\1\164\1\145\1"
        "\151\1\164\1\151\1\145\1\157\1\145\1\165\1\156\1\164\1\141\1\162"
        "\1\172\1\146\1\162\1\164\1\172\1\160\1\165\1\uffff\1\145\1\150"
        "\1\154\1\uffff\1\164\1\172\1\170\1\162\1\172\1\145\1\144\1\165"
        "\1\172\1\164\2\172\1\157\1\uffff\1\160\2\172\1\162\1\uffff\1\141"
        "\2\154\1\155\2\145\1\142\1\171\1\162\1\uffff\1\154\1\162\1\160"
        "\1\143\2\uffff\1\171\1\145\1\163\2\172\1\164\1\147\1\145\1\172"
        "\1\141\1\151\1\172\1\144\1\145\1\172\1\uffff\1\162\2\uffff\1\145"
        "\1\143\1\164\1\141\2\156\1\162\1\172\1\154\1\145\1\151\1\162\1"
        "\155\1\uffff\1\172\1\156\1\163\1\uffff\2\164\2\172\1\154\1\151"
        "\1\uffff\1\172\1\164\1\uffff\1\156\1\151\1\141\1\uffff\1\172\2"
        "\uffff\1\165\1\171\2\uffff\1\163\1\147\1\154\1\151\1\141\1\144"
        "\1\172\1\141\1\160\1\144\1\164\1\156\1\157\1\164\1\160\1\172\1"
        "\141\2\uffff\1\151\2\172\1\uffff\1\171\1\156\1\uffff\1\172\1\156"
        "\1\uffff\1\157\1\172\1\164\1\172\1\156\1\165\1\164\1\172\1\uffff"
        "\1\164\1\162\1\172\1\156\1\145\1\151\1\uffff\1\141\1\172\1\151"
        "\1\145\2\uffff\1\172\1\157\1\uffff\2\172\1\141\1\147\1\uffff\1"
        "\156\2\172\2\145\1\156\1\172\1\165\1\uffff\1\143\1\145\1\172\1"
        "\137\1\172\1\151\1\172\1\145\1\uffff\1\143\1\172\1\156\2\uffff"
        "\1\172\1\147\1\uffff\1\172\1\167\1\uffff\1\172\1\uffff\1\164\1"
        "\145\1\137\1\uffff\2\172\1\uffff\1\147\1\172\1\156\1\154\1\uffff"
        "\1\157\1\172\1\uffff\2\156\2\uffff\1\164\1\145\1\144\2\uffff\1"
        "\172\1\154\1\145\1\uffff\1\162\1\153\1\172\1\uffff\1\143\1\156"
        "\1\uffff\1\156\1\uffff\1\172\1\164\1\uffff\1\147\1\uffff\1\172"
        "\1\uffff\1\143\1\uffff\2\172\1\165\2\uffff\1\172\1\uffff\1\151"
        "\1\172\1\156\1\uffff\1\172\1\147\1\145\2\172\1\uffff\1\137\1\144"
        "\1\145\1\172\1\uffff\1\141\1\147\1\164\1\uffff\1\151\1\172\1\uffff"
        "\1\157\2\uffff\1\163\1\uffff\1\163\1\uffff\1\172\1\uffff\2\172"
        "\2\uffff\1\145\2\172\1\uffff\1\143\2\172\1\157\1\uffff\1\165\1"
        "\145\1\164\3\uffff\1\156\2\uffff\1\150\2\uffff\2\156\1\162\1\151"
        "\1\141\1\145\1\172\1\164\1\172\1\143\1\142\1\172\1\uffff\1\172"
        "\1\uffff\1\172\1\154\3\uffff\1\145\1\172\1\uffff"
        )

    DFA15_accept = DFA.unpack(
        "\23\uffff\1\133\1\134\1\135\2\uffff\1\141\1\uffff\1\144\1\145\1"
        "\146\1\147\1\150\1\151\3\uffff\1\155\3\uffff\1\164\1\uffff\1\173"
        "\64\uffff\1\160\1\136\1\140\1\137\1\172\1\142\1\143\1\174\1\152"
        "\1\175\1\153\1\161\1\154\1\156\1\166\1\165\1\157\1\170\1\167\1"
        "\163\1\162\1\uffff\1\171\2\172\2\uffff\1\3\5\uffff\1\11\26\uffff"
        "\1\32\3\uffff\1\33\1\uffff\1\37\12\uffff\1\50\34\uffff\1\1\33\uffff"
        "\1\102\3\uffff\1\27\15\uffff\1\44\4\uffff\1\113\11\uffff\1\121"
        "\4\uffff\1\56\1\57\17\uffff\1\6\1\uffff\1\7\1\12\15\uffff\1\22"
        "\3\uffff\1\105\6\uffff\1\31\2\uffff\1\36\3\uffff\1\41\1\uffff\1"
        "\43\1\110\2\uffff\1\46\1\47\21\uffff\1\62\1\63\3\uffff\1\132\2"
        "\uffff\1\2\2\uffff\1\73\10\uffff\1\74\6\uffff\1\23\4\uffff\1\25"
        "\1\26\2\uffff\1\34\4\uffff\1\42\10\uffff\1\52\10\uffff\1\60\3\uffff"
        "\1\127\1\65\2\uffff\1\4\2\uffff\1\13\1\uffff\1\15\3\uffff\1\77"
        "\2\uffff\1\21\4\uffff\1\72\2\uffff\1\30\2\uffff\1\35\1\71\3\uffff"
        "\1\111\1\112\3\uffff\1\116\3\uffff\1\120\2\uffff\1\123\1\uffff"
        "\1\55\2\uffff\1\64\1\uffff\1\130\1\uffff\1\5\1\uffff\1\14\3\uffff"
        "\1\17\1\20\1\uffff\1\100\3\uffff\1\104\5\uffff\1\51\4\uffff\1\125"
        "\3\uffff\1\126\2\uffff\1\131\1\uffff\1\75\1\76\1\uffff\1\70\1\uffff"
        "\1\24\1\uffff\1\106\2\uffff\1\40\1\45\3\uffff\1\53\4\uffff\1\67"
        "\3\uffff\1\103\1\66\1\107\1\uffff\1\115\1\117\1\uffff\1\124\1\54"
        "\14\uffff\1\61\1\uffff\1\16\2\uffff\1\122\1\10\1\101\2\uffff\1"
        "\114"
        )

    DFA15_special = DFA.unpack(
        "\50\uffff\1\0\112\uffff\1\1\u01ac\uffff"
        )

            
    DFA15_transition = [
        DFA.unpack("\2\51\2\uffff\1\51\22\uffff\1\51\1\47\1\24\2\uffff\1"
        "\43\1\uffff\1\23\1\34\1\33\1\31\1\37\1\30\1\40\1\27\1\41\12\50"
        "\1\26\1\25\1\44\1\42\1\45\1\uffff\1\32\32\uffff\1\36\1\uffff\1"
        "\35\1\47\2\uffff\1\1\1\2\1\3\1\4\1\5\1\6\1\7\1\24\1\10\2\24\1\11"
        "\1\24\1\12\1\13\1\14\1\24\1\15\1\16\1\17\1\20\1\22\1\21\3\24\1"
        "\uffff\1\46\1\uffff\1\47"),
        DFA.unpack("\1\52\3\uffff\1\53\1\54\1\uffff\1\55"),
        DFA.unpack("\1\56\11\uffff\1\57\5\uffff\1\60\3\uffff\1\61"),
        DFA.unpack("\1\62\12\uffff\1\66\2\uffff\1\64\2\uffff\1\63\2\uffff"
        "\1\65"),
        DFA.unpack("\1\67"),
        DFA.unpack("\1\70\1\uffff\1\72\11\uffff\1\71"),
        DFA.unpack("\1\73\3\uffff\1\74\11\uffff\1\75\5\uffff\1\76"),
        DFA.unpack("\1\77"),
        DFA.unpack("\1\100\6\uffff\1\103\1\101\4\uffff\1\102"),
        DFA.unpack("\1\104\7\uffff\1\105\5\uffff\1\106"),
        DFA.unpack("\1\23\107\uffff\1\107\5\uffff\1\110"),
        DFA.unpack("\1\111\1\uffff\1\112\1\uffff\1\113\1\114"),
        DFA.unpack("\1\115\7\uffff\1\116\10\uffff\1\117"),
        DFA.unpack("\1\120\3\uffff\1\122\11\uffff\1\121"),
        DFA.unpack("\1\123\3\uffff\1\124\13\uffff\1\125\3\uffff\1\126"),
        DFA.unpack("\1\127\6\uffff\1\131\11\uffff\1\130"),
        DFA.unpack("\1\132\2\uffff\1\133"),
        DFA.unpack("\1\134"),
        DFA.unpack("\1\135"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\136"),
        DFA.unpack("\1\141\1\uffff\12\142"),
        DFA.unpack(""),
        DFA.unpack("\1\143"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\145"),
        DFA.unpack("\1\147"),
        DFA.unpack("\1\151"),
        DFA.unpack(""),
        DFA.unpack("\1\153\1\154\1\47"),
        DFA.unpack("\1\157\1\156"),
        DFA.unpack("\1\161"),
        DFA.unpack(""),
        DFA.unpack("\1\165\1\uffff\12\163\53\uffff\1\166"),
        DFA.unpack(""),
        DFA.unpack("\1\167"),
        DFA.unpack("\1\170"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\172"),
        DFA.unpack("\1\174\14\uffff\1\173"),
        DFA.unpack("\1\175"),
        DFA.unpack("\1\176"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0080"),
        DFA.unpack("\1\u0081"),
        DFA.unpack("\1\u0082\1\u0083\1\u0084"),
        DFA.unpack("\1\u0085"),
        DFA.unpack("\1\u0086"),
        DFA.unpack("\1\u0089\2\uffff\1\u0087\5\uffff\1\u0088\7\uffff\1"
        "\u008a"),
        DFA.unpack("\1\u008b"),
        DFA.unpack("\1\u008e\1\uffff\1\u008f\3\uffff\1\u008d\12\uffff\1"
        "\u008c"),
        DFA.unpack("\1\u0090"),
        DFA.unpack("\1\u0091"),
        DFA.unpack("\1\u0092"),
        DFA.unpack("\1\u0093"),
        DFA.unpack("\1\u0094"),
        DFA.unpack("\1\u0095"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\3\24\1\u0097"
        "\16\24\1\u0098\1\u0099\6\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\16\24\1"
        "\u009b\13\24"),
        DFA.unpack("\1\u009d"),
        DFA.unpack("\1\u009e"),
        DFA.unpack("\1\u009f\1\uffff\1\u00a0"),
        DFA.unpack("\1\u00a1\13\uffff\1\u00a2"),
        DFA.unpack("\1\u00a4\20\uffff\1\u00a3"),
        DFA.unpack("\1\u00a5"),
        DFA.unpack("\1\u00a6"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u00a8"),
        DFA.unpack("\1\u00a9"),
        DFA.unpack("\1\u00aa\16\uffff\1\u00ab"),
        DFA.unpack("\1\u00ac"),
        DFA.unpack("\1\u00ad\15\uffff\1\u00ae"),
        DFA.unpack("\1\u00af"),
        DFA.unpack("\1\u00b0\12\uffff\1\u00b1"),
        DFA.unpack("\1\u00b2\2\uffff\1\u00b3\14\uffff\1\u00b4\1\u00b5"),
        DFA.unpack("\1\u00b6"),
        DFA.unpack("\1\u00b7\7\uffff\1\u00b8"),
        DFA.unpack("\1\u00b9"),
        DFA.unpack("\1\u00ba"),
        DFA.unpack("\1\u00bb"),
        DFA.unpack("\1\u00bc\23\uffff\1\u00bd"),
        DFA.unpack("\1\u00be"),
        DFA.unpack("\1\u00bf"),
        DFA.unpack("\1\u00c0"),
        DFA.unpack("\1\u00c2\3\uffff\1\u00c1"),
        DFA.unpack("\1\u00c3"),
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
        DFA.unpack(""),
        DFA.unpack("\1\165\1\uffff\12\163\53\uffff\1\166"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u00c5"),
        DFA.unpack(""),
        DFA.unpack("\1\u00c6"),
        DFA.unpack("\1\u00c7"),
        DFA.unpack("\1\u00c8"),
        DFA.unpack("\1\u00c9"),
        DFA.unpack("\1\u00ca"),
        DFA.unpack(""),
        DFA.unpack("\1\u00cb"),
        DFA.unpack("\1\u00cc"),
        DFA.unpack("\1\u00cd"),
        DFA.unpack("\1\u00ce"),
        DFA.unpack("\1\u00cf\1\u00d0"),
        DFA.unpack("\1\u00d1\1\u00d2"),
        DFA.unpack("\1\u00d3"),
        DFA.unpack("\1\u00d4\7\uffff\1\u00d5"),
        DFA.unpack("\1\u00d6"),
        DFA.unpack("\1\u00d7"),
        DFA.unpack("\1\u00d8"),
        DFA.unpack("\1\u00d9\3\uffff\1\u00da"),
        DFA.unpack("\1\u00db"),
        DFA.unpack("\1\u00dc\1\u00dd"),
        DFA.unpack("\1\u00de"),
        DFA.unpack("\1\u00df"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u00e1"),
        DFA.unpack("\1\u00e2"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\1\u00e3"
        "\31\24"),
        DFA.unpack("\1\u00e5"),
        DFA.unpack("\1\u00e6"),
        DFA.unpack(""),
        DFA.unpack("\1\u00e7"),
        DFA.unpack("\1\u00e8"),
        DFA.unpack("\1\u00e9"),
        DFA.unpack(""),
        DFA.unpack("\1\u00ea"),
        DFA.unpack(""),
        DFA.unpack("\1\u00eb"),
        DFA.unpack("\1\u00ec"),
        DFA.unpack("\1\u00ed"),
        DFA.unpack("\1\u00ee"),
        DFA.unpack("\1\u00ef"),
        DFA.unpack("\1\u00f0"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\5\24\1\u00f1"
        "\24\24"),
        DFA.unpack("\1\u00f3"),
        DFA.unpack("\1\u00f4"),
        DFA.unpack("\1\u00f5"),
        DFA.unpack(""),
        DFA.unpack("\1\u00f6"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u00f8"),
        DFA.unpack("\1\u00f9"),
        DFA.unpack("\1\u00fa"),
        DFA.unpack("\1\u00fb"),
        DFA.unpack("\1\u00fc"),
        DFA.unpack("\1\u00fd"),
        DFA.unpack("\1\u00fe"),
        DFA.unpack("\1\u00ff"),
        DFA.unpack("\1\u0100"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0102"),
        DFA.unpack("\1\u0103"),
        DFA.unpack("\1\u0104"),
        DFA.unpack("\1\u0105"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0108"),
        DFA.unpack("\1\u0109"),
        DFA.unpack("\1\u010a"),
        DFA.unpack("\1\u010b"),
        DFA.unpack("\1\u010c"),
        DFA.unpack("\1\u010d"),
        DFA.unpack("\1\u010e"),
        DFA.unpack("\1\u010f"),
        DFA.unpack("\1\u0110"),
        DFA.unpack("\1\u0111\6\uffff\1\u0112"),
        DFA.unpack(""),
        DFA.unpack("\1\u0113"),
        DFA.unpack("\1\u0114"),
        DFA.unpack("\1\u0115"),
        DFA.unpack("\1\u0116"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\u0118\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u011b"),
        DFA.unpack("\1\u011c"),
        DFA.unpack("\1\u011d"),
        DFA.unpack("\1\u011e"),
        DFA.unpack("\1\u011f"),
        DFA.unpack("\1\u0120"),
        DFA.unpack("\1\u0121"),
        DFA.unpack("\1\u0122"),
        DFA.unpack("\1\u0123"),
        DFA.unpack("\1\u0124"),
        DFA.unpack("\1\u0125"),
        DFA.unpack("\1\u0126"),
        DFA.unpack("\1\u0127"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0129"),
        DFA.unpack("\1\u012a"),
        DFA.unpack("\1\u012b"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u012d"),
        DFA.unpack("\1\u012e"),
        DFA.unpack(""),
        DFA.unpack("\1\u012f"),
        DFA.unpack("\1\u0130"),
        DFA.unpack("\1\u0131"),
        DFA.unpack(""),
        DFA.unpack("\1\u0132"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0134"),
        DFA.unpack("\1\u0135"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0137"),
        DFA.unpack("\1\u0138"),
        DFA.unpack("\1\u0139"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u013b"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u013e"),
        DFA.unpack(""),
        DFA.unpack("\1\u013f"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0142"),
        DFA.unpack(""),
        DFA.unpack("\1\u0143"),
        DFA.unpack("\1\u0144"),
        DFA.unpack("\1\u0145"),
        DFA.unpack("\1\u0146"),
        DFA.unpack("\1\u0147"),
        DFA.unpack("\1\u0148"),
        DFA.unpack("\1\u0149"),
        DFA.unpack("\1\u014a"),
        DFA.unpack("\1\u014b"),
        DFA.unpack(""),
        DFA.unpack("\1\u014c"),
        DFA.unpack("\1\u014d"),
        DFA.unpack("\1\u014e"),
        DFA.unpack("\1\u014f"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u0150"),
        DFA.unpack("\1\u0151"),
        DFA.unpack("\1\u0152"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0155"),
        DFA.unpack("\1\u0156"),
        DFA.unpack("\1\u0157"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0159"),
        DFA.unpack("\1\u015a"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u015c"),
        DFA.unpack("\1\u015d"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u015f"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u0160"),
        DFA.unpack("\1\u0161"),
        DFA.unpack("\1\u0162"),
        DFA.unpack("\1\u0163"),
        DFA.unpack("\1\u0164"),
        DFA.unpack("\1\u0165"),
        DFA.unpack("\1\u0166"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0168"),
        DFA.unpack("\1\u0169"),
        DFA.unpack("\1\u016a\3\uffff\1\u016b"),
        DFA.unpack("\1\u016c"),
        DFA.unpack("\1\u016d"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u016f"),
        DFA.unpack("\1\u0170"),
        DFA.unpack(""),
        DFA.unpack("\1\u0171"),
        DFA.unpack("\1\u0172"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0175"),
        DFA.unpack("\1\u0176"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0178"),
        DFA.unpack(""),
        DFA.unpack("\1\u0179"),
        DFA.unpack("\1\u017a"),
        DFA.unpack("\1\u017b"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u017d"),
        DFA.unpack("\1\u017e"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u017f"),
        DFA.unpack("\1\u0180"),
        DFA.unpack("\1\u0181"),
        DFA.unpack("\1\u0182"),
        DFA.unpack("\1\u0183"),
        DFA.unpack("\1\u0184"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0186"),
        DFA.unpack("\1\u0187"),
        DFA.unpack("\1\u0188"),
        DFA.unpack("\1\u0189"),
        DFA.unpack("\1\u018a"),
        DFA.unpack("\1\u018b"),
        DFA.unpack("\1\u018c"),
        DFA.unpack("\1\u018d"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u018f"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u0190\3\uffff\1\u0191"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u0194"),
        DFA.unpack("\1\u0195"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0197"),
        DFA.unpack(""),
        DFA.unpack("\1\u0198"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u019a"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u019c"),
        DFA.unpack("\1\u019d"),
        DFA.unpack("\1\u019e"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01a0"),
        DFA.unpack("\1\u01a1"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01a3"),
        DFA.unpack("\1\u01a4"),
        DFA.unpack("\1\u01a5"),
        DFA.unpack(""),
        DFA.unpack("\1\u01a6"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01a8"),
        DFA.unpack("\1\u01a9"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01ab"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\10\24\1"
        "\u01ac\21\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01af"),
        DFA.unpack("\1\u01b0"),
        DFA.unpack(""),
        DFA.unpack("\1\u01b1"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01b4"),
        DFA.unpack("\1\u01b5"),
        DFA.unpack("\1\u01b6"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01b8"),
        DFA.unpack(""),
        DFA.unpack("\1\u01b9"),
        DFA.unpack("\1\u01ba"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01bc"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\10\24\1"
        "\u01bd\21\24"),
        DFA.unpack("\1\u01bf"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01c1"),
        DFA.unpack(""),
        DFA.unpack("\1\u01c2"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01c4"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01c6"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01c8"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01ca"),
        DFA.unpack("\1\u01cb"),
        DFA.unpack("\1\u01cc"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01cf"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01d1"),
        DFA.unpack("\1\u01d2"),
        DFA.unpack(""),
        DFA.unpack("\1\u01d3"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01d5"),
        DFA.unpack("\1\u01d6"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u01d7"),
        DFA.unpack("\1\u01d8"),
        DFA.unpack("\1\u01d9"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01db"),
        DFA.unpack("\1\u01dc"),
        DFA.unpack(""),
        DFA.unpack("\1\u01dd"),
        DFA.unpack("\1\u01de"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01e0"),
        DFA.unpack("\1\u01e1"),
        DFA.unpack(""),
        DFA.unpack("\1\u01e2"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01e4"),
        DFA.unpack(""),
        DFA.unpack("\1\u01e5"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01e7"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01ea"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01ec"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01ee"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u01f0"),
        DFA.unpack("\1\u01f1"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01f4"),
        DFA.unpack("\1\u01f5"),
        DFA.unpack("\1\u01f6"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01f8"),
        DFA.unpack("\1\u01f9"),
        DFA.unpack("\1\u01fa"),
        DFA.unpack(""),
        DFA.unpack("\1\u01fb"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u01fd"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u01fe"),
        DFA.unpack(""),
        DFA.unpack("\1\u01ff"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u0203"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\1\u0206"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0209"),
        DFA.unpack(""),
        DFA.unpack("\1\u020a"),
        DFA.unpack("\1\u020b"),
        DFA.unpack("\1\u020c"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u020d"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u020e"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u020f"),
        DFA.unpack("\1\u0210"),
        DFA.unpack("\1\u0211"),
        DFA.unpack("\1\u0212"),
        DFA.unpack("\1\u0213"),
        DFA.unpack("\1\u0214"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0216"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u0218"),
        DFA.unpack("\1\u0219"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(""),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("\1\u021d"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\u021e"),
        DFA.unpack("\2\24\13\uffff\12\24\45\uffff\1\24\1\uffff\32\24"),
        DFA.unpack("")
    ]

    # class definition for DFA #15

    class DFA15(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA15_40 = input.LA(1)

                 
                index15_40 = input.index()
                input.rewind()
                s = -1
                if ((48 <= LA15_40 <= 57)):
                    s = 115

                elif (LA15_40 == 46) and ((self.numberDotValid())):
                    s = 117

                elif (LA15_40 == 101):
                    s = 118

                else:
                    s = 116

                 
                input.seek(index15_40)
                if s >= 0:
                    return s
            elif s == 1: 
                LA15_115 = input.LA(1)

                 
                index15_115 = input.index()
                input.rewind()
                s = -1
                if (LA15_115 == 101):
                    s = 118

                elif ((48 <= LA15_115 <= 57)):
                    s = 115

                elif (LA15_115 == 46) and ((self.numberDotValid())):
                    s = 117

                else:
                    s = 116

                 
                input.seek(index15_115)
                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 15, _s, input)
            self_.error(nvae)
            raise nvae
 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(sqlLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
