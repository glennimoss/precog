/*
Oracle SQL parser.

Originally based on:
| Oracle PL/SQL grammar built with ANTLR v3.2 and v3.1.3. I only vouch that it works for v3.2, though.
|
| Author: Patrick Higgins
| License: GNU Lesser General Public License, version 2.1 or (at your option) any later version.
|
| I have used a swallow_to_semi trick to avoid parsing SQL statements and other statements that were not of value to me.
| The idea was that a separate parser for SQL would be created (I believe this is what Oracle itself does).
|
| Nearly all of the PL/SQL language from 11g is in this grammar, though. It works on all files in a fairly large code
| base.
|
| This has some limited support for parsing SQL*Plus files, which turns out to be pretty hard to work into ANTLR.
|
| It works for my usage, but I think doing it properly would mean writing a Java class to parse the SQL*Plus language
| (which is pretty simple and shouldn't need ANTLR) and another adapter for ANTLR which enables tracking back to the
| original source line numbers. This PL/SQL parser might be invoked many times for each SQL*Plus file.
*/

grammar sql;

options {
  language=Python;
}

scope g { database }

@lexer::header {
  from antlr3.ext import NamedConstant, FileStream
  from . import util

  NL_CHANNEL = DEFAULT_CHANNEL + 1
}
@parser::header {
  from antlr3.ext import NamedConstant, FileStream
  from . import util
  from precog.identifier import OracleFQN
  from precog.objects import *
  from precog.util import InsensitiveDict

  NL_CHANNEL = DEFAULT_CHANNEL + 1
}
@lexer::init {
  self.aloneOnLine = util.aloneOnLine(lambda p: self.input.LT(p))
}
@parser::init {
  self._aloneOnLine = util.aloneOnLine(lambda p: self.input.LT(p).text)
}
@lexer::members {
  # needed for things like BETWEEN 1..2 where 1. would be treated as a literal
  def numberDotValid ():
      i = 1
      while self.input.LA(i) >= '0' and self.input.LA(i) <= '9':
          i += 1
      return self.input.LA(i) == '.' and self.input.LA(i+1) != '.'
}
@parser::members {
  def aloneOnLine (self):
    self.input.add(NL_CHANNEL)
    ret = self._aloneOnLine()
    self.input.drop(NL_CHANNEL)
    return ret
}
@lexer::main {
  NamedConstant.name(locals())

  def main(argv):
    from precog import reserved

    #from antlr3.ext import MultiChannelTokenStream
    inStream = FileStream(argv[1])
    lexer = sqlLexer(inStream)
    #tokenStream = MultiChannelTokenStream(lexer)
    #tokenStream.add(NL_CHANNEL, HIDDEN)
    tokenStream = CommonTokenStream(lexer)
    for t in tokenStream:
      print(t)
}
@parser::main {
  database = Database('fileschema')

  def main(argv):
    global schema
    from antlr3.ext import MultiChannelTokenStream
    from .sqlLexer import sqlLexer
    inStream = FileStream(argv[1])
    lexer = sqlLexer(inStream)
    tokenStream = MultiChannelTokenStream(lexer)
    parser = sqlParser(tokenStream)
    parser.sqlplus_file(database)
}

sqlplus_file[database]
scope g;
@init { $g::database = database }
    : ( stmt=sql_stmt { $g::database.add(stmt) }
      | stmt=sqlplus_stmt { print($stmt.mystmt) }
      /*| stmt=plsql_stmt*/
      )* EOF
    ;


plsql_stmt returns [mystmt]
  : type=( DECLARE
    | BEGIN
    | CREATE FUNCTION { $type = 'creating that function' }
    ) content+=~(TERMINATOR)+ TERMINATOR { $mystmt = repr($type) + '[' + ']['.join(x.text for x in $content) + ']' }
  ;

