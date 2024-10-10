import os
from antlr4 import *
from cobol85.Cobol85Lexer import Cobol85Lexer
from cobol85.Cobol85Parser import Cobol85Parser


def ASTGenerator(payload):
    input_stream = InputStream(payload)
    lexer = Cobol85Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Cobol85Parser(stream)
    tree = parser.startRule()
    ast = tree.toStringTree(recog=parser)
    return ast