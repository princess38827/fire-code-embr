import unittest

from fire_code import (
    FireCompileError, FireRuntimeError, compile_to_fire_ir,
    execute_fire_ir, run_source,
)
from fire_code.fire_ir import FireIR, strip_source_spans


class RuntimeTests(unittest.TestCase):
    def test_run_collects_values_and_named_state(self):
        received = []
        result = run_source(
            "ember warmth = 7\nburn warmth\nember light = 12\nburn light\nburn warmth",
            output=received.append,
        )
        self.assertEqual(received, [7, 12, 7])
        self.assertEqual(result.outputs, (7, 12, 7))
        self.assertEqual(result.embers, {"warmth": 7, "light": 12})
        with self.assertRaises(TypeError):
            result.embers["warmth"] = 9

    def test_invalid_program_has_no_output_even_after_valid_prefix(self):
        received = []
        with self.assertRaises(FireCompileError) as caught:
            run_source("ember warmth = 7\nburn warmth\nburn missing_flame",
                       output=received.append)
        self.assertEqual(received, [])
        diagnostic = caught.exception.diagnostics[0]
        self.assertEqual(diagnostic.code, "FIRE-IR-001")
        self.assertEqual(diagnostic.name, "missing_flame")
        self.assertEqual(diagnostic.source_span.line, 3)

    def test_direct_ir_is_validated(self):
        ir = compile_to_fire_ir("ember warmth = 7\nember warmth = 9")
        with self.assertRaises(FireCompileError) as caught:
            execute_fire_ir(ir)
        diagnostic = caught.exception.diagnostics[0]
        self.assertEqual(diagnostic.code, "FIRE-IR-002")
        self.assertEqual(diagnostic.original_span.line, 1)

    def test_use_before_declaration_is_rejected(self):
        with self.assertRaises(FireCompileError):
            run_source("burn warmth\nember warmth = 7")

    def test_context_is_fresh_for_every_run(self):
        first = run_source("ember warmth = 7")
        second = run_source("ember warmth = 9\nburn warmth")
        self.assertEqual(first.embers["warmth"], 7)
        self.assertEqual(second.outputs, (9,))
        with self.assertRaises(FireCompileError):
            run_source("burn warmth")

    def test_empty_program(self):
        result = run_source("")
        self.assertEqual(result.outputs, ())
        self.assertEqual(result.embers, {})

    def test_source_metadata_does_not_change_execution(self):
        ir = compile_to_fire_ir("ember warmth = 7\nburn warmth")
        self.assertEqual(execute_fire_ir(ir), execute_fire_ir(strip_source_spans(ir)))

    def test_handler_error_retains_burn_location_and_cause(self):
        error = OSError("sink unavailable")
        def fail(value):
            raise error
        with self.assertRaises(FireRuntimeError) as caught:
            run_source("ember warmth = 7\nburn warmth", output=fail)
        self.assertEqual(caught.exception.code, "FIRE-RUN-001")
        self.assertEqual(caught.exception.source_span.line, 2)
        self.assertEqual(caught.exception.source_span.column, 1)
        self.assertIs(caught.exception.__cause__, error)

    def test_unknown_instruction_is_rejected_before_output(self):
        received = []
        valid = compile_to_fire_ir("ember warmth = 7\nburn warmth")
        ir = FireIR(valid.instructions + (object(),))
        with self.assertRaises(TypeError):
            execute_fire_ir(ir, output=received.append)
        self.assertEqual(received, [])


if __name__ == "__main__":
    unittest.main()
