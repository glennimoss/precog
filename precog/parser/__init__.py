import logging
from antlr3.ext import (InputStream, FileStream, MultiChannelTokenStream,
    NamedConstant, StringStream)
from precog.parser.sqlLexer import sqlLexer
from precog.parser.sqlParser import sqlParser

__all__ = ['file_parser', 'string_parser']

def file_parser (filename):
  stream = FileStream
  name = filename
  if not isinstance(filename, str):
    stream = InputStream
    name = filename.name
  logging.getLogger('precog.parser.file_parser()').info(
      "Parsing file {}".format(name))
  return parser(stream(filename))

def string_parser (string):
  return parser(StringStream(string))

def parser (stream):
  lexer = sqlLexer(stream)
  tokenStream = MultiChannelTokenStream(lexer)
  parser = sqlParser(tokenStream)
  return parser
