"""Shell parser boundary properties; never invokes OS commands."""
import unittest
from b11_shell import CommandError, parse, evaluate

class ShellBoundaries(unittest.TestCase):
    def test_whitespace_normalization(self):
        for source in ("echo   alpha   beta", " echo alpha beta ", "\techo\talpha\tbeta\n"):
            with self.subTest(source=source):
                self.assertEqual(parse(source), ("echo", ["alpha", "beta"]))
                self.assertEqual(evaluate(source), "alpha beta")

    def test_empty_echo_is_valid(self):
        self.assertEqual(parse("echo"), ("echo", []))
        self.assertEqual(evaluate("echo"), "")

    def test_help_exit_reject_arguments(self):
        for source in ("help extra", "exit 0", "help --all", "exit now"):
            with self.subTest(source=source):
                self.assertRaises(CommandError, parse, source)

    def test_nontext_and_empty_inputs_rejected(self):
        for source in (None, 1, b"echo", "", "  \t"):
            with self.subTest(source=repr(source)):
                self.assertRaises(CommandError, parse, source)

    def test_no_implicit_command_execution(self):
        for source in ("rm -rf /", "ls", "pwd", "Echo hello", "echo;rm x"):
            with self.subTest(source=source):
                self.assertRaises(CommandError, parse, source)

if __name__ == "__main__":
    unittest.main()
