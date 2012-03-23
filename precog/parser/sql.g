/*
Oracle SQL parser.

Originally based on a grammar by Patrick Higgins
*/

grammar sql;

options {
  language=Python;
  superClass=LoggingParser;
  output=AST;
}

tokens {
  CALL;
}

scope g { database ; var_dict }

scope tab_col_ref { alias_map; table; columns }

@lexer::header {
  from antlr3.ext import NamedConstant, FileStream, NL_CHANNEL
  from precog.parser.util import *

  # Monkey patch in our lexer superclass
  Lexer = LoggingLexer
}
@parser::header {
  import os

  from antlr3.exceptions import RecognitionException
  from antlr3.ext import (NamedConstant, FileStream, NL_CHANNEL, ValueNode,
                          CommonTreeAdaptor)
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

  def get_location (self):
    return (self.getSourceName(), self.input.LT(1).line)
}
@lexer::main {
  NamedConstant.name(locals())

  def main(argv):
    from antlr3.ext import IterableTokenStream

    #from antlr3.ext import MultiChannelTokenStream
    inStream = FileStream(argv[1])
    lexer = sqlLexer(inStream)
    tokenStream = IterableTokenStream(lexer)
    for t in tokenStream:
      print(t)
}

sqlplus_file[database] returns [included_files]
scope { included_files_ ; next_obj_props ; create_location }
scope g;
@init {
  $g::database = $database
  $sqlplus_file::included_files_ = []
  $sqlplus_file::next_obj_props = InsensitiveDict()
}
@after {
  $included_files = $sqlplus_file::included_files_
}
    : ( {
          $sqlplus_file::create_location = self.get_location()
        }
        ( stmt=sql_stmt
        | stmt=plsql_stmt
        ) {
            if $stmt.obj:
              $stmt.obj.create_location = $sqlplus_file::create_location
              $stmt.obj.props.update($sqlplus_file::next_obj_props)
              $g::database.add($stmt.obj)
            $sqlplus_file::next_obj_props = InsensitiveDict()
          }
        | directive_stmt
        | (~( CREATE | INSERT | DIRECTIVE ))=> sqlplus_stmt
      )* EOF
    ;

plsql_stmt returns [obj]
scope { type; name; props }
@init {
  $plsql_stmt::props = InsensitiveDict()
}
@after {
  $obj = $plsql_stmt::type($plsql_stmt::name, source=$source.text,
                           database=$g::database, **$plsql_stmt::props)
}
  : CREATE (OR kREPLACE)? source=plsql_object_def
    TERMINATOR
  ;

sql_stmt returns [obj]
  : ( stmt_=create_table { $obj = $stmt_.obj }
    | stmt_=create_index { $obj = $stmt_.obj }
    | stmt_=create_sequence { $obj = $stmt_.obj }
    | stmt_=create_synonym { $obj = $stmt_.obj }
    | insert_statement
    ) SEMI
  ;

sqlplus_stmt returns [stmt]
  : { self.input.add(NL_CHANNEL) }

    ( (AT_SIGN | DOUBLE_AT_SIGN)
      file_name=swallow_to_nl NL
      // At one time we had the single @ as non-relative and @@ as relative
      // but really who ever wants it to be non-relative? It's annoying to have
      // to change files already using single @s.
      {
        file_name = $file_name.text
        relative_dir = os.path.dirname(self.input.getSourceName())

        file_name = ''.join((relative_dir,
                             os.sep if relative_dir else '',
                             file_name))

        $sqlplus_file::included_files_.append(file_name)
        $g::database.came_from_file(file_name, 'include')
      }
    | (~( AT_SIGN | DOUBLE_AT_SIGN ))=> command=swallow_to_nl NL
    )
  ;
finally {
  self.input.drop(NL_CHANNEL)
}

directive_stmt
  : { self.input.add(NL_CHANNEL) }
    DIRECTIVE
    ( directive_ignore
    | directive_option
    )
    NL
  ;
finally {
  self.input.drop(NL_CHANNEL)
}

directive_ignore
@init {
  schema = False
}
  : kIGNORE (kSCHEMA { schema = True })? i=identifier {
      name = $i.ident
      if schema:
        $g::database.ignore_schema(name.obj)
      else:
        $g::database.ignore(name)
    }
  ;

directive_option
  : OPTION o=ID {
      $sqlplus_file::next_obj_props[$o.text] = True
    }
  ;

