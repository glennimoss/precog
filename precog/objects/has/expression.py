from precog.diff import Reference
from precog.objects.base import OracleObject
from precog.objects.has.prop import HasProp
from precog.parser import Expression

HasDataDefault = HasProp('data_default')

_HasExpression = HasProp('expression', assert_type=Expression)
_HasExpressionRefs = HasProp('_expression_refs', dependency=Reference.HARD)
class HasExpression (_HasExpression, _HasExpressionRefs):

  @_HasExpression.expression.setter
  def expression (self, value):
    if value and not isinstance(value, Expression):
      value = Expression(value, scope_obj=self.table, database=self.database)
    _HasExpression.expression.__set__(self, value)

  @expression.getter
  def expression (self):
    expression = _HasExpression.expression.__get__(self)
    if (expression and not expression.tree and
        self.table and self.database):
      # Try again for late binding
      _HasExpression.expression.__set__(self, expression.text)
    return _HasExpression.expression.__get__(self)

  @OracleObject.dependencies.getter
  def dependencies (self):
    self._expression_refs = self.expression.references
    return OracleObject.dependencies.__get__(self)

class HasExpressionWithDataDefault (HasExpression):
  """ Expects subclass to also inherit HasDataDefault somewhere. """

  @HasExpression.expression.setter
  def expression (self, value):
    HasExpression.expression.__set__(self, value)
    self.data_default = self.expression and self.expression.text

  data_default = HasDataDefault.data_default.setter(expression.__set__)
