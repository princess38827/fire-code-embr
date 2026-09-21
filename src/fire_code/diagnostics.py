from dataclasses import dataclass

from .source import SourceSpan


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    name: str
    source_span: SourceSpan | None = None
    original_span: SourceSpan | None = None


class FireCompileError(Exception):
    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        summary = "; ".join(f"{item.code}: {item.message}" for item in diagnostics)
        super().__init__(summary)

