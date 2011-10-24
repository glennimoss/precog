/*
Oracle SQL parser.

Originally based on a grammar by Patrick Higgins
*/

grammar sql;

options {
  language=Python;
  superClass=LoggingParser;
}

scope g { database }

scope tab_col_ref { alias_map; table; columns }

scope expression_ctx { ctx_name }

@lexer::header {
  from antlr3.ext import NamedConstant, FileStream, NL_CHANNEL
  from precog.parser.util import *

  # Monkey patch in our lexer superclass
  Lexer = LoggingLexer
}
@parser::header {
  import os

  from antlr3.exceptions import RecognitionException
  from antlr3.ext import NamedConstant, FileStream, NL_CHANNEL
  from precog.parser.util import *
  from precog.identifier import OracleFQN, OracleIdentifier, GeneratedId
  from precog.objects import *
  from precog.util import InsensitiveDict
}
@lexer::init {
  self.aloneOnLine = aloneOnLine(lambda p: self.input.LT(p))
}
@parser::init {
  self._aloneOnLine = aloneOnLine(lambda p: self.input.LT(p).text)
}
@lexer::members {
  # needed for things like BETWEEN 1..2 where 1. would be treated as a literal
  def numberDotValid (self):
      i = 1
      while self.input.LT(i) >= '0' and self.input.LT(i) <= '9':
          i += 1
      return self.input.LT(i) == '.' and self.input.LT(i+1) != '.'
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
    from antlr3.ext import IterableTokenStream

    #from antlr3.ext import MultiChannelTokenStream
    inStream = FileStream(argv[1])
    lexer = sqlLexer(inStream)
    tokenStream = IterableTokenStream(lexer)
    for t in tokenStream:
      print(t)
}

sqlplus_file[database]
scope { stmt_begin; }
scope g;
@init { $g::database = $database }
    : ( { $sqlplus_file::stmt_begin = self.input.LT(1) }
        ( stmt=sql_stmt
        | stmt=plsql_stmt
        )  { $g::database.add($stmt.obj) }
        | sqlplus_stmt
      )* EOF
    ;

plsql_stmt returns [obj]
scope { type; name; props }
@init { $plsql_stmt::props = InsensitiveDict() }
@after {
  $obj = PlsqlCode.new($plsql_stmt::type, $plsql_stmt::name, $source.text,
    **$plsql_stmt::props)
}
  : CREATE (OR kREPLACE)? source=plsql_object_def
    TERMINATOR
  ;

plsql_object_def
@after {
  if $pb.text or $tb.text:
    # This is a body, so it depends on its header.
    header_type = Package if $pb.text else Type
    $plsql_stmt::props['header'] = $g::database.find($i.ident, header_type)
}
  : ( kFUNCTION { $plsql_stmt::type = 'FUNCTION' }
    | PROCEDURE { $plsql_stmt::type = 'PROCEDURE' }
    | kPACKAGE pb=kBODY?
      {
        $plsql_stmt::type = "PACKAGE{}".format(' BODY' if $pb.text else '')
      }
    | TRIGGER { $plsql_stmt::type = 'TRIGGER' }
    | kTYPE tb=kBODY?
      { $plsql_stmt::type = "TYPE{}".format(' BODY' if $tb.text else '') }
    ) i=identifier { $plsql_stmt::name = $i.ident }
    ( IS | AS )
    ( (~TERMINATOR)=> ~TERMINATOR )+
  ;


sql_stmt returns [obj]
  : ( stmt_=create_table { $obj = $stmt_.obj }
    | stmt_=create_index { $obj = $stmt_.obj }
    | stmt_=create_sequence { $obj = $stmt_.obj }
    | stmt_=create_synonym { $obj = $stmt_.obj }
    | stmt_=insert_statement { $obj = $stmt_.obj }
    ) SEMI
  ;

sqlplus_stmt returns [stmt]
  : TERMINATOR { $stmt = 'Repeat me!' }
  | kQUIT  { $stmt = "Quittin' time!" }
  | (AT_SIGN | relative=DOUBLE_AT_SIGN) { self.input.add(NL_CHANNEL) }
    file_name=swallow_to_nl NL
    {
      file_name = $file_name.text
      if $relative:
        relative_dir = os.path.dirname(self.input.getSourceName())

        file_name = ''.join((relative_dir,
                             os.sep if relative_dir else '',
                             file_name))

      $g::database.add_file(file_name)
    }
  ;
