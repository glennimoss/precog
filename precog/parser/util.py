from antlr3.ext import NL_CHANNEL
from antlr3 import EOF
from antlr3.constants import HIDDEN_CHANNEL
from antlr3.recognizers import Lexer, Parser
from antlr3.streams import TokenStream

from precog.util import HasLog

__all__ = ['format_syntax_error', 'aloneOnLine', 'LoggingLexer',
           'LoggingParser']

def format_syntax_error (title, source_name, line, column, line_text,
                         explanation=''):
  return '{}\n  {}, line {}\n    {}\n    {}^{}'.format(
    title, source_name, line, line_text, ' '*(column),
    "\n{}".format(explanation) if explanation else '')

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

    logger(
      format_syntax_error(message, 'File "{}"'.format(input.getSourceName()),
                          line, column, line_text))

class LoggingLexer (LoggingRecognizer, Lexer):
  pass

class LoggingParser (LoggingRecognizer, Parser):
  pass

