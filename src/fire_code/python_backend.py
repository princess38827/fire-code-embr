from .fire_ir import BurnEmber, DeclareEmber, FireIR


def generate_python(ir: FireIR) -> str:
    lines = []
    for instruction in ir.instructions:
        if isinstance(instruction, DeclareEmber):
            lines.append(f"{instruction.name} = {instruction.value}")
        elif isinstance(instruction, BurnEmber):
            lines.append(f"print({instruction.name})")
        else:  # pragma: no cover
            raise TypeError(f"Unsupported Fire IR instruction: {type(instruction).__name__}")
    return "\n".join(lines) + ("\n" if lines else "")

