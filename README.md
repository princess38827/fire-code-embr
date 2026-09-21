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
