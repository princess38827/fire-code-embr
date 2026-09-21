from .ast import BurnStatement, EmberDeclaration, Program
from .fire_ir import BurnEmber, DeclareEmber, FireIR


def lower_to_fire_ir(program: Program) -> FireIR:
    instructions = []
    for statement in program.statements:
        if isinstance(statement, EmberDeclaration):
            instructions.append(DeclareEmber(statement.name, statement.value, statement.source_span))
        elif isinstance(statement, BurnStatement):
            instructions.append(BurnEmber(statement.name, statement.source_span))
        else:  # pragma: no cover - defensive boundary for future AST nodes
            raise TypeError(f"Unsupported AST statement: {type(statement).__name__}")
    return FireIR(tuple(instructions))