identifier returns [ident]
  : first=tID ( DOT second=tID ( DOT third=tID )? )?
    // TODO: this should probably check for schemas to determine if it's
    // schema.obj or obj.part
    {
      schema = $first.id if $second.id else None
      obj = $second.id if $second.id else $first.id
      part = $third.id if $third.id else None
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
@init {
  $create_table::props = InsensitiveDict({'columns': [], 'constraints': set()})
}
@after {
  $obj = Table($ident.ident, database=$g::database, **$create_table::props)
}
  : CREATE TABLE ident=identifier {
      $create_table::table_name = $ident.ident
    }
    LPAREN
      table_item (COMMA table_item)*
    RPAREN
    ( kTABLESPACE ID
      { $create_table::props['tablespace_name'] = $ID.text }
    )?
  ;

table_item
  : col=col_spec { $create_table::props['columns'].append($col.column) }
  | cons=out_of_line_constraint {
      $create_table::props['constraints'].add($cons.constraint)
    }
  ;

col_spec returns [column]
scope { column_ }
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  $tab_col_ref::table = $create_table::table_name
  props = InsensitiveDict()
  constraints = set()
  props['nullable'] = 'Y'
  create_location = self.get_location()
}
@after {
  $column = $col_spec::column_
}
  : i=tID
    ( dt=data_type[True] { props.update($dt.props) }
      ( DEFAULT e=expression
        { props['data_default'] = $e.exp.text } )?
    | ( kGENERATED kALWAYS )? AS LPAREN virt=expression RPAREN kVIRTUAL? {
        props['virtual_column'] = 'YES'
        props['expression'] = $virt.exp
      }
    )
    {
      $col_spec::column_ = $g::database.add(
        Column($create_table::table_name.with_(part=$i.id),
               database=$g::database, create_location=create_location, **props))
    }
    ( NOT? NULL { $col_spec::column_.props['nullable'] = 'N' if $NOT else 'Y' }
    | ic=inline_constraint {
        if $ic.cons:
          constraints.add($ic.cons)
      }
    )*
    { $col_spec::column_.constraints = constraints }
  ;

data_type[sized] returns [props]
scope { props_ }
@init {
  $data_type::props_ = InsensitiveDict()
}
@after {
  $props = $data_type::props_
}
  : string_data_type[$sized]
  | numeric_data_type[$sized]
  | long_raw_data_type[$sized]
  | datetime_data_type[$sized]
  | lob_data_type
  | rowid_data_type[$sized]
  | oracle_data_type
  | user_data_type
  ;

int_parameter returns [val]
  : LPAREN i=tINTEGER RPAREN { $val = $i.val }
  ;

string_data_type[sized]
  : (t=CHAR | t=VARCHAR2) { $data_type::props_['data_type'] = $t.text.upper() }
    ( {$sized}? LPAREN
      l=tINTEGER { $data_type::props_['char_length'] = $l.val }
      ( kBYTE { $data_type::props_['char_used'] = 'B' }
      | CHAR { $data_type::props_['char_used'] = 'C' }
      )?
      RPAREN
    | {not $sized}? // nothing
    )
  | (nt=kNCHAR | nt=kNVARCHAR2) {
      $data_type::props_['data_type'] = $nt.text.upper()
    }
    ( {$sized}? l=int_parameter { $data_type::props_['char_length'] = $l.val }
    | {not $sized}? // nothing
    )
  ;

numeric_data_type[sized]
  : ( t=NUMBER ({$sized}? number_precision)?
    | t=FLOAT ({$sized}? p=int_parameter
               { $data_type::props_['data_precision'] = $p.val })?
    | k1=kBINARY_FLOAT
    | k2=kBINARY_DOUBLE
    ) {
      $data_type::props_['data_type'] = (($t and $t.text) or
                                         $k1.text or $k2.text).upper()
    }
  | INTEGER {
      $data_type::props_['data_type'] = 'NUMBER'
      $data_type::props_['data_scale'] = 0
    }
  ;

number_precision
  : LPAREN
     ( precision=tINTEGER
       { $data_type::props_['data_precision'] = $precision.val }
       (COMMA neg=HYPHEN? scale=tINTEGER)?
     | ASTERISK COMMA neg=HYPHEN? scale=tINTEGER
     )
     {
       if $scale.val:
         $data_type::props_['data_scale'] = $scale.val * (-1 if $neg else 1)
     }
    RPAREN
  ;

