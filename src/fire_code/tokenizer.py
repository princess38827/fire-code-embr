from dataclasses import dataclass
from enum import Enum, auto

from .source import SourceSpan


class TokenKind(Enum):
    EMBER = auto()
    BURN = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    EQUALS = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    text: str
    span: SourceSpan


class TokenizeError(ValueError):
    def __init__(self, message: str, span: SourceSpan):
        super().__init__(message)
        self.span = span


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    index = 0
    line = 1
    column = 1

    while index < len(source):
        char = source[index]
        if char in " \t\r":
            index += 1
            column += 1
            continue
        if char == "\n":
            tokens.append(Token(TokenKind.NEWLINE, char, SourceSpan(line, column, line, column + 1)))
            index += 1
            line += 1
            column = 1
            continue
        if char == "=":
            tokens.append(Token(TokenKind.EQUALS, char, SourceSpan(line, column, line, column + 1)))
            index += 1
            column += 1
            continue
        if char.isdigit():
            start = index
            start_column = column
            while index < len(source) and source[index].isdigit():
                index += 1
                column += 1
            text = source[start:index]
            tokens.append(Token(TokenKind.INTEGER, text, SourceSpan(line, start_column, line, column)))
            continue
        if char.isalpha() or char == "_":
            start = index
            start_column = column
            while index < len(source) and (source[index].isalnum() or source[index] == "_"):
                index += 1
                column += 1
            text = source[start:index]
            kind = {"ember": TokenKind.EMBER, "burn": TokenKind.BURN}.get(text, TokenKind.IDENTIFIER)
            tokens.append(Token(kind, text, SourceSpan(line, start_column, line, column)))
            continue
        span = SourceSpan(line, column, line, column + 1)
        raise TokenizeError(f"Unexpected character {char!r}", span)

    tokens.append(Token(TokenKind.EOF, "", SourceSpan(line, column, line, column)))
    return tokens

