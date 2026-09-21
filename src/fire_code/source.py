from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceSpan:
    line: int
    column: int
    end_line: int
    end_column: int

    @classmethod
    def covering(cls, first: "SourceSpan", last: "SourceSpan") -> "SourceSpan":
        return cls(first.line, first.column, last.end_line, last.end_column)