long_raw_data_type[sized]
@after {
  $data_type::props_['data_type'] = OracleIdentifier(
    ' '.join(w.text.upper() for w in $t), True)
}
  : t+=LONG t+=RAW?
  | t+=RAW ({$sized}? i=int_parameter
            { $data_type::props_['data_length'] = $i.val }
           | {not $sized}? //nothing
           )
  ;

datetime_data_type[sized]
  : DATE
    { $data_type::props_['data_type'] = 'DATE' }
  | kTIMESTAMP ({$sized}? i=int_parameter)? (t=WITH l=kLOCAL? kTIME kZONE)?
    {
      $data_type::props_['data_type'] = "TIMESTAMP({}){}".format(
        $i.val or 6,
        " WITH {}TIME ZONE".format('LOCAL ' if $l.text else '')
          if $t else '')
    }
  | kINTERVAL
    ( kYEAR ({$sized}? i=int_parameter)? TO kMONTH
    {
      $data_type::props_['data_type'] = "INTERVAL YEAR({}) TO MONTH".format(
        $i.val or 2)
    }
    | kDAY ({$sized}? d=int_parameter)? TO kSECOND ({$sized}? s=int_parameter)?
    {
      $data_type::props_['data_type'] = "INTERVAL DAY({}) TO SECOND({})".format(
        $d.val or 2, $s.val or 6)
    }
    )
  ;

lob_data_type
@after {
  $data_type::props_['data_type'] = ($t1.text or $t2.text or $t3.text or
                                   $t4.text).upper()
}
  : t1=kBLOB
  | t2=kCLOB
  | t3=kNCLOB
  | t4=kBFILE
  ;

rowid_data_type[sized]
@after {
  $data_type::props_['data_type'] = (($t and $t.text) or $k.text).upper()
}
  : t=ROWID
  | k=kUROWID ({$sized}? i=int_parameter
               { $data_type::props_['data_length'] = $i.val })?
  ;

oracle_data_type
@after { $data_type::props_['data_type'] = ($t1.text or $t2.text).upper() }
  : t1=kXMLTYPE
  | t2=kURITYPE
  ;

user_data_type
  : i=identifier {
      user_type = $g::database.find($i.ident, Type)
      $data_type::props_['user_type'] = user_type
    }
  ;

inline_constraint returns [cons]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  $tab_col_ref::table = $create_table::table_name
  cons_class = None
  props = InsensitiveDict()
  index = None
  create_location = self.get_location()
}
@after {
  if cons_class:
    $cons = $g::database.add(cons_class($constraint_name.id,
                                        columns=[$col_spec::column_],
                                        database=$g::database,
                                        create_location=create_location,
                                        **props))
  else:
    $cons = None
}
  : ( kCONSTRAINT constraint_name=tID // Non-spec: making required
    | {
        token = self.input.LT(1)
        self.logSyntaxError('"CONSTRAINT [constraint_name]" is required.',
                            self.input, token.index, token.line,
                            token.charPositionInLine)
        constraint_name = self.tID_return()
        constraint_name.id = GeneratedId()
      }
    )
    ( ( UNIQUE { props['is_pk'] = False }
      | kPRIMARY kKEY { props['is_pk'] = True }
      ) {
        cons_class = UniqueConstraint
        index_props = InsensitiveDict()
        props['index_ownership'] = UniqueConstraint.IMPLICIT_INDEX_CREATE
      }
      using_index[$constraint_name.id] {
        props.update($using_index.props)
      }
    | ref=references_clause {
        props.update($ref.props)
        cons_class = ForeignKeyConstraint
      }
    | CHECK LPAREN check_exp=expression RPAREN {
        props['expression'] = $check_exp.exp
        cons_class = CheckConstraint
      }
    )
    { props['is_enabled'] = True }
    ( kENABLE
    | kDISABLE { props['is_enabled'] = False } )?
  ;

references_clause returns [props]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  $props = InsensitiveDict({'delete_rule': 'NO ACTION'})
}
@after {
  $props['fk_constraint'] = $g::database.find_unique_constraint(
    $tab_col_ref::columns)
}
  : kREFERENCES ref=identifier { $tab_col_ref::table = $ref.ident }
    LPAREN column_ref (COMMA column_ref)* RPAREN // Non-spec: making required
    (ON DELETE ( kCASCADE { $props['delete_rule'] = 'CASCADE' }
               | SET NULL { $props['delete_rule'] = 'SET NULL' } ) )?
  ;