finally {
  self.input.drop(NL_CHANNEL)
}

/*
show_errors
    : kSHOW kERRORS SEMI?
    ;
    */

identifier returns [ident]
  : first=ID ( DOT second=ID ( DOT third=ID )? )?
    // TODO: this should probably check for schemas to determine if it's
    // schema.obj or obj.part
    {
      schema = $first.text if $second else None
      obj = $second.text if $second else $first.text
      part = $third.text if $third else None
      $ident = OracleFQN(schema, obj, part)
    }
  ;

tID returns [id, token]
  : i=ID
    {
      $id = OracleIdentifier($i.text)
      $token = $i
    }
  ;

aliasing_identifier returns [ident]
  : i=identifier alias=tID? {
      $ident = $i.ident
      if $alias.id:
        if not $tab_col_ref::alias_map:
          $tab_col_ref::alias_map = InsensitiveDict()

        $tab_col_ref::alias_map[$alias.id] = $ident
    }
  ;

aliased_identifier returns [ident]
  : parts=part_identifier
    {
      resolved = None
      if $tab_col_ref::alias_map and $parts.parts[0] in $tab_col_ref::alias_map:
        resolved = $tab_col_ref::alias_map[$parts.parts[0]]
        $parts.parts.pop(0)

      $ident = OracleIdentifier($parts.parts)
      if resolved:
        $ident = OracleFQN(resolved.schema, resolved.obj, $ident)

      #self.logSyntaxWarning("Alias [{}] does not exist".format($alias.id),
        #self.input, $alias.token.index, $alias.token.line,
        #$alias.token.charPositionInLine)
    }
  ;

part_identifier returns [parts]
scope { _parts; }
@init { $part_identifier::_parts = [] }
@after { $parts = [$first.id] + $part_identifier::_parts }
  : first=tID (DOT part_identifier_part)*
  ;

part_identifier_part
  : part=tID { $part_identifier::_parts.append($part.id) }
  ;

create_table returns [obj]
scope { props; table_name }
scope expression_ctx;
@init {
  $create_table::props = InsensitiveDict({'columns': [], 'constraints': set()})
}
@after {
  $obj = Table($ident.ident, database=$g::database, **$create_table::props)
}
  : CREATE TABLE ident=identifier {
      $create_table::table_name = $ident.ident
      $expression_ctx::ctx_name = $ident.ident
    }
    LPAREN
      table_item (COMMA table_item)*
    RPAREN
    (tablespace_clause { props.update($tablespace_clause.props) })?
  ;

table_item
  : col=col_spec { $create_table::props['columns'].append($col.column) }
  | cons=out_of_line_constraint {
      $create_table::props['constraints'].add($cons.constraint)
    }
  ;

col_spec returns [column]
scope { props }
@init {
  $col_spec::props = InsensitiveDict()
  $col_spec::props['constraints'] = set()
}
@after {
  $column = Column($i.id, **$col_spec::props)
}
  : i=tID
    ( column_data_type
      ( DEFAULT e=expression
        { $col_spec::props['data_default'] = $e.exp.text } )?
    | ( kGENERATED kALWAYS )? AS LPAREN virt=expression RPAREN kVIRTUAL? {
        $col_spec::props['virtual_column'] = 'YES'
        $col_spec::props['data_default'] = $virt.exp.text
      }
    )
    ( ic=inline_constraint {
        if $ic.cons:
          $col_spec::props['constraints'].add($ic.cons)
      }
    )*
  ;

column_data_type
  : string_data_type
  | numeric_data_type
  | long_raw_data_type
  | datetime_data_type
  | lob_data_type
  | rowid_data_type
  | oracle_data_type
  | user_data_type
  ;

int_parameter returns [val]
  : LPAREN i=tINTEGER RPAREN { $val = $i.val }
  ;

