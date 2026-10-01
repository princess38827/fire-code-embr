# Fire Code + Embr

Fire Code + Embr is a small experimental language pipeline by **Alana Sky**.
The current baseline implements:

```text
source → tokenizer → parser → AST → Fire IR → validator → Python backend
```

## Supported syntax

```text
ember warmth = 7
burn warmth
```

This compiles to:

```python
warmth = 7
print(warmth)
```

Every token, AST statement, IR instruction, and diagnostic carries a source
span. The validator rejects undefined names and duplicate top-level ember
declarations before the Python backend is allowed to run.

## Development

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Living Ember direction

This baseline begins the Living Ember work through three boundaries:

- **Intent:** validation must succeed before source becomes executable Python.
- **Memory:** named embers must be declared once and recalled before use.
- **Provenance:** source spans survive into Fire IR and diagnostics.

## Embr Core runtime

The Python API can also execute Fire IR directly, without generating or
executing Python source:

```python
from fire_code import compile_to_fire_ir, execute_fire_ir, run_source

result = run_source("ember warmth = 7\nburn warmth", output=print)
assert result.outputs == (7,)
assert result.embers["warmth"] == 7

ir = compile_to_fire_ir("ember light = 12\nburn light")
assert execute_fire_ir(ir).outputs == (12,)
```

Each run uses a fresh execution context and returns an immutable state snapshot.
The entire IR is checked before execution: undefined names and duplicate
declarations raise the existing `FireCompileError` diagnostics, and unsupported
instruction types raise `TypeError` before output is delivered.

Without an output handler, burns are collected silently. With a handler, values
are delivered in order and also collected in the result. A handler exception
stops the run and raises `FireRuntimeError` (`FIRE-RUN-001`) with the burn's
source span and the original exception as its cause. Already delivered output
cannot be rolled back.

This first runtime supports integer declarations and burns only. Persistent
memory, permissions, concurrency, and a visual debugger are future work.
