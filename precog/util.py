from collections import OrderedDict
import logging, sys

class InsensitiveDict (OrderedDict):

  def __setitem__ (self, key, value):
    if isinstance(key, str):
      key = key.lower()

    super().__setitem__(key, value)

  def __getitem__ (self, key):
    if isinstance(key, str):
      key = key.lower()

    try:
      return super().__getitem__(key)
    except KeyError:
      return None

  def __delitem__ (self, key):
    if isinstance(key, str):
      key = key.lower()

    super().__delitem__(key)

  def __contains__ (self, key):
    if isinstance(key, str):
      key = key.lower()

    return super().__contains__(key)

def ValidatingList (validator):
  def validate_each (items):
    for i in items:
      validate(i)

  def validate (item):
    if not validator(item):
      raise ValidationError(item)

  class ValidatingList (list):
    def __init__ (self, init):
      validate_each(init)
      super().__init__(init)

    def __add__ (self, other):
      return MyList(super().__add__(other))

    def __iadd__ (self, other):
      validate_each(other)
      return super().__iadd__(other)

    def __setitem__ (self, i, other):
      validate(other)
      super().__setitem__(i, other)

    def append (self, other):
      validate(other)
      super().append(other)

    def extend (self, other):
      validate_each(other)
      super().extend(other)

    def insert (self, i, other):
      validate(other)
      super().insert(i, other)

  return ValidatingList

class ValidationError (Exception):

  def __init__ (self, invalid):
    self.invalid = invalid

  def __str__ (self):
    return "Item {!r} failed validation".format(self.invalid)

def coerced_comparison (class_):
  def coerced_method (m):
    def c_m (self, other):
      if not isinstance(other, class_):
        try:
          other = class_(other)
        except Exception:
          # Compare as-is if coercion isn't possible
          pass

      return m(self, other)

    c_m.__name__ = m.__name__
    return c_m

  for m_name in 'eq ne lt le gt ge cmp contains'.split():
    m_name = "__{}__".format(m_name)

    # Find the method that would be resolved
    for Sup in class_.__mro__:
      if m_name in Sup.__dict__:
        orig_m = getattr(Sup, m_name)
        break

    if not orig_m:
      continue

    coerced_m = coerced_method(orig_m)
    setattr(class_, m_name, coerced_m)

  return class_

class HasLog (object):
  """ Mixin for making a log named after the class """

  def __init__ (self, *args, **kwargs):
    self._log = None

    super().__init__(*args, **kwargs)

  @property
  def log (self):
    if not self._log:
      self._log = HasLog.log_for(self)
    return self._log

  def __getstate__ (self):
    state = self.__dict__.copy()
    del state['_log']
    return state

  @staticmethod
  def log_for (obj):
    id_ = ''
    if isinstance(obj, type):
      class_ = obj
    else:
      class_ = type(obj)
      id_ = ".{}".format(id(obj))

    return logging.getLogger(
        "{}.{}{}".format(class_.__module__, class_.__name__, id_))

class classproperty (object):

  def __init__ (self, getter):
    self.getter = getter

  def __get__ (self, obj, class_):
    return self.getter(class_)

def _progress (coll, output, message, start, count, complete):
  if count is None:
    count = len(coll)

  if callable(message):
    make_message = lambda o: message(o)
  else:
    make_message = lambda o: message

  if count: # avoid divide by zero
    itr = iter(coll)
    c = start
    obj = None
    while True:
      output(make_message(obj).format("{:03.0%}".format(c/count)), '\x1b[0K\r')
      try:
        obj = next(itr)
        step = yield obj
      except StopIteration:
        break
      if step is None:
        step = 1
      c += step

  if complete:
    output(make_message(None).format('100%'), '\x1b[0K\n')

def progress_log (coll, log, message, level=logging.INFO, start=0, count=None,
                  complete=True):
  def output (msg, term):
    old_terminator = log.root.handlers[0].terminator
    log.root.handlers[0].terminator = term
    log.log(level, msg)
    log.root.handlers[0].terminator = old_terminator

  return _progress(coll, output, message, start, count, complete)

def progress_print (coll, message, stream=sys.stderr, start=0, count=None,
                    complete=True):
  def output (msg, term):
    print(msg, end=term, file=stream)

  return _progress(coll, output, message, start, count, complete)