string_data_type
  : (t=CHAR | t=VARCHAR2) { $col_spec::props['data_type'] = $t.text.upper() }
    ( LPAREN
      l=tINTEGER { $col_spec::props['char_length'] = $l.val }
      ( kBYTE { $col_spec::props['char_used'] = 'B' }
      | CHAR { $col_spec::props['char_used'] = 'C' }
      )?
      RPAREN
    )?
  | (nt=kNCHAR | nt=kNVARCHAR2) {
      $col_spec::props['data_type'] = $nt.text.upper()
    }
    (l=int_parameter { $col_spec::props['char_length'] = $l.val })?
  ;

numeric_data_type
@after {
  $col_spec::props['data_type'] = (($t and $t.text) or
                                   $k1.text or $k2.text).upper()
}
  : t=NUMBER number_precision?
  | t=FLOAT (p=int_parameter { $col_spec::props['data_precision'] = $p.val })?
  | k1=kBINARY_FLOAT
  | k2=kBINARY_DOUBLE
  ;

number_precision
  : LPAREN
     ( precision=tINTEGER
       { $col_spec::props['data_precision'] = $precision.val }
       (COMMA neg=HYPHEN? scale=tINTEGER)?
     | ASTERISK COMMA neg=HYPHEN? scale=tINTEGER
     )
     {
       if $scale.val:
         $col_spec::props['data_scale'] = $scale.val * (-1 if $neg else 1)
     }
    RPAREN
  ;

long_raw_data_type
@after {
  $col_spec::props['data_type'] = OracleIdentifier(
    ' '.join(w.text.upper() for w in $t), True)
}
  : t+=LONG t+=RAW?
  | t+=RAW i=int_parameter { $col_spec::props['data_length'] = $i.val }
  ;

datetime_data_type
  : DATE
    { $col_spec::props['data_type'] = 'DATE' }
  | kTIMESTAMP i=int_parameter? (t=WITH l=kLOCAL? kTIME kZONE)?
    {
      $col_spec::props['data_type'] = "TIMESTAMP({}){}".format(
        $i.val or 6,
        " WITH {}TIME ZONE".format('LOCAL ' if $l.text else '')
          if $t else '')
    }
  | kINTERVAL
    ( kYEAR i=int_parameter? TO kMONTH
    {
      $col_spec::props['data_type'] = "INTERVAL YEAR({}) TO MONTH".format(
        $i.val or 2)
    }
    | kDAY d=int_parameter? TO kSECOND s=int_parameter?
    {
      $col_spec::props['data_type'] = "INTERVAL DAY({}) TO SECOND({})".format(
        $d.val or 2, $s.val or 6)
    }
    )
  ;

lob_data_type
@after {
  $col_spec::props['data_type'] = ($t1.text or $t2.text or $t3.text or
                                   $t4.text).upper()
}
  : t1=kBLOB
  | t2=kCLOB
  | t3=kNCLOB
  | t4=kBFILE
  ;

rowid_data_type
@after { $col_spec::props['data_type'] = (($t and $t.text) or $k.text).upper() }
  : t=ROWID
  | k=kUROWID (i=int_parameter { $col_spec::props['data_length'] = $i.val })?
  ;

oracle_data_type
@after { $col_spec::props['data_type'] = ($t1.text or $t2.text).upper() }
  : t1=kXMLTYPE
  | t2=kURITYPE
  ;

user_data_type
  : i=identifier {
      user_type = $g::database.find($i.ident, Type)
      $col_spec::props['user_type'] = user_type
    }
  ;

