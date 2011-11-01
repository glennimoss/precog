import logging
from antlr3.ext import (NL_CHANNEL, InputStream, FileStream,
                        MultiChannelTokenStream, NamedConstant, StringStream,
                        ValueNode)
from antlr3 import EOF
from antlr3.constants import HIDDEN_CHANNEL
from antlr3.recognizers import Lexer, Parser
from antlr3.streams import TokenStream


from precog.errors import SqlSyntaxError
from precog import reserved
from precog.util import HasLog
#import logging

__all__ = ['aloneOnLine', 'LoggingLexer', 'LoggingParser', 'SqlPlusFileParser',
           'string_parser', 'Expression']

def aloneOnLine (LT):
  #log = logging.getLogger('precog.parser.util.aloneOnLine')
  def _aloneOnLine (dir=None):
    if not dir:
      #log.debug('Starting at token: %s', repr(LT(1)))
      return _aloneOnLine(-1) and _aloneOnLine(1)

    #log.debug("Alone on line: %d", dir)
    # A terminator can only occur on a line by itself, possibly with whitespace
    p = 1 if dir == 1 else 0
    c = 0
    while c != EOF:
      p += dir
      c = LT(p)
      #log.debug('At: %s saw: %s', p, repr(c))
      if c == '\n':
        return True
      if c not in (' ', '\t', '\r'):
        return False

    # EOF is as good as a line terminator
    return True
  return _aloneOnLine

class LoggingRecognizer (HasLog):
  def displayRecognitionError(self, token_names, error):
    self.logSyntaxError(self.getErrorMessage(error, token_names), error.input,
        error.index, error.line, error.charPositionInLine)

  def logSyntaxError (self, message, input, index, line, column):
    self._log_syntax(message, input, index, line, column, self.log.error)

  def logSyntaxWarning (self):
    self._log_syntax(message, input, index, line, column, self.log.warn)

  def _log_syntax (self, message, input, index, line, column, logger):
    token_stream = isinstance(input, TokenStream)
    if token_stream:
      from precog.parser.sqlParser import NL
      test = lambda t: t is None or t.type in (NL, EOF)
      input.add(NL_CHANNEL, HIDDEN_CHANNEL)
    else:
      test = lambda t: t in (EOF, '\n')

    input.mark()
    input.seek(index)

    def find (dir):
      p = dir
      while True:
        this_token = input.LT(p)
        if test(this_token):
          break;
        p += dir
      return p

    start_token = find(-1) + index
    if start_token < 0:
      start_token = 0
    end_token = find(1) + index - 1
    input.rewind()

    if token_stream:
      input.drop(NL_CHANNEL, HIDDEN_CHANNEL)
      get_line = input.toString
    else:
      get_line = input.substring

    line_text = get_line(start_token, end_token).strip('\n')

    logger(SqlSyntaxError(message, 'File "{}"'.format(input.getSourceName()),
      line, column, line_text))

class LoggingLexer (LoggingRecognizer, Lexer):
  pass

class LoggingParser (LoggingRecognizer, Parser):
  pass

class SqlPlusFileParser (HasLog):

  def __init__ (self):
    super().__init__()
    from precog.parser.sqlLexer import sqlLexer
    from precog.parser.sqlParser import sqlParser
    self.parser = sqlParser(MultiChannelTokenStream(sqlLexer()))

  def parse (self, filename, database):
    parse_queue = [filename]
    num_errors = 0
    for file in parse_queue:
      stream = FileStream
      if not isinstance(file, str):
        stream = InputStream

      token_stream = self.parser.input
      lexer = token_stream.tokenSource
      lexer.setCharStream(stream(file))
      token_stream.setTokenSource(lexer)
      self.parser.setTokenStream(token_stream)

      self.log.info("Parsing file {}".format(self.parser.getSourceName()))
      includes = self.parser.sqlplus_file(database).included_files
      parse_queue.extend(includes)
      num_errors += self.parser.getNumberOfSyntaxErrors()

    if num_errors:
      raise ParseError(num_errors)

def string_parser (string):
  from precog.parser.sqlLexer import sqlLexer
  from precog.parser.sqlParser import sqlParser
  lexer = sqlLexer(StringStream(string))
  tokenStream = MultiChannelTokenStream(lexer)
  parser = sqlParser(tokenStream)
  return parser

class Expression (object):

  def __init__ (self, text, tree=None, scope_obj=None, database=None):
    self.text = text.strip()
    self._tree = tree
    self.scope_obj = scope_obj
    self.database = database

  @property
  def tree (self):
    if not self._tree and self.text and self.scope_obj and self.database:
      self._tree = string_parser(self.text).parse_expression(
        self.scope_obj.name, self.database).tree
    return self._tree

  @property
  def references (self):
    from precog.parser.sqlParser import CALL
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
      references.add(self.database.find(parts))

    return references

  def __eq__ (self, other):
    if self.tree and hasattr(other, 'tree') and other.tree:
      return self.tree == other.tree
    return str(self) == str(other)

  def __str__ (self):
    return self.text

  def __repr__ (self):
    return "Expression({!r}, <{}>)".format(self.text, self.tree and
                                           self.tree.pretty_print())

  def __getstate__ (self):
    state = self.__dict__.copy()
    del state['_tree']
    return state