sql_stmt returns [stmt]
  : ( stmt_=create_table { $stmt = $stmt_.obj }
    | stmt_=create_index { $stmt = $stmt_.obj }
    ) SEMI
  ;

sqlplus_stmt returns [mystmt]
  : TERMINATOR { $mystmt = 'Repeat me!' }
  | kQUIT  { $mystmt = "Quittin' time!" }
  ;

/*
show_errors
    : kSHOW kERRORS SEMI?
    ;
    */

identifier returns [ident]
  : first=ID ( DOT second=ID ( DOT third=ID )? )?
    {
      schema = $first.text if $second else None
      obj = $second.text if $second else $first.text
      part = $third.text if $first and $second else None
      $ident = OracleFQN(schema, obj, part)
    }
  ;
create_table returns [obj]
@init {
  columns = []
  props = InsensitiveDict()
}
@after { obj = Table($ident.ident, columns=columns, **props) }
  : CREATE TABLE ident=identifier
    LPAREN
      c=column_specification { columns.append($c.column) }
      (COMMA c=column_specification { columns.append($c.column) } )*
    RPAREN
    (tablespace_clause { props.update($tablespace_clause.props) })?
  ;

column_specification returns [column]
@after { column = Column($i.text, **$c.props) }
  : i=ID c=column_data_type
    ( DEFAULT e=expression { $c.props['data_default'] = $e.text } )?
    ( NOT? NULL { $c.props['nullable'] = 'N' if $NOT else 'Y' } )?
  ;

column_data_type returns [props]
@after { $props = $type_props.props }
  :
  ( type_props=numeric_data_type
  | type_props=string_data_type
  | type_props=other_data_type
  | type_props=user_data_type
  )
  ;

numeric_data_type returns [props]
@init { props = InsensitiveDict() }
  : data_type=
  (NUMBER
  | FLOAT
  ) { props['data_type'] = $data_type.text }
  (p=numeric_data_type_precision { props.update($p.props) })?
  ;

numeric_data_type_precision returns [props]
@init { $props = InsensitiveDict() }
  : LPAREN ( precision=INTEGER
           (COMMA scale=INTEGER { props['data_scale'] = int($scale.text) })?
             { props['data_precision'] = int($precision.text) }
           | ASTERISK COMMA scale=INTEGER
             { props['data_scale'] = int($scale.text) } )
    RPAREN
  ;

string_data_type returns [props]
@init { $props = InsensitiveDict() }
  : type=VARCHAR2
    ( LPAREN INTEGER RPAREN { $props['data_length'] = int($INTEGER.text) })?
    { $props['data_type'] = $type.text }
  ;

other_data_type returns [props]
@init { $props = InsensitiveDict() }
  : d=DATE { $props['data_type'] = $d.text }
  ;

user_data_type returns [props]
  : i=identifier { $props = InsensitiveDict([('data_type', str($i.ident))]) }
  ;

create_index returns [obj]
@init {
  columns = []
  props = InsensitiveDict()
}
@after { obj = Index($index_name.ident, columns=columns, **props) }
  : CREATE ( UNIQUE /*| BITMAP*/ )? INDEX index_name=identifier
    ON table_name=identifier /*table_alias=ID?*/
    LPAREN
      c=ID {
        columns.append($g::database.find(
          OracleFQN($table_name.ident.schema, $table_name.ident.obj, $c.text),
          Column))
        }
      (COMMA c=ID {
        columns.append($g::database.find(
          OracleFQN($table_name.ident.schema, $table_name.ident.obj, $c.text),
          Column))
        }
      )*
    RPAREN
    (tablespace_clause { props.update($tablespace_clause.props) })?
  ;

tablespace_clause returns [props]
@init { props = InsensitiveDict() }
  : kTABLESPACE ID { props['tablespace_name'] = $ID.text }
  ;

expression
  : SYSDATE
  ;