inline_constraint returns [cons]
@init {
  args = []
  cons_class = None
  props = InsensitiveDict()
  index = None
}
@after {
  if cons_class:
    $cons = cons_class($constraint_name.id, database=$g::database, **props)
  else:
    $cons = None
}
  : ( NOT? NULL { $col_spec::props['nullable'] = 'N' if $NOT else 'Y' }
    | ( kCONSTRAINT constraint_name=tID // Non-spec: making required
      | {
          token = self.input.LT(1)
          self.logSyntaxError('"CONSTRAINT [constraint_name]" is required.',
                              self.input, token.index, token.line,
                              token.charPositionInLine)
          constraint_name = self.tID_return()
          constraint_name.id = GeneratedId()
        } )
      ( ( UNIQUE { props['is_pk'] = False }
        | kPRIMARY kKEY { props['is_pk'] = True }
        ) { index_props = InsensitiveDict() }
        ( kUSING INDEX
          ( index_name=identifier {
              index = $g::database.find($index_name.ident, Index)
            }
          | LPAREN new_index=create_index RPAREN {
              index = $new_index.obj
              $g::database.add(index)
            }
          | ts=tablespace_clause { index_props.update($ts.props) }
          )
        )?
        {
          if not index:
            index = Index($constraint_name.id, database=$g::database,
                          **index_props)
            $g::database.add(index)

          props['index'] = index
          cons_class = UniqueConstraint
        }
      | ref=references_clause {
          props.update($ref.props)
          cons_class = ForeignKeyConstraint
        }
      | CHECK LPAREN check_exp=expression RPAREN {
          props['condition'] = $check_exp.exp
          cons_class = CheckConstraint
        }
      )
      ( kENABLE { props['is_enabled'] = True }
      | kDISABLE { props['is_enabled'] = False } )?
    )
  ;

references_clause returns [props]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  props = InsensitiveDict({'delete_action': 'NO ACTION'})
}
@after {
  $props['fk_constraint'] = $g::database.find_unique_constraint(
    $tab_col_ref::columns)
}
  : kREFERENCES ref=identifier { $tab_col_ref::table = $ref.ident }
    LPAREN column_ref (COMMA column_ref)* RPAREN // Non-spec: making required
    (ON DELETE ( kCASCADE { $props['delete_action'] = 'CASCADE' }
               | SET NULL { $props['delete_action'] = 'SET NULL' } ) )?
  ;

out_of_line_constraint returns [constraint]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  $tab_col_ref::table = $create_table::table_name
  props = InsensitiveDict()
  cons_class = Constraint
}
@after {
  $constraint = cons_class($constraint_name.id, database=$g::database, **props)
}
  : kCONSTRAINT constraint_name=tID // Non-spec: making required
    ( ( ( UNIQUE { props['is_pk'] = False }
        | kPRIMARY kKEY { props['is_pk'] = True } )
        { cons_class = UniqueConstraint }
      | kFOREIGN kKEY
        { cons_class = ForeignKeyConstraint }
      )
      LPAREN
        column_ref (COMMA column_ref)*
      RPAREN
      { props['columns'] = $tab_col_ref::columns }
      ( { cons_class == ForeignKeyConstraint }? ref=references_clause {
          props.update($ref.props)
          cons_class = ForeignKeyConstraint
        }
      | // { cons_class != ForeignKeyConstraint }? // Nothing
      )
    | CHECK LPAREN check_exp=expression RPAREN {
        props['condition'] = $check_exp.exp
        cons_class = CheckConstraint
      }
    )
    ( kENABLE { props['is_enabled'] = True }
    | kDISABLE { props['is_enabled'] = False } )?
  ;

column_ref
  : c=aliased_identifier {
      fqn = $c.ident
      if not isinstance(fqn, OracleFQN):
        fqn = OracleFQN($tab_col_ref::table.schema,
          $tab_col_ref::table.obj, $c.ident)

      $tab_col_ref::columns.append($g::database.find(fqn, Column))
    }
  ;

create_index returns [obj]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  props = InsensitiveDict()
}
@after {
  table = $g::database.find($tab_col_ref::table, Table)
  #$obj = Index($index_name.ident, table=table, columns=$tab_col_ref::columns,
  $obj = Index($index_name.ident, columns=$tab_col_ref::columns,
    database=$g::database, **props)
}
  : CREATE ( UNIQUE { props['uniqueness'] = 'UNIQUE' }
           | kBITMAP
           | { props['uniqueness'] = 'NONUNIQUE' }
           )
    INDEX index_name=identifier
    ON table_name=aliasing_identifier
      { $tab_col_ref::table = $table_name.ident }
    LPAREN
      column_ref (COMMA column_ref)*
    RPAREN
    (tablespace_clause { props.update($tablespace_clause.props) })?
  ;

