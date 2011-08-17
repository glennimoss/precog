from antlr3.constants import DEFAULT_CHANNEL, EOF
from antlr3 import exceptions
from antlr3.streams import (CommonTokenStream, StringStream, FileStream,
  InputStream)

NL_CHANNEL = DEFAULT_CHANNEL + 1

class IterableTokenStream(CommonTokenStream):

  def __iter__ (self):
    return self

  def __next__ (self):
    c = self.LT(1)
    if c.type == EOF:
      raise StopIteration
    self.consume()
    return c

class MultiChannelTokenStream (IterableTokenStream):

  def __init__(self, tokenSource=None, channel=DEFAULT_CHANNEL):
    super().__init__(tokenSource, channel)

    self._channels = { channel }


  def add (self, *channels):
    # there may be tokens we wanted to see between the last on-channel token and
    # the ones we're now looking for. First, go back, then add the new channel
    # and move to the next on-channel token.
    # Maybe we don't want to do that... :P
    #self.p = self.skipOffTokenChannelsReverse(self.p - 1)
    self._channels.update(channels)
    #self.consume()

  def drop (self, *channels):
    self._channels.difference_update(channels)
    # We may be resting on a now off-channel token. Just skip anything no longer
    # on-channel. (Maybe nothing)
    self.p = self.skipOffTokenChannels(self.p)

  def skipOffTokenChannels(self, i):
    """
    Given a starting index, return the index of the first on-channel
    token.
    """

    try:
        while self.tokens[i].channel not in self._channels:
            i += 1
    except IndexError:
        # hit the end of token stream
        pass

    return i


  def skipOffTokenChannelsReverse(self, i):
    while i >= 0 and self.tokens[i].channel not in self._channels:
        i -= 1

    return i

class InsensitiveStringStream (StringStream):

  def LA(self, i):
    if i == 0:
      return 0 # undefined

    if i < 0:
      i += 1 # e.g., translate LA(-1) to use offset i=0; then data[p+0-1]

    try:
      return ord(chr(self.data[self.p+i-1]).lower())
    except IndexError:
      return EOF



  def LT(self, i):
    if i == 0:
      return 0 # undefined

    if i < 0:
      i += 1 # e.g., translate LA(-1) to use offset i=0; then data[p+0-1]

    try:
      return self.strdata[self.p+i-1].lower()
    except IndexError:
      return EOF

class InsensitiveFileStream (FileStream, InsensitiveStringStream):
  pass

class InsensitiveInputStream (InputStream, InsensitiveStringStream):
  pass

StringStream = InsensitiveStringStream
FileStream = InsensitiveFileStream
InputStream = InsensitiveInputStream

class NamedConstant (int):
  """Augment constant numbers with printable names"""
  def __new__ (self, id, text):
    return super().__new__(self, id)

  def __init__ (self, id, text):
    self._text = text

  def __str__ (self):
    return self._text

  def __repr__ (self):
    return "<{} {}>".format(self._text, int(self))

  @staticmethod
  def name (vars):
    for name, value in vars.items():
      if isinstance(value, int) and name.isupper():
        vars[name] = NamedConstant(value, name)