/*


create_object
    : create_package
    | create_package_body
    | create_function
    | create_procedure
    ;

procedure_heading :
        PROCEDURE ID parameter_declarations?
    ;

function_heading :
        FUNCTION ID parameter_declarations? RETURN datatype
    ;

parameter_declarations :
        (   LPAREN  parameter_declaration ( COMMA  parameter_declaration )* RPAREN )
    ;

parameter_declaration :
        ID ( IN | ( ( OUT | IN OUT ) NOCOPY? ) )? datatype
        ( ( ASSIGN | DEFAULT ) expression )?
    ;

declare_section :
    ( type_definition SEMI
    | subtype_definition SEMI
    | cursor_definition SEMI
    | item_declaration SEMI
    | function_declaration_or_definition SEMI
    | procedure_declaration_or_definition SEMI
    | pragma SEMI
    )+
    ;

cursor_definition :
        CURSOR ID parameter_declarations? IS select_statement
    ;

item_declaration
    : variable_declaration
    | constant_declaration
    | exception_declaration
    ;

variable_declaration :
        ID datatype (  (  NOT NULL )? (  ASSIGN  | DEFAULT ) expression  )?
    ;

constant_declaration :
        ID CONSTANT datatype ( NOT NULL )? (   ASSIGN  | DEFAULT  ) expression
    ;

exception_declaration :
        ID EXCEPTION
    ;

type_definition :
        kTYPE ID IS ( record_type_definition | collection_type_definition | ref_cursor_type_definition )
    ;

subtype_definition :
        SUBTYPE ID IS datatype ( NOT NULL )?
    ;

record_type_definition :
	RECORD LPAREN record_field_declaration ( COMMA record_field_declaration )* RPAREN
    ;

record_field_declaration :
	ID datatype ( ( NOT NULL )? ( ASSIGN | DEFAULT ) expression )?
    ;

collection_type_definition
	:	varray_type_definition
	|	nested_table_type_definition
	;

varray_type_definition
	:	( VARYING ARRAY? | VARRAY ) LPAREN numeric_literal RPAREN kOF datatype ( NOT NULL )?
	;

nested_table_type_definition
	:	TABLE kOF datatype ( NOT NULL )? ( INDEX BY associative_index_type )?
	;

associative_index_type
	:	datatype
	;

ref_cursor_type_definition
	:	REF CURSOR ( RETURN datatype )?
	;

datatype
    : ( REF )? ID ( DOT ID )? ( LPAREN numeric_literal ( COMMA numeric_literal )* RPAREN | PERCENT ( kTYPE | ROWTYPE ) )?
    ;

function_declaration_or_definition :
        function_heading
        ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
        ( ( IS | AS ) declare_section? body )?
	;

function_declaration :
        function_heading
        ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
    ;

function_definition :
        function_heading
        ( DETERMINISTIC | PIPELINED | PARALLEL_ENABLE | RESULT_CACHE )*
        ( IS | AS ) declare_section? body
	;

procedure_declaration_or_definition :
        procedure_heading
        ( ( IS | AS ) declare_section? body )?
    ;

procedure_declaration :
	procedure_heading
	;

procedure_definition :
	procedure_heading
	( IS | AS ) declare_section? body
	;

body 	:
	BEGIN statement SEMI ( statement SEMI | pragma SEMI )*
	( EXCEPTION exception_handler+ )? END ID?
	;

exception_handler
	:	WHEN ( qual_id ( OR qual_id )* | OTHERS )
		THEN ( statement SEMI )+
	;

statement :
    label*
    ( assign_or_call_statement
    | case_statement
    | close_statement
    | continue_statement
    | basic_loop_statement
    | execute_immediate_statement
    | exit_statement
    | fetch_statement
    | for_loop_statement
    | forall_statement
    | goto_statement
    | if_statement
    | null_statement
    | open_statement
    | plsql_block
    | raise_statement
    | return_statement
    | sql_statement
    | while_loop_statement
    )
    ;

lvalue
    : call ( DOT call )*
    ;

assign_or_call_statement
    : lvalue ( DOT delete_call | ASSIGN expression )?
    ;

call
    : COLON? ID ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN )?
    ;

delete_call
    : DELETE ( LPAREN parameter? RPAREN )?
    ;

basic_loop_statement :
        LOOP ( statement SEMI )+ END LOOP label_name?
    ;

case_statement :
        CASE expression?
        ( WHEN expression THEN ( statement SEMI )+ )+
        ( ELSE statement SEMI )?
        END CASE label_name?
    ;

close_statement :
        CLOSE ID ( DOT ID )?
    ;

continue_statement :
        CONTINUE ( lbl=ID )? ( WHEN expression )?
    ;

execute_immediate_statement :
        EXECUTE IMMEDIATE expression (
        ( into_clause | bulk_collect_into_clause) using_clause?
        | using_clause dynamic_returning_clause?
        | dynamic_returning_clause
        )?
    ;

exit_statement :
        EXIT ( lbl=ID )? ( WHEN expression )?
    ;

fetch_statement :
        FETCH qual_id ( into_clause | bulk_collect_into_clause ( LIMIT numeric_expression )? )
    ;

into_clause :
        INTO lvalue ( COMMA lvalue )*
    ;

bulk_collect_into_clause :
        BULK COLLECT INTO lvalue ( COMMA lvalue )*
    ;

using_clause :
        USING param_modifiers? expression ( COMMA param_modifiers? expression )*
    ;

param_modifiers
	: IN OUT? | OUT
	;

dynamic_returning_clause :
        ( RETURNING | RETURN ) ( into_clause | bulk_collect_into_clause )
    ;

for_loop_statement :
        FOR ID IN ( ~(LOOP) )+ LOOP ( statement SEMI )+ END LOOP label_name?
    ;

forall_statement :
        FORALL ID IN bounds_clause sql_statement ( kSAVE kEXCEPTIONS )?
    ;

bounds_clause
    : numeric_expression DOUBLEDOT numeric_expression
    | kINDICES kOF atom ( BETWEEN numeric_expression AND numeric_expression )?
    | kVALUES kOF atom
    ;

goto_statement :
        GOTO label_name
    ;

if_statement :
        IF expression THEN ( statement SEMI )+
        ( ELSIF expression THEN ( statement SEMI )+ )*
        ( ELSE ( statement SEMI )+ )?
        END IF
    ;

null_statement :
        NULL
    ;

open_statement :
        OPEN ID ( DOT ID )* call_args? ( FOR select_statement )?
    ;

pragma :
        PRAGMA swallow_to_semi
    ;

raise_statement :
        RAISE ( ID ( DOT ID )* )?
    ;

return_statement :
        RETURN expression?
    ;

plsql_block :
        ( DECLARE declare_section )? body
    ;

label :
        LLABEL label RLABEL
    ;

qual_id :
	COLON? ID ( DOT COLON? ID )*
    ;

sql_statement
    : commit_statement
    | delete_statement
    | insert_statement
    | lock_table_statement
    | rollback_statement
    | savepoint_statement
    | select_statement
    | set_transaction_statement
    | update_statement
    ;

commit_statement :
        COMMIT swallow_to_semi?
    ;

delete_statement :
        DELETE swallow_to_semi
    ;

insert_statement :
        INSERT swallow_to_semi
    ;

lock_table_statement :
        LOCK TABLE swallow_to_semi
    ;

rollback_statement :
        ROLLBACK swallow_to_semi?
    ;

savepoint_statement :
        SAVEPOINT ID
    ;

select_statement :
        SELECT swallow_to_semi
    ;

set_transaction_statement :
        SET TRANSACTION swallow_to_semi
    ;

update_statement :
        UPDATE swallow_to_semi
    ;

swallow_to_semi :
        ~( SEMI )+
    ;

while_loop_statement :
        WHILE expression LOOP ( statement SEMI )+ END LOOP label_name?
    ;

match_parens
    : ( options {greedy=false;} : ~( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT ) )*
    | RPAREN match_parens LPAREN
    ;

label_name:	ID;

expression
    : or_expr
    ;

or_expr
    : and_expr ( OR and_expr )*
    ;

and_expr
    : not_expr ( AND not_expr )*
    ;

not_expr
    : NOT? compare_expr
    ;

compare_expr
    : is_null_expr ( ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ ) is_null_expr )?
    ;

is_null_expr
    : like_expr ( IS NOT? NULL)?
    ;

like_expr
    : between_expr ( NOT? LIKE between_expr )?
    ;

between_expr
    : in_expr ( NOT? BETWEEN in_expr AND in_expr )?
    ;

in_expr
    : add_expr ( NOT? IN LPAREN add_expr ( COMMA add_expr )* RPAREN )?
    ;

numeric_expression
    : add_expr
    ;

add_expr
    : mul_expr ( ( MINUS | PLUS | DOUBLEVERTBAR ) mul_expr )*
    ;

mul_expr
    : unary_sign_expr ( ( ASTERISK | SLASH | kMOD ) unary_sign_expr )*
    ;

unary_sign_expr
    : ( MINUS | PLUS )? exponent_expr
    ;

exponent_expr
    : atom ( EXPONENT atom )?
    ;

atom
    : variable_or_function_call ( PERCENT attribute )?
    | SQL PERCENT attribute
    | string_literal
    | numeric_atom
    | boolean_atom
    | NULL
    | LPAREN expression RPAREN
    ;

variable_or_function_call
    : call ( DOT call )* ( DOT delete_call )?
    ;

attribute
    : BULK_ROWCOUNT LPAREN expression RPAREN
    | kFOUND
    | ISOPEN
    | NOTFOUND
    | kROWCOUNT
    ;

call_args
    : LPAREN ( parameter ( COMMA parameter )* )? RPAREN
    ;

boolean_atom
    : boolean_literal
    | collection_exists
    | conditional_predicate
    ;

numeric_atom
    : numeric_literal
    ;

numeric_literal
    : INTEGER
    | REAL_NUMBER
    ;

boolean_literal
    : TRUE
    | FALSE
    ;

string_literal
    : QUOTED_STRING
    ;

collection_exists
    : ID DOT EXISTS LPAREN expression RPAREN
    ;

conditional_predicate
    : INSERTING
    | UPDATING ( LPAREN QUOTED_STRING RPAREN )?
    | DELETING
    ;

parameter
    : ( ID ARROW )? expression
    ;

index
    : expression
    ;

create_package :
        CREATE ( OR kREPLACE )? PACKAGE ( schema_name=ID DOT )? package_name=ID
        ( invoker_rights_clause )?
        ( IS | AS ) ( declare_section )? END ( ID )? SEMI
    ;

create_package_body :
        CREATE ( OR kREPLACE )? PACKAGE BODY ( schema_name=ID DOT )? package_name=ID
        ( IS | AS ) ( declare_section )?
        ( initialize_section=body | END ( package_name2=ID )? )
        SEMI
    ;

create_procedure :
        CREATE ( OR kREPLACE )? PROCEDURE ( schema_name=ID DOT )? procedure_name=ID
        ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )?
        invoker_rights_clause?
        ( IS | AS )
        ( declare_section? body
        | call_spec
        | EXTERNAL
        ) SEMI
    ;

create_function :
        CREATE ( OR kREPLACE )? FUNCTION ( schema_name=ID DOT )? function_name=ID
        ( LPAREN parameter_declaration ( COMMA parameter_declaration )* RPAREN )?
        RETURN datatype
        invoker_rights_clause?
        ( IS | AS )
        ( declare_section? body
        | call_spec
        | EXTERNAL
        ) SEMI
    ;

invoker_rights_clause :
        AUTHID ( CURRENT_USER | DEFINER )
    ;

call_spec
    : LANGUAGE swallow_to_semi
    ;

kERRORS : { len(self.input.LT(1).text) >= 3 and "errors".startswith(self.input.LT(1).text.lower())}? ID;
kEXCEPTIONS : {self.input.LT(1).text.lower() == "exceptions"}? ID;
kFOUND : {self.input.LT(1).text.lower() == "found"}? ID;
kINDICES : {self.input.LT(1).text.lower() == "indices"}? ID;
kMOD : {self.input.LT(1).text.lower() == "mod"}? ID;
kNAME : {self.input.LT(1).text.lower() == "name"}? ID;
kOF : {self.input.LT(1).text.lower() == "of"}? ID;
kREPLACE : {self.input.LT(1).text.lower() == "replace"}? ID;
kROWCOUNT : {self.input.LT(1).text.lower() == "rowcount"}? ID;
kSAVE : {self.input.LT(1).text.lower() == "save"}? ID;
kSHOW : {self.input.LT(1).text.lower() == "show"}? ID;
kTYPE : {self.input.LT(1).text.lower() == "type"}? ID;
kVALUES : {self.input.LT(1).text.lower() == "values"}? ID;

*/

