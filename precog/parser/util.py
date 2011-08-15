from antlr3 import EOF
#import logging

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
      if not (c == ' ' or c == '\t'):
        return False

    # EOF is as good as a line terminator
    return True
  return _aloneOnLine
