"""Public API for the Fire Code + Embr compiler."""

from .compiler import compile_to_fire_ir, compile_to_python
from .diagnostics import Diagnostic, FireCompileError
from .python_backend import generate_python
from .validator import validate_fire_ir

__all__ = [
    "Diagnostic",
    "FireCompileError",
    "compile_to_fire_ir",
    "compile_to_python",
    "generate_python",
    "validate_fire_ir",
]

