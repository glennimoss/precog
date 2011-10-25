from precog.diff import Reference
from precog.objects.has.prop import HasProp
from precog.objects.plsql import Type

HasUserType = HasProp('user_type', assert_type=Type, dependency=Reference.HARD)