out_of_line_constraint returns [constraint]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  $tab_col_ref::table = $create_table::table_name
  props = InsensitiveDict()
  cons_class = Constraint
  index_props = InsensitiveDict()
  index = None
  create_location = self.get_location()
}
@after {
  $constraint = $g::database.add(cons_class($constraint_name.id,
                                            database=$g::database,
                                            create_location=create_location,
                                            **props))
}
  : kCONSTRAINT constraint_name=tID // Non-spec: making required
    ( ( ( UNIQUE { props['is_pk'] = False }
        | kPRIMARY kKEY { props['is_pk'] = True } )
        {
          cons_class = UniqueConstraint
          props['index_ownership'] = UniqueConstraint.IMPLICIT_INDEX_CREATE
        }
      | kFOREIGN kKEY
        { cons_class = ForeignKeyConstraint }
      )
      LPAREN
        column_ref (COMMA column_ref)*
      RPAREN
      { props['columns'] = $tab_col_ref::columns }
      ( { cons_class is ForeignKeyConstraint }? ref=references_clause {
          props.update($ref.props)
          cons_class = ForeignKeyConstraint
        }
      | { cons_class is UniqueConstraint }?
        using_index[$constraint_name.id] {
          props.update($using_index.props)
        }
      | // Nothing
      )
    | CHECK LPAREN check_exp=expression RPAREN {
        props['expression'] = $check_exp.exp
        props['columns'] = [col for col in $check_exp.exp.references
                            if isinstance(col, Column)]
        cons_class = CheckConstraint
      }
    )
    ( kENABLE { props['is_enabled'] = True }
    | kDISABLE { props['is_enabled'] = False } )?
  ;

column_ref
  : ( ID (COMMA | RPAREN) )=> c=aliased_identifier {
      fqn = $c.ident
      if not isinstance(fqn, OracleFQN):
        fqn = OracleFQN($tab_col_ref::table.schema,
          $tab_col_ref::table.obj, $c.ident)

      $tab_col_ref::columns.append($g::database.find(fqn, Column))
    }
  | { create_location = self.get_location() }
    virt=expression {
    $tab_col_ref::columns.append($g::database.add(
      VirtualColumn($tab_col_ref::table.with_(part=GeneratedId()),
                    expression=$virt.exp, database=$g::database,
                    hidden_column='YES', create_location=create_location)))
  }
  ;

using_index [constraint_name] returns [props]
@init {
  $props = InsensitiveDict()
  index_props = InsensitiveDict()
  index_props['index_type'] = 'NORMAL'
  create_location = self.get_location()
}
@after {
  if not $props['index']:
    $props['index'] = $g::database.add(
      Index($constraint_name, unique=True, database=$g::database,
            create_location=create_location, **index_props))
}
  : kUSING INDEX
    { create_location = self.get_location() }
    ( index_name=identifier {
        $props['index'] = $g::database.find($index_name.ident, Index)
        $props['index_ownership'] = None
      }
    | LPAREN new_index=create_index RPAREN {
        $props['index'] = $g::database.add($new_index.obj)
        $props['index_ownership'] = UniqueConstraint.FULL_INDEX_CREATE
      }
    | attr=index_attributes {
        index_props.update($attr.props)
        $props['index_ownership'] = UniqueConstraint.SHORT_INDEX_CREATE
      }
    )
  | // Nothing
  ;

create_index returns [obj]
scope tab_col_ref;
@init {
  $tab_col_ref::columns = []
  props = InsensitiveDict()
  props['index_type'] = 'NORMAL'
  create_location = self.get_location()
}
@after {
  table = $g::database.find($tab_col_ref::table, Table)
  $obj = Index($index_name.ident, columns=$tab_col_ref::columns,
               database=$g::database, create_location=create_location, **props)
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
    (attr=index_attributes { props.update($attr.props) })?
  ;

index_attributes returns [props]
scope { props_ }
@init {
  $index_attributes::props_ = InsensitiveDict()
}
@after {
  $props = $index_attributes::props_
}
  // NOTE: Remember, we had to do this because there is a bug when using more
  // than one keyword ID token at the same level within a subrule where the
  // first one is always chosen by lookahead, and so all other alternatives
  // cause an error. By breaking out the subrule to its own rule, the code is
  // generated correctly, without the bug.
  : index_attribute+
  ;

index_attribute
  : kREVERSE { $index_attributes::props_['index_type'] = 'NORMAL/REV' }
  | kTABLESPACE ID { $index_attributes::props_['tablespace_name'] = $ID.text }
  ;

/*
tablespace_clause returns [ts_name]
  : kTABLESPACE ID { $ts_name = $ID.text }
  ;
  */

create_sequence returns [obj]
scope { props }
@init {
  $create_sequence::props = InsensitiveDict()
}
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
      $obj = Synonym($syn.ident, for_name=$target.ident, database=$g::database)
    }
  ;
