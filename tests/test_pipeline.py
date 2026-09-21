import unittest

from fire_code import FireCompileError, compile_to_fire_ir, compile_to_python, generate_python
from fire_code.fire_ir import strip_source_spans


class PipelineTests(unittest.TestCase):
    def test_source_spans_survive_lowering_without_changing_python(self):
        ir = compile_to_fire_ir("ember warmth = 7")

        self.assertEqual(ir.instructions[0].source_span.line, 1)
        self.assertEqual(ir.instructions[0].source_span.column, 1)
        self.assertEqual(generate_python(ir), generate_python(strip_source_spans(ir)))

    def test_valid_program_compiles_to_python(self):
        python = compile_to_python("""
ember warmth = 7
burn warmth
""")

        self.assertEqual(python, "warmth = 7\nprint(warmth)\n")

    def test_undefined_name_stops_compilation(self):
        with self.assertRaises(FireCompileError) as caught:
            compile_to_python("burn missing_flame")

        self.assertEqual(len(caught.exception.diagnostics), 1)
        self.assertEqual(caught.exception.diagnostics[0].code, "FIRE-IR-001")
        self.assertEqual(caught.exception.diagnostics[0].name, "missing_flame")
        self.assertEqual(caught.exception.diagnostics[0].source_span.line, 1)

    def test_duplicate_declaration_references_both_locations(self):
        with self.assertRaises(FireCompileError) as caught:
            compile_to_python("ember warmth = 7\nember warmth = 9")

        diagnostic = caught.exception.diagnostics[0]
        self.assertEqual(diagnostic.code, "FIRE-IR-002")
        self.assertEqual(diagnostic.source_span.line, 2)
        self.assertEqual(diagnostic.original_span.line, 1)


if __name__ == "__main__":
    unittest.main()
