from dataclasses import dataclass, replace

from .source import SourceSpan


@dataclass(frozen=True, slots=True)
class DeclareEmber:
    name: str
    value: int
    source_span: SourceSpan | None = None


@dataclass(frozen=True, slots=True)
class BurnEmber:
    name: str
    source_span: SourceSpan | None = None


Instruction = DeclareEmber | BurnEmber


@dataclass(frozen=True, slots=True)
class FireIR:
    instructions: tuple[Instruction, ...]


def strip_source_spans(ir: FireIR) -> FireIR:
    return FireIR(tuple(replace(instruction, source_span=None) for instruction in ir.instructions))