kCLOB : {self.input.LT(1).text.lower() == 'clob'}? ID;
kTABLESPACE : {self.input.LT(1).text.lower() == 'tablespace'}? ID;
kQUIT : {self.input.LT(1).text.lower() == 'quit' and self.aloneOnLine()}? ID;

/*****
 * PL/SQL Reserved words
 *****/
kWHEN	:	{self.input.LT(1).text.lower() == 'when'}? ID;

/*****
 * Keywords
 *****/
ADD : 'add' ;
ALTER : 'alter' ;
AND	:	'and'	;
ARRAY : 'array' ;
AS : 'as' ;
AUTHID: 'authid';
BEGIN	:	'begin'	;
BETWEEN : 'between' ;
BODY	:	'body';
BULK: 'bulk';
BULK_ROWCOUNT: 'bulk_rowcount';
BY	:	'by';
CASE: 'case';
CHAR : 'char' ;
CHECK : 'check' ;
CLOSE	:	'close';
COLLECT:	'collect';
COMMIT	:	'commit';
CONSTANT	:	'constant'	;
CONTINUE:	'continue';
CREATE: 'create';
CURRENT_USER: 'current_user';
CURSOR	:	'cursor'	;
DATE : 'date' ;
DECLARE	:	'declare'	;
DEFAULT : 'default' ;
DEFINER: 'definer';
DELETE	:	'delete';
DELETING:	'deleting';
DETERMINISTIC	: 'deterministic'	;
DROP : 'drop' ;
ELSE : 'else' ;
ELSIF	:	'elsif';
END	:	'end'	;
EXCEPTION	:	'exception'	;
EXECUTE	:	'execute';
EXISTS	:	'exists';
EXIT	:	'exit';
EXTERNAL:	'external';
FALSE	:	'false';
FETCH	:	'fetch';
FLOAT : 'float';
FOR : 'for' ;
FORALL : 'forall' ;
FROM : 'from' ;
FUNCTION	:	'function'	;
GOTO	:	'goto';
IF	:	'if';
IMMEDIATE	:	'immediate';
IN : 'in' ;
INCREMENT : 'increment' ;
INDEX : 'index' ;
INSERT	:	'insert';
INSERTING :	'inserting';
INTO	:	'into';
IS : 'is' ;
ISOPEN	:	'isopen';
LANGUAGE:	'language';
LIKE : 'like' ;
LIMIT : 'limit' ;
LOCK	:	'lock';
LOOP	:	'loop';
NOCOPY	:	'nocopy'	;
NOT : 'not' ;
NOTFOUND:	'notfound';
NULL : 'null' ;
NUMBER : 'number' ;
OF : 'of' ;
ON : 'on' ;
OPEN	:	'open';
OR : 'or' ;
OTHERS	:	'others'	;
OUT	:	'out'	;
PACKAGE: 'package';
PARALLEL_ENABLE	:	'parallel_enable';
PIPELINED	:	'pipelined'	;
PRAGMA	:	'pragma'	;
PROCEDURE	:	'procedure'	;
RAISE	:	'raise';
RECORD	:	'record'	;
REF	:	'ref'	;
RESULT_CACHE	:	'result_cache'	;
RETURN	:	'return'	;
RETURNING	:	'returning'	;
ROLLBACK:	'rollback';
ROW : 'row' ;
ROWTYPE	:	'rowtype'	;
SAVEPOINT	:	'savepoint';
SELECT	:	'select';
SET	:	'set';
SQL	:	'sql';
START : 'start' ;
SUBTYPE	:	'subtype'	;
SYSDATE : 'sysdate' ;
TABLE	:	'table';
THEN : 'then' ;
TRANSACTION	:	'transaction';
TRIGGER : 'trigger' ;
TRUE	:	'true';
UNIQUE : 'unique';
UPDATE	:	'update';
UPDATING:	'updating';
USING:	'using'	;
VALUES : 'values' ;
VARCHAR : 'varchar' ;
VARCHAR2 : 'varchar2' ;
VARRAY	:	'varray'	;
VARYING	:	'varying'	;
WHERE : 'where' ;
WHILE	:	'while';
WITH : 'with' ;

