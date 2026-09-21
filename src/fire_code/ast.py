from dataclasses import dataclass

from .source import SourceSpan


@dataclass(frozen=True, slots=True)
class EmberDeclaration:
    name: str
    value: int
    source_span: SourceSpan


@dataclass(frozen=True, slots=True)
class BurnStatement:
    name: str
    source_span: SourceSpan


Statement = EmberDeclaration | BurnStatement


@dataclass(frozen=True, slots=True)
class Program:
    statements: tuple[Statement, ...]

