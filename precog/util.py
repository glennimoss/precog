from collections import OrderedDict, defaultdict
import logging, sys, time

class classproperty (object):

  def __init__ (self, getter, instance_getter=None):
    self._getter = getter
    self._instance_getter = instance_getter

  def instance (self, func):
    self._instance_getter = func
    return self

  def __get__ (self, obj, class_):
    if obj is None or self._instance_getter is None:
      return self._getter(class_)
    return self._instance_getter(obj)

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
      return ValidatingList(super().__add__(other))

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
  _log = None

  @classproperty
  def log (class_):
    if not class_._log:
      class_._log = HasLog.log_for(class_)
    return class_._log

  @log.instance
  def log (self):
    if not self._log:
      self._log = HasLog.log_for(self)
    return self._log

  def __getstate__ (self):
    state = self.__dict__.copy()
    state['_log'] = None
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

class _OnceLogger (logging.Logger):
  _logged = defaultdict(set)

  def __init__ (self, name, level=0):
    super().__init__(name, level)


  def debug_once (self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.DEBUG):
      self.log_once(logging.DEBUG, msg, *args, **kwargs)

  def info_once (self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.INFO):
      self.log_once(logging.INFO, msg, *args, **kwargs)

  def warning_once (self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.WARNING):
      self.log_once(logging.WARNING, msg, *args, **kwargs)

  def error_once (self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.ERROR):
      self.log_once(logging.ERROR, msg, *args, **kwargs)

  def critical_once (self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.CRITICAL):
      self.log_once(logging.CRITICAL, msg, *args, **kwargs)

  fatal_once = critical_once

  def log_once (self, level, msg, *args, **kwargs):
    if self.isEnabledFor(level):
      if msg not in self._logged[level]:
        self._logged[level].add(msg)
        self.log(level, msg, *args, **kwargs)


logging.setLoggerClass(_OnceLogger)

progress_output_enabled = True

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
    try:
      obj = next(itr)
      while True:
        output(make_message(obj).format("{:03.0%}".format(c/count)),
               '\x1b[0K\r')
        step = yield obj
        if step is None:
          step = 1
        c += step
        obj = next(itr)
    except StopIteration:
      pass

  if complete:
    output(make_message(None).format('100%'), '\x1b[0K\n')

def progress_log (coll, log, message, level=logging.INFO, start=0, count=None,
                  complete=True):
  if not progress_output_enabled or log.isEnabledFor(logging.DEBUG):
    # These progress messages are just extra noise at debug level
    def output (msg, term):
      pass
  else:
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
    stream.flush()

  return _progress(coll, output, message, start, count, complete)

def pluralize (count, word, with_count=True):
  parts = []

  if abs(count) != 1:
    if word[-1] == 'x':
      parts.append('es')
    elif word[-1] == 'y':
      parts.append('ies')
      word = word[:-1]
    else:
      parts.append('s')

  parts.append(word)

  if with_count:
    parts.append("{} ".format(count))


  return "".join(reversed(parts))

class timer (object):

  def __init__ (self, task):
    self.task = task
    self.start = time.time()

  def stop (self, force=False):
    took = time.time() - self.start
    if took > 1 or force:
      print("{} took {:.10f}".format(self.task, took))
    return took

def split_list (list, func):
  lists = {}
  for item in list:
    ret = func(item)
    if ret not in lists:
      lists[ret] = []
    lists[ret].append(item)

  return lists

def _type_to_class_name (type):
  return ''.join(word.capitalize() for word in type.split())

def _with_location (obj, with_line=True):
  return '{}, {}'.format(obj.pretty_name, obj.get_location(with_line))