tablespace_clause returns [props]
@init { $props = InsensitiveDict() }
  : kTABLESPACE ID { $props['tablespace_name'] = $ID.text }
  ;

create_sequence returns [obj]
scope { props }
@init { $create_sequence::props = InsensitiveDict() }
@after {
  $obj = Sequence($i.ident, database=$g::database, **$create_sequence::props)
}
  : CREATE kSEQUENCE i=identifier
    sequence_prop*
  ;

sequence_prop
  : INCREMENT BY n=tINTEGER
    { $create_sequence::props['increment_by'] = $n.val }
  | START WITH n=tINTEGER
    { $create_sequence::props['start_with'] = $n.val }
  | kMAXVALUE n=tINTEGER
    { $create_sequence::props['maxvalue'] = $n.val }
  | kNOMAXVALUE
    { $create_sequence::props['maxvalue'] = 9999999999999999999999999999 }
  | kMINVALUE n=tINTEGER
    { $create_sequence::props['minvalue'] = $n.val }
  | kNOMINVALUE
    { $create_sequence::props['minvalue'] = 1 }
  | kCYCLE
    { $create_sequence::props['cycle_flag'] = 'Y' }
  | kNOCYCLE
    { $create_sequence::props['cycle_flag'] = 'N' }
  | kCACHE n=tINTEGER
    { $create_sequence::props['cache_size'] = $n.val }
  | kNOCACHE
    { $create_sequence::props['cache_size'] = 0 }
  | ORDER
    { $create_sequence::props['order_flag'] = 'Y' }
  | kNOORDER
    { $create_sequence::props['order_flag'] = 'N' }
  ;

create_synonym returns [obj]
  : CREATE (OR kREPLACE)? SYNONYM syn=identifier FOR target=identifier
    {
      $obj = Synonym($syn.ident, $g::database.find($target.ident, OracleObject),
        database=$g::database)
    }
  ;
insert_statement returns [obj]
scope { expressions; }
scope tab_col_ref, expression_ctx;
@init {
  $insert_statement::expressions = []
  $tab_col_ref::columns = []
}
@after {
  table.add_data($tab_col_ref::columns, $insert_statement::expressions)
}
  : INSERT INTO table_name=aliasing_identifier
    {
      $tab_col_ref::table = $table_name.ident
      $expression_ctx::ctx_name = $table_name.ident
      table = $g::database.find($tab_col_ref::table, Table)
    }
    LPAREN
      column_ref (COMMA column_ref)*
    RPAREN
    VALUES
    LPAREN
      insert_expression (COMMA insert_expression)*
    RPAREN
    ;

insert_expression
  : exp=expression { $insert_statement::expressions.append($exp.text) }
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

body :
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

while_loop_statement :
        WHILE expression LOOP ( statement SEMI )+ END LOOP label_name?
    ;

match_parens
    : ( options {greedy=false;} : ~( RPAREN | LPAREN | SEMI | AS | IS | IN | OUT ) )*
    | RPAREN match_parens LPAREN
    ;

label_name:	ID;

*/

expression returns [exp]
scope { refs }
@init {
  $expression::refs = set()
}
@after {
  $exp = Expression($e.text, $expression::refs)
}
    : e=or_expr
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

/*
numeric_expression
    : add_expr
    ;
*/

add_expr
    : mul_expr ( ( HYPHEN | PLUS | DOUBLEVERTBAR ) mul_expr )*
    ;

mul_expr
    : unary_sign_expr ( ( ASTERISK | SLASH | kMOD ) unary_sign_expr )*
    ;

unary_sign_expr
    : ( HYPHEN | PLUS )? exponent_expr
    ;

exponent_expr
    : atom ( EXPONENT atom )?
    ;

atom
    //: variable_or_function_call ( PERCENT attribute )?
    : call ( PERCENT attribute )?
    | SQL PERCENT attribute
    | string_literal
    | numeric_atom
    | boolean_atom
    | global_name_literal
    | NULL
    | LPAREN expression RPAREN
    ;

global_name_literal
  : SYSDATE
  ;

