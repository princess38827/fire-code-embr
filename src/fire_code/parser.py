from .ast import BurnStatement, EmberDeclaration, Program
from .source import SourceSpan
from .tokenizer import Token, TokenKind


class ParseError(ValueError):
    def __init__(self, message: str, span: SourceSpan):
        super().__init__(message)
        self.span = span


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.index]

    def advance(self) -> Token:
        token = self.current
        self.index += 1
        return token

    def expect(self, kind: TokenKind) -> Token:
        if self.current.kind is not kind:
            raise ParseError(f"Expected {kind.name}, found {self.current.kind.name}", self.current.span)
        return self.advance()

    def parse(self) -> Program:
        statements = []
        while self.current.kind is not TokenKind.EOF:
            if self.current.kind is TokenKind.NEWLINE:
                self.advance()
                continue
            statements.append(self.parse_statement())
            if self.current.kind is TokenKind.NEWLINE:
                self.advance()
            elif self.current.kind is not TokenKind.EOF:
                raise ParseError("Expected end of line", self.current.span)
        return Program(tuple(statements))

    def parse_statement(self) -> EmberDeclaration | BurnStatement:
        if self.current.kind is TokenKind.EMBER:
            start = self.advance()
            name = self.expect(TokenKind.IDENTIFIER)
            self.expect(TokenKind.EQUALS)
            value = self.expect(TokenKind.INTEGER)
            return EmberDeclaration(
                name.text,
                int(value.text),
                SourceSpan.covering(start.span, value.span),
            )
        if self.current.kind is TokenKind.BURN:
            start = self.advance()
            name = self.expect(TokenKind.IDENTIFIER)
            return BurnStatement(name.text, SourceSpan.covering(start.span, name.span))
        raise ParseError("Expected an ember declaration or burn statement", self.current.span)


def parse(tokens: list[Token]) -> Program:
    return Parser(tokens).parse()

