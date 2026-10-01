"""Small Embr Core interpreter for validated Fire IR."""

from collections.abc import Callable
from dataclasses import dataclass
from types import MappingProxyType
from collections.abc import Mapping

from .compiler import compile_to_fire_ir
from .diagnostics import FireCompileError
from .fire_ir import BurnEmber, DeclareEmber, FireIR
from .source import SourceSpan
from .validator import validate_fire_ir


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Immutable snapshot of one run's named embers and emitted values."""

    embers: Mapping[str, int]
    outputs: tuple[int, ...]


class FireRuntimeError(Exception):
    """An output handler failed at a particular burn instruction."""

    def __init__(self, message: str, source_span: SourceSpan | None):
        super().__init__(message)
        self.code = "FIRE-RUN-001"
        self.source_span = source_span


def execute_fire_ir(
    ir: FireIR, *, output: Callable[[int], None] | None = None
) -> ExecutionResult:
    """Validate the whole program, then execute in a fresh context.

    Values are always collected. An optional output handler receives each burn
    value in order. Handler failures stop execution and retain source provenance;
    already delivered output cannot be rolled back.
    """
    # Reject unknown nodes before any callback can produce an external effect.
    for instruction in ir.instructions:
        if not isinstance(instruction, (DeclareEmber, BurnEmber)):
            raise TypeError(
                f"Unsupported Fire IR instruction: {type(instruction).__name__}"
            )
    diagnostics = validate_fire_ir(ir)
    if diagnostics:
        raise FireCompileError(diagnostics)

    embers: dict[str, int] = {}
    outputs: list[int] = []
    for instruction in ir.instructions:
        if isinstance(instruction, DeclareEmber):
            embers[instruction.name] = instruction.value
        else:
            value = embers[instruction.name]
            if output is not None:
                try:
                    output(value)
                except Exception as error:
                    raise FireRuntimeError(
                        f"Output handler failed for ember {instruction.name!r}",
                        instruction.source_span,
                    ) from error
            outputs.append(value)
    return ExecutionResult(MappingProxyType(embers), tuple(outputs))


def run_source(
    source: str, *, output: Callable[[int], None] | None = None
) -> ExecutionResult:
    """Compile Fire Code and execute its IR without generating Python."""
    return execute_fire_ir(compile_to_fire_ir(source), output=output)
