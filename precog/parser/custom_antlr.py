from antlr3 import CommonTokenStream
from antlr3.constants import DEFAULT_CHANNEL

class MultiChannelTokenStream (CommonTokenStream):

  def __init__(self, tokenSource=None, channel=DEFAULT_CHANNEL):
    super().__init__(tokenSource, channel)

    self._channels = { channel }


  def add (self, *channels):
    # there may be tokens we wanted to see between the last on-channel token and
    # the ones we're now looking for. First, go back, then add the new channel
    # and move to the next on-channel token.
    self.p = self.skipOffTokenChannelsReverse(self.p - 1)
    self._channels.update(channels)
    self.consume()

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
