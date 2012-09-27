from precog.diff import Reference
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp
from precog.parser.parser import Expression

_HasDataDefault = HasProp('data_default', strict_none=True)
class HasDataDefault (_HasDataDefault):

  @_HasDataDefault.data_default.setter
  def data_default (self, value):
    if isinstance(value, str):
      value = value.strip()
    _HasDataDefault.data_default.__set__(self, value)

_HasExpression = HasProp('expression', assert_type=Expression)
_HasExpressionRefs = HasProp('_expression_refs', dependency=Reference.HARD)
class HasExpression (_HasExpression, _HasExpressionRefs):

  @_HasExpression.expression.setter
  def expression (self, value):
    if value and not isinstance(value, Expression):
      value = Expression(value, scope_obj=self.table)
    _HasExpression.expression.__set__(self, value)

  @expression.getter
  def expression (self):
    expression = _HasExpression.expression.__get__(self)
    if (expression and not expression.tree and
        self.table and self.database):
      # Try again for late binding
      self.expression = expression.text
      expression = _HasExpression.expression.__get__(self)
    if expression:
      return expression
    if not self.deferred:
      self.log.warn("{} has no expression!".format(self.pretty_name))
    return None

  def _build_dep_set (self, *args, **kwargs):
    # refresh expression references
    self._expression_refs = self.expression.references
    return super()._build_dep_set(*args, **kwargs)

class HasExpressionWithDataDefault (HasExpression):
  """ Expects subclass to also inherit HasDataDefault somewhere. """

  expression = HasExpression.expression

  @property
  def data_default (self):
    return self.expression and self.expression.text

  data_default = data_default.setter(expression.__set__)

  def _eq_data_default (self, other):
    return (isinstance(other, HasExpression) and
            self.expression == other.expression)