/*
variable_or_function_call
    : call ( DOT call )* /*( DOT delete_call )?* /
    ;
    */

call
@init {
  is_call = False
}
@after {
  if not is_call:
    ref = $i.parts
    found = None
    if len(ref) > 1:
      found = $g::database.find(ref, OracleObject, False)

    if not found:
      name = $expression_ctx::ctx_name
      name_parts = []
      if name.schema:
        name_parts.append(name.schema)
      name_parts.append(name.obj)
      name_parts.extend(ref)
      found = $g::database.find(name_parts, OracleObject)

    if found:
      $expression::refs.add(found)
}
    : /* COLON? sqlplus vars */
      i=part_identifier
      ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN { is_call = True }
        ( DOT call )? )?
    ;

attribute
    : kBULK_ROWCOUNT LPAREN expression RPAREN
    | kFOUND
    | kISOPEN
    | kNOTFOUND
    | kROWCOUNT
    ;

call_args
    : LPAREN ( parameter ( COMMA parameter )* )? RPAREN
    ;

boolean_atom
    : boolean_literal
    /*| collection_exists
    | conditional_predicate*/
    ;

numeric_atom
    : numeric_literal
    ;

numeric_literal
    : T_INTEGER
    | REAL_NUMBER
    ;

boolean_literal
    : kTRUE
    | kFALSE
    ;

string_literal
    : QUOTED_STRING
    ;

/*
collection_exists
    : ID DOT EXISTS LPAREN expression RPAREN
    ;

conditional_predicate
    : INSERTING
    | UPDATING ( LPAREN QUOTED_STRING RPAREN )?
    | DELETING
    ;
    */

parameter
    : ( ID ARROW )? expression
    ;

/*
index
    : expression
    ;
    */

/*
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
*/

//kERRORS : { len(self.input.LT(1).text) >= 3 and "errors".startswith(self.input.LT(1).text.lower())}? ID;
//kEXCEPTIONS : {self.input.LT(1).text.lower() == "exceptions"}? ID;
kFOUND : {self.input.LT(1).text.lower() == "found"}? ID;
//kINDICES : {self.input.LT(1).text.lower() == "indices"}? ID;
kMOD : {self.input.LT(1).text.lower() == "mod"}? ID;
//kNAME : {self.input.LT(1).text.lower() == "name"}? ID;
//kOF : {self.input.LT(1).text.lower() == "of"}? ID;
kROWCOUNT : {self.input.LT(1).text.lower() == "rowcount"}? ID;
//kSAVE : {self.input.LT(1).text.lower() == "save"}? ID;
//kSHOW : {self.input.LT(1).text.lower() == "show"}? ID;