QUOTED_STRING
	:	( 'n' )? '\'' ( '\'\'' | ~('\'') )* '\''
	;

ID
	:	( 'a' .. 'z' )
		( 'a' .. 'z' | '0' .. '9' | '_' | '$' | '#' )*
	|	DOUBLEQUOTED_STRING
	;
SEMI
	:	';'
	;
COLON
	:	':'
	;
DOUBLEDOT
	:	POINT POINT
	;
DOT
	:	POINT
	;
fragment
POINT
	:	'.'
	;
COMMA
	:	','
	;
EXPONENT
	:	'**'
	;
ASTERISK
	:	'*'
	;
AT_SIGN
	:	'@'
	;
RPAREN
	:	')'
	;
LPAREN
	:	'('
	;
RBRACK
	:	']'
	;
LBRACK
	:	'['
	;
PLUS
	:	'+'
	;
MINUS
	:	'-'
	;
SLASH
	:	'/'
	;
EQ
	:	'='
	;
PERCENT
	:	'%'
	;
LLABEL
	:	'<<'
	;
RLABEL
	:	'>>'
	;
ASSIGN
	:	':='
	;
ARROW
	:	'=>'
	;
VERTBAR
	:	'|'
	;
DOUBLEVERTBAR
	:	'||'
	;
NOT_EQ
	:	'<>' | '!=' | '~='| '^='
	;
LTH
	:	'<'
	;
LEQ
	:	'<='
	;
GTH
	:	'>'
	;
GEQ
	:	'>='
	;
INTEGER
    :   N
    ;
REAL_NUMBER
	:	NUMBER_VALUE	( 'e' ( PLUS | MINUS )? N )?
	;
fragment
NUMBER_VALUE
	:	{self.numberDotValid()}?=> N POINT N?
	|	POINT N
	|	N
	;
fragment
N
	: ('0'..'9')+
	;
fragment
DOUBLEQUOTED_STRING
	:	'"' ( ~('"') )* '"'
	;
NL : '\r'? '\n' { $channel = NL_CHANNEL } ;
SPACE	:	(' '|'\t') { $channel=HIDDEN } ;
SL_COMMENT
	:	'--' ~('\n'|'\r')* NL {$channel=HIDDEN;}
	;
ML_COMMENT
	:	'/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
	;
TERMINATOR
  : { self.aloneOnLine() }? SLASH
  ;
