import datetime, re

from precog import db
from precog.diff import Diff
from precog.identifier import OracleFQN
from precog.objects.base import OracleObject
from precog.objects.column import Column
from precog.objects.has.columns import HasSoftColumns, HasTableFromColumns
from precog.util import InsensitiveDict, pluralize

class Data (HasSoftColumns, HasTableFromColumns, OracleObject):

  def __init__ (self, table, columns, expressions, **props):
    super().__init__(OracleFQN(table.name.schema, table.name.obj,
      "__DATA_{}".format(len(table.data))), columns=columns, **props)

    self.expressions = []
    for i, exp in enumerate(expressions):
      exp = Data.parse(exp, self.columns[i])
      self.expressions.append(exp)

  def __eq__ (self, other):
    if not isinstance(other, type(self)):
      return False

    return self.table.name == other.table.name and self._comp() == other._comp()

  def __ne__ (self, other):
    return not self == other

  def __hash__ (self):
    return hash((self.table.name, self._comp()))

  def _comp (self, warnings=False):
    """ A tuple view for hashing, comparing, etc.
    Optional "warnings" whether to warn about underspecification.
    """
    discriminators = self.columns
    uks = sorted(
      {uk for col in self.columns for uk in col._find_unique_constraints()},
      key=lambda o: len(o.columns), reverse=True)

    for uk in uks:
      col_set = set(uk.columns)
      if col_set.issubset(self.columns):
        discriminators = col_set

      # If there's a PK we prefer it over anything else (Including warning
      # about underspecified rows.)
      if uk.is_pk:
        break

    # Warn about not enough columns to uniquely specify this row of data.
    if warnings and discriminators is self.columns and uks:
      try:
        uk = [k for k in uks if k.is_pk][0]
      except IndexError:
        # If no PK, then use the shortest UK
        uk = uks[-1]

      unspec_cols = sorted({col.name.part for col in uk.columns} -
                           {col.name.part for col in self.columns})
      col_list = ''
      if len(unspec_cols) > 1:
        col_list = ', '.join(unspec_cols[:-1]) + ' and '
      col_list += unspec_cols[-1]

      self.log.warning_once('INSERT {} underspecifies the {} key "{}". '
                            'Consider adding {} {} to the INSERT statement.'
                            .format(
                              self.get_location(True),
                              "primary" if uk.is_pk else "unique",
                              uk,
                              pluralize(len(unspec_cols), "column", False),
                              col_list))

    discriminators = {col.name.part.lower() for col in discriminators}

    return tuple(sorted(tup for tup in self.values().items()
                        if tup[0] in discriminators))

  def values (self):
    return InsensitiveDict((col.name.part.lower(), value)
                           for col, value in zip(self.columns, self.expressions)
                           if not col.is_virtual)

  @staticmethod
  def format (value):
    if value is None:
      return 'NULL'
    if isinstance(value, datetime.datetime):
      if value.microsecond:
        fmt = "TO_TIMESTAMP('{}', 'YYYY-MM-DD HH24:MI:SS.FF')"
      else:
        fmt = "TO_DATE('{}', 'YYYY-MM-DD HH24:MI:SS')"
      return fmt.format(value)
    return str(value)

  def _sql (self, fq=True, columns=None):
    table_name = self.table.name
    if not fq:
      table_name = table_name.obj
    values = self.values()
    if columns:
      values = InsensitiveDict((col, values[col])
                               for col in columns if col in values)

    return "INSERT INTO {} ({}) VALUES ({})".format(table_name.lower(),
      ", ".join(values.keys()), ", ".join(Data.format(val)
                                          for val in values.values()))

  def _equal_pairs (self, pairs, assign=False):
    return [" = ".join((col, Data.format(val))) if val is not None or assign
            else "{} IS NULL".format(col)
            for col, val in pairs.items()]

  def _drop (self):
    return Diff("DELETE FROM {} WHERE {}"
                .format(self.table.name.lower(),
                        " AND ".join(self._equal_pairs(self.values()))))

  def diff (self, other, **kwargs):
    other_vals = other.values()
    col_diff = {col: val for col, val in self.values().items()
                if (col in other_vals and val != other_vals[col])}

    if col_diff:
      return [Diff("UPDATE {} SET {} WHERE {}"
                   .format(self.table.name.lower(),
                           ", ".join(self._equal_pairs(col_diff, True)),
                           " AND ".join(self._equal_pairs(dict(self._comp()))))
                  )]
    return []



  @staticmethod
  def parse (value, column):
    if isinstance(value, str):
      if value.upper() == 'NULL' or value == "''":
        return None

      if column.is_number or not (value.startswith("'") and
                                  value.endswith("'")):
        val = value.strip("'")
        try:
          num = float(val)
          if num.is_integer():
            num = int(num)
          if not column.is_number:
            num = "'{}'".format(num)
          return num
        except ValueError:
          pass
      if column.is_datetime:
        date = re.match(r"^'\s*(\d{4}(.)\d{2}\2\d{2})\s*"
                        r"(\d{2}:\d{2}(:\d{2}(\.\d{1,6})?)?)?\s*'$", value)
        if date:
          date_parts = date.groups()
          datestr = " ".join(filter(None, date_parts[0:3:2]))
          formatstr = ["%Y{0}%m{0}%d".format(date_parts[1])]
          if date_parts[2]:
            formatstr.append(" %H:%M")
          if date_parts[3]:
            formatstr.append(":%S")
          if date_parts[4]:
            formatstr.append(".%f")
          formatstr = "".join(formatstr)
          return datetime.datetime.strptime(datestr, formatstr)
    return value

  @staticmethod
  def escape (value, column):
    if isinstance(value, str):
      return "'{}'".format(value.replace("'", "''"))
    return Data.parse(value, column)

  @classmethod
  def from_db (class_, table, column_names=None):
    order_by = ''
    if column_names:
      order_by = "ORDER BY {}".format(", ".join(column_names))
    if not table.data:
      with db.exact_numbers():
        table.log.debug("Querying {} data for columns {}...".format(
          table.name, "(all)" if column_names is None else ", ".join(column_names)))
        rs = db.query_all(""" SELECT *
                              FROM {}
                              {}
                          """.format(table.name, order_by))

        table.log.debug("Query returned {} rows.".format(len(rs)))
      if rs:
        columns = [table.database.find(
          OracleFQN(table.name.schema, table.name.obj, column_name), Column)
          for column_name in rs[0]]

        for row in rs:
          table.add_data(columns, [Data.escape(col, columns[i])
                                   for i, col in enumerate(row.values())])