kALWAYS : {self.input.LT(1).text.lower() == 'always'}? ID;
kBFILE : {self.input.LT(1).text.lower() == 'bfile'}? ID;
kBINARY_DOUBLE : {self.input.LT(1).text.lower() == 'binary_double'}? ID;
kBINARY_FLOAT : {self.input.LT(1).text.lower() == 'binary_float'}? ID;
kBITMAP : {self.input.LT(1).text.lower() == 'bitmap'}? ID;
kBLOB : {self.input.LT(1).text.lower() == 'blob'}? ID;
kBODY : {self.input.LT(1).text.lower() == 'body'}? ID;
kBULK_ROWCOUNT : {self.input.LT(1).text.lower() == 'bulk_rowcount'}? ID;
kBYTE : {self.input.LT(1).text.lower() == 'byte'}? ID;
kCACHE : {self.input.LT(1).text.lower() == 'cache'}? ID;
kCASCADE : {self.input.LT(1).text.lower() == 'cascade'}? ID;
kCLOB : {self.input.LT(1).text.lower() == 'clob'}? ID;
kCONSTRAINT : {self.input.LT(1).text.lower() == 'constraint'}? ID;
kCYCLE : {self.input.LT(1).text.lower() == 'cycle'}? ID;
kDAY : {self.input.LT(1).text.lower() == 'day'}? ID;
kDELETING : {self.input.LT(1).text.lower() == 'deleting'}? ID;
kDISABLE : {self.input.LT(1).text.lower() == 'disable'}? ID;
kENABLE : {self.input.LT(1).text.lower() == 'enable'}? ID;
kFALSE : {self.input.LT(1).text.lower() == 'false'}? ID;
kFOREIGN : {self.input.LT(1).text.lower() == 'foreign'}? ID;
kFUNCTION : {self.input.LT(1).text.lower() == 'function'}? ID;
kGENERATED : {self.input.LT(1).text.lower() == 'generated'}? ID;
kINSERTING : {self.input.LT(1).text.lower() == 'inserting'}? ID;
kINTERVAL : {self.input.LT(1).text.lower() == 'interval'}? ID;
kISOPEN : {self.input.LT(1).text.lower() == 'isopen'}? ID;
kKEY : {self.input.LT(1).text.lower() == 'key'}? ID;
kLOCAL : {self.input.LT(1).text.lower() == 'local'}? ID;
kMAXVALUE : {self.input.LT(1).text.lower() == 'maxvalue'}? ID;
kMINVALUE : {self.input.LT(1).text.lower() == 'minvalue'}? ID;
kMONTH : {self.input.LT(1).text.lower() == 'month'}? ID;
kNCHAR : {self.input.LT(1).text.lower() == 'nchar'}? ID;
kNCLOB : {self.input.LT(1).text.lower() == 'nclob'}? ID;
kNOCACHE : {self.input.LT(1).text.lower() == 'nocache'}? ID;
kNOCYCLE : {self.input.LT(1).text.lower() == 'nocycle'}? ID;
kNOMAXVALUE : {self.input.LT(1).text.lower() == 'nomaxvalue'}? ID;
kNOMINVALUE : {self.input.LT(1).text.lower() == 'nominvalue'}? ID;
kNOORDER : {self.input.LT(1).text.lower() == 'noorder'}? ID;
kNOTFOUND : {self.input.LT(1).text.lower() == 'notfound'}? ID;
kNVARCHAR2 : {self.input.LT(1).text.lower() == 'nvarchar2'}? ID;
kPACKAGE : {self.input.LT(1).text.lower() == 'package'}? ID;
kPRIMARY : {self.input.LT(1).text.lower() == 'primary'}? ID;
kQUIT : {self.input.LT(1).text.lower() == 'quit' and self.aloneOnLine()}? ID;
kREFERENCES : {self.input.LT(1).text.lower() == 'references'}? ID;
kREPLACE : {self.input.LT(1).text.lower() == 'replace'}? ID;
kSECOND : {self.input.LT(1).text.lower() == 'second'}? ID;
kSEQUENCE : {self.input.LT(1).text.lower() == 'sequence'}? ID;
kTABLESPACE : {self.input.LT(1).text.lower() == 'tablespace'}? ID;
kTIME : {self.input.LT(1).text.lower() == 'time'}? ID;
kTIMESTAMP : {self.input.LT(1).text.lower() == 'timestamp'}? ID;
kTRUE : {self.input.LT(1).text.lower() == 'true'}? ID;
kTYPE : {self.input.LT(1).text.lower() == 'type'}? ID;
kUPDATING : {self.input.LT(1).text.lower() == 'updating'}? ID;
kURITYPE : {self.input.LT(1).text.lower() == 'uritype'}? ID;
kUROWID : {self.input.LT(1).text.lower() == 'urowid'}? ID;
kUSING : {self.input.LT(1).text.lower() == 'using'}? ID;
kVIRTUAL : {self.input.LT(1).text.lower() == 'virtual'}? ID;
kXMLTYPE : {self.input.LT(1).text.lower() == 'xmltype'}? ID;
kYEAR : {self.input.LT(1).text.lower() == 'year'}? ID;
kZONE : {self.input.LT(1).text.lower() == 'zone'}? ID;
// kXYZZY : {self.input.LT(1).text.lower() == 'xyzzy'}? ID;

/*
swallow_to_semi
  : ~( SEMI )+
  ;
  */

swallow_to_nl
  : ~( NL )+
  ;

tINTEGER returns [val]
  : i=T_INTEGER { $val = int($i.text) }
  ;


/*
    PL/SQL Reserved words
*/