insert_statement
scope { expressions; }
scope tab_col_ref;
@init {
  $insert_statement::expressions = []
  $tab_col_ref::columns = []
}
@after {
  data = table.add_data($tab_col_ref::columns, $insert_statement::expressions)
  $g::database.came_from_file(data)
}
  : INSERT INTO table_name=aliasing_identifier
    {
      $tab_col_ref::table = $table_name.ident
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

plsql_object_def
@init {
  $sqlplus_file::create_location = self.get_location()
}
  : plsql_function
  | plsql_procedure
  | plsql_trigger
  | plsql_package
  | plsql_package_body
  | plsql_type
  | plsql_type_body
  ;

plsql_function
  : FUNCTION { $plsql_stmt::type = Function }
    i=identifier { $plsql_stmt::name = $i.ident }
    (LPAREN ~RPAREN* RPAREN)?
    kRETURN data_type[False]
    kDETERMINISTIC?
    kPIPELINED?
    ( IS | AS )
    ( (~TERMINATOR)=> ~TERMINATOR )+
  ;

plsql_procedure
  : PROCEDURE { $plsql_stmt::type = Procedure }
    i=identifier { $plsql_stmt::name = $i.ident }
    (LPAREN ~RPAREN* RPAREN)?
    ( IS | AS )
    ( (~TERMINATOR)=> ~TERMINATOR )+
  ;

plsql_trigger
  : TRIGGER { $plsql_stmt::type = Trigger }
    i=identifier { $plsql_stmt::name = $i.ident }
    ( BEFORE | AFTER | INSTEAD | FOR )
    ( (~TERMINATOR)=> ~TERMINATOR )+
  ;

plsql_package
  : PACKAGE { $plsql_stmt::type = Package }
    i=identifier { $plsql_stmt::name = $i.ident }
    ( IS | AS )
    ( (~TERMINATOR)=> ~TERMINATOR )+
    /*( plsql_function | plsql_procedure )*
    END ID? SEMI*/
  ;

plsql_package_body
  : PACKAGE kBODY { $plsql_stmt::type = PackageBody }
    i=identifier { $plsql_stmt::name = $i.ident }
    ( IS | AS )
    ( (~TERMINATOR)=> ~TERMINATOR )+
    /* END ID? SEMI */
  ;

plsql_type
  : kTYPE { $plsql_stmt::type = Type }
    i=identifier { $plsql_stmt::name = $i.ident }
    ( IS | AS )
    ( plsql_type_object
    | plsql_type_collection
    ) SEMI?
  ;

plsql_type_object
  : kOBJECT
    ( (~TERMINATOR)=> ~TERMINATOR )+
  /*
    LPAREN
      plsql_type_object_attribute ( COMMA plsql_type_object_attribute )*
    RPAREN
    */
  ;

plsql_type_object_attribute
  : tID data_type[True]
  ;

plsql_type_collection
  : ( kVARRAY size=int_parameter {
        $plsql_stmt::props['collection_type'] = "VARRAY({})".format($size.val)
      }
    | TABLE {
        $plsql_stmt::props['collection_type'] = 'TABLE'
      }
    )
    OF dt=data_type[True] ( NOT NULL { $dt.props['nullable'] = 'N' } )?
    { $plsql_stmt::props.update($dt.props) }
  ;

plsql_type_body
  : kTYPE kBODY { $plsql_stmt::type = TypeBody }
    i=identifier { $plsql_stmt::name = $i.ident }
    ( IS | AS )
    ( (~TERMINATOR)=> ~TERMINATOR )+
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

parse_expression[table] returns [exp]
scope g, tab_col_ref;
@init {
  $g::database = $table.database
  $tab_col_ref::table = $table.name
}
@after {
  $exp = $e.exp
}
    : e=expression
    ;

expression returns [exp]
@after {
  table = $g::database.find($tab_col_ref::table, Table)
  $exp = Expression($e.text, tree=$e.tree, scope_obj=table)
}
    : e=expression_
    ;

expression_
    : or_expr
    ;

or_expr
    : and_expr ( OR^ and_expr )*
    ;

and_expr
    : not_expr ( AND^ not_expr )*
    ;

not_expr
    : NOT? compare_expr
    ;

compare_expr
    : is_null_expr ( ( EQ | NOT_EQ | LTH | LEQ | GTH | GEQ )^ is_null_expr )?
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
    : mul_expr ( ( HYPHEN | PLUS | DOUBLEVERTBAR )^ mul_expr )*
    ;

mul_expr
    : unary_sign_expr ( ( ASTERISK | SLASH )^ unary_sign_expr )*
    ;

unary_sign_expr
    : ( HYPHEN | PLUS )? exponent_expr
    ;

exponent_expr
    : atom ( EXPONENT^ atom )?
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
    | LPAREN! expression_ RPAREN!
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
    : /* COLON? sqlplus vars */
      i=part_identifier
      ( LPAREN ( parameter ( COMMA parameter )* )? RPAREN { is_call = True }
        ( DOT call )? )?
      -> { is_call }? ^( CALL {ValueNode($i.parts)} parameter* )
      -> {ValueNode($i.parts)}
    ;

attribute
    : kBULK_ROWCOUNT LPAREN expression_ RPAREN
    | kFOUND
    | kISOPEN
    | kNOTFOUND
    | kROWCOUNT
    ;

/*
call_args
    : LPAREN ( parameter ( COMMA parameter )* )? RPAREN
    ;
    */

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
    : ID DOT EXISTS LPAREN expression_ RPAREN
    ;

conditional_predicate
    : INSERTING
    | UPDATING ( LPAREN QUOTED_STRING RPAREN )?
    | DELETING
    ;
    */

parameter
    : ( ID ARROW )? expression_
    ;

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
//kMOD : {self.input.LT(1).text.lower() == "mod"}? ID;
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
kDETERMINISTIC : {self.input.LT(1).text.lower() == 'deterministic'}? ID;
kDISABLE : {self.input.LT(1).text.lower() == 'disable'}? ID;
kENABLE : {self.input.LT(1).text.lower() == 'enable'}? ID;
kFALSE : {self.input.LT(1).text.lower() == 'false'}? ID;
kFOREIGN : {self.input.LT(1).text.lower() == 'foreign'}? ID;
kGENERATED : {self.input.LT(1).text.lower() == 'generated'}? ID;
kIGNORE : {self.input.LT(1).text.lower() == 'ignore'}? ID;
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
kOBJECT : {self.input.LT(1).text.lower() == 'object'}? ID;
kPIPELINED : {self.input.LT(1).text.lower() == 'pipelined'}? ID;
kPRIMARY : {self.input.LT(1).text.lower() == 'primary'}? ID;
kREFERENCES : {self.input.LT(1).text.lower() == 'references'}? ID;
kREPLACE : {self.input.LT(1).text.lower() == 'replace'}? ID;
kRETURN : {self.input.LT(1).text.lower() == 'return'}? ID;
kREVERSE : {self.input.LT(1).text.lower() == 'reverse'}? ID;
kSCHEMA : {self.input.LT(1).text.lower() == 'schema'}? ID;
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
kVARRAY : {self.input.LT(1).text.lower() == 'varray'}? ID;
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
 * Not reserved but required to be tokens to relieve the parser's addled brain
 */
AFTER : 'after';
BEFORE : 'before';
FUNCTION : 'function';
INSTEAD : 'instead';
PACKAGE : 'package';

/*
 * PL/SQL Reserved words
 */
// None yet...

/*
 * Keywords
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
PLSQL_COMPILE_DIRECTIVE
  : '$' ID
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
fragment
AMPERSAND
  : '&'
  ;
CARET
  : '^'
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

DIRECTIVE
	:	'--@'
	;
NL : '\r'? '\n' { $channel=NL_CHANNEL } ;
SPACE	:	(' '|'\t') { $channel=HIDDEN } ;
SL_COMMENT
	:	{ self.input.LT(3) != '@' }?=> '--' ~('\n'|'\r')* { $channel=HIDDEN }
	;
ML_COMMENT
	:	'/*' ( options {greedy=false;} : . )* '*/' { $channel=HIDDEN }
	;
TERMINATOR
  : { self.aloneOnLine() }? SLASH
  ;
