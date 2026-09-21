from .diagnostics import Diagnostic
from .fire_ir import BurnEmber, DeclareEmber, FireIR
from .source import SourceSpan


def validate_fire_ir(ir: FireIR) -> list[Diagnostic]:
    declarations: dict[str, SourceSpan | None] = {}
    diagnostics: list[Diagnostic] = []

    for instruction in ir.instructions:
        if isinstance(instruction, DeclareEmber):
            if instruction.name in declarations:
                diagnostics.append(
                    Diagnostic(
                        code="FIRE-IR-002",
                        message=f"Ember {instruction.name!r} is already declared",
                        name=instruction.name,
                        source_span=instruction.source_span,
                        original_span=declarations[instruction.name],
                    )
                )
            else:
                declarations[instruction.name] = instruction.source_span
        elif isinstance(instruction, BurnEmber) and instruction.name not in declarations:
            diagnostics.append(
                Diagnostic(
                    code="FIRE-IR-001",
                    message=f"Ember {instruction.name!r} has not been declared",
                    name=instruction.name,
                    source_span=instruction.source_span,
                )
            )

    return diagnostics