//kWHEN	:	{self.input.LT(1).text.lower() == 'when'}? ID;

/*
    Keywords
*/
ACCESS : 'access';
ADD : 'add';
ALL : 'all';
ALTER : 'alter';
AND : 'and';
ANY : 'any';
AS : 'as';
ASC : 'asc';
AT : 'at';
AUDIT : 'audit';
BEGIN : 'begin';
BETWEEN : 'between';
BY : 'by';
CASE : 'case';
CHAR : 'char';
CHECK : 'check';
CLUSTER : 'cluster';
CLUSTERS : 'clusters';
COLAUTH : 'colauth';
COLUMN : 'column';
COLUMNS : 'columns';
COMMENT : 'comment';
COMPRESS : 'compress';
CONNECT : 'connect';
CRASH : 'crash';
CREATE : 'create';
CURRENT : 'current';
DATE : 'date';
DECIMAL : 'decimal';
DECLARE : 'declare';
DEFAULT : 'default';
DELETE : 'delete';
DESC : 'desc';
DISTINCT : 'distinct';
DROP : 'drop';
ELSE : 'else';
END : 'end';
EXCEPTION : 'exception';
EXCLUSIVE : 'exclusive';
EXISTS : 'exists';
FETCH : 'fetch';
FILE : 'file';
FLOAT : 'float';
FOR : 'for';
FROM : 'from';
GOTO : 'goto';
GRANT : 'grant';
GROUP : 'group';
HAVING : 'having';
IDENTIFIED : 'identified';
IF : 'if';
IMMEDIATE : 'immediate';
IN : 'in';
INCREMENT : 'increment';
INDEX : 'index';
INDEXES : 'indexes';
INITIAL : 'initial';
INSERT : 'insert';
INTEGER : 'integer';
INTERSECT : 'intersect';
INTO : 'into';
IS : 'is';
LEVEL : 'level';
LIKE : 'like';
LOCK : 'lock';
LONG : 'long';
MAXEXTENTS : 'maxextents';
MINUS : 'minus';
MLSLABEL : 'mlslabel';
MODE : 'mode';
MODIFY : 'modify';
NOAUDIT : 'noaudit';
NOCOMPRESS : 'nocompress';
NOT : 'not';
NOWAIT : 'nowait';
NULL : 'null';
NUMBER : 'number';
OF : 'of';
OFFLINE : 'offline';
ON : 'on';
ONLINE : 'online';
OPTION : 'option';
OR : 'or';
ORDER : 'order';
OVERLAPS : 'overlaps';
PCTFREE : 'pctfree';
PRIOR : 'prior';
PRIVILEGES : 'privileges';
PROCEDURE : 'procedure';
PUBLIC : 'public';
RAW : 'raw';
RENAME : 'rename';
RESOURCE : 'resource';
REVOKE : 'revoke';
ROW : 'row';
ROWID : 'rowid';
ROWNUM : 'rownum';
ROWS : 'rows';
SELECT : 'select';
SESSION : 'session';
SET : 'set';
SHARE : 'share';
SIZE : 'size';
SMALLINT : 'smallint';
SQL : 'sql';
START : 'start';
SUCCESSFUL : 'successful';
SYNONYM : 'synonym';
SYSDATE : 'sysdate';
TABAUTH : 'tabauth';
TABLE : 'table';
THEN : 'then';
TO : 'to';
TRIGGER : 'trigger';
UID : 'uid';
UNION : 'union';
UNIQUE : 'unique';
UPDATE : 'update';
USER : 'user';
VALIDATE : 'validate';
VALUES : 'values';
VARCHAR : 'varchar';
VARCHAR2 : 'varchar2';
VIEW : 'view';
VIEWS : 'views';
WHEN : 'when';
WHENEVER : 'whenever';
WHERE : 'where';
WITH : 'with';


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
BANG
  : '!'
  ;
AT_SIGN
	:	'@'
	;
DOUBLE_AT_SIGN
	:	'@@'
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
HYPHEN
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
T_INTEGER
    :   N
    ;
REAL_NUMBER
	:	NUMBER_VALUE	( 'e' ( PLUS | HYPHEN )? N )?
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
