from antlr3.ext import (FileStream, MultiChannelTokenStream, NamedConstant,
    StringStream)
from precog.parser.sqlLexer import sqlLexer
from precog.parser.sqlParser import sqlParser

__all__ = ['file_parser', 'string_parser']

def file_parser (filename):
  return parser(FileStream(filename))

def string_parser (string):
  return parser(StringStream(string))

def parser (stream):
  lexer = sqlLexer(stream)
  tokenStream = MultiChannelTokenStream(lexer)
  parser = sqlParser(tokenStream)
  return parser
