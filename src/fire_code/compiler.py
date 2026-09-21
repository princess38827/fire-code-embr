from .diagnostics import FireCompileError
from .fire_ir import FireIR
from .lowering import lower_to_fire_ir
from .parser import parse
from .python_backend import generate_python
from .tokenizer import tokenize
from .validator import validate_fire_ir


def compile_to_fire_ir(source: str) -> FireIR:
    return lower_to_fire_ir(parse(tokenize(source)))


def compile_to_python(source: str) -> str:
    ir = compile_to_fire_ir(source)
    diagnostics = validate_fire_ir(ir)
    if diagnostics:
        raise FireCompileError(diagnostics)
    return generate_python(ir)

