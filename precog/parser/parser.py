from precog.antlr3.ext import (InputStream, FileStream, MultiChannelTokenStream,
                        StringStream, ValueNode)

from precog.errors import ParseError
from precog import reserved
from precog.util import HasLog

__all__ = ['SqlPlusFileParser', 'string_parser', 'Expression']

class SqlPlusFileParser (HasLog):

  def __init__ (self, parsed_files=None):
    super().__init__()
    from precog.parser.sqlLexer import sqlLexer
    from precog.parser.sqlParser import sqlParser
    self.parser = sqlParser(MultiChannelTokenStream(sqlLexer()))
    self.parsed_files = []
    if parsed_files:
      self.parsed_files.extend(parsed_files)

  def parse (self, filename, database):
    included_here = []
    parse_queue = [filename]
    num_errors = 0
    for file in parse_queue:
      if file not in self.parsed_files:
        stream = FileStream
        if not isinstance(file, str):
          stream = InputStream

        token_stream = self.parser.input
        lexer = token_stream.tokenSource
        lexer.setCharStream(stream(file))
        token_stream.setTokenSource(lexer)
        self.parser.setTokenStream(token_stream)

        self.log.info("Parsing file {}".format(self.source_file))
        includes = self.parser.sqlplus_file(database).included_files
        parse_queue.extend(includes)
        included_here.extend(includes)

        num_errors += self.parser.getNumberOfSyntaxErrors()

        self.parsed_files.append(self.source_file)

    if num_errors:
      raise ParseError(num_errors)
    return included_here

  @property
  def source_file (self):
    return self.parser.getSourceName()

def string_parser (string):
  from precog.parser.sqlLexer import sqlLexer
  from precog.parser.sqlParser import sqlParser
  lexer = sqlLexer(StringStream(string))
  tokenStream = MultiChannelTokenStream(lexer)
  parser = sqlParser(tokenStream)
  return parser

class Expression (object):

  def __init__ (self, text, tree=None, scope_obj=None):
    self.text = text.strip()
    self._tree = tree
    self.scope_obj = scope_obj

  @property
  def tree (self):
    if not self._tree and self.text and self.scope_obj:
      self._tree = string_parser(self.text).parse_expression(
        self.scope_obj).tree
    return self._tree

  @property
  def references (self):
    #from precog.parser.sqlParser import CALL
    references = set()
    names = []

    def find (node):
      if isinstance(node, ValueNode):
        names.append(node.value)
        return

      children = node.children
      # maybe treat calls differently because we know they're some kind of
      # function?
      #if node.token.type == CALL:
        #names.append(node.children[0].value, OracleObject)) #Function))
        #children = children[1:]

      for child in children:
        find(child)

    if self.tree:
      find(self.tree)

    for name in names:
      parts = name
      if len(parts) == 1:
        if parts[0] in reserved.functions:
          # ignore any built-in functions
          continue
        parts = [self.scope_obj.name.schema, self.scope_obj.name.obj]
        parts.extend(name)
      references.add(self.scope_obj.database.find(parts))

    return references

  def __eq__ (self, other):
    if self.tree and hasattr(other, 'tree') and other.tree:
      return self.tree == other.tree
    return str(self) == str(other)

  def __ne__ (self, other):
    return not self == other

  def __str__ (self):
    return self.text

  def __repr__ (self):
    return "Expression({!r}, <{}>)".format(self.text, self.tree and
                                           self.tree.pretty_print())

  def __getstate__ (self):
    state = self.__dict__.copy()
    state['_tree'] = None
    return state

