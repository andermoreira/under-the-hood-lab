import unittest
from b11_shell import parse,evaluate,CommandError
class Tests(unittest.TestCase):
    def test_help(self): self.assertEqual(evaluate("help"),"help echo exit")
    def test_echo(self): self.assertEqual(evaluate("echo oi mundo"),"oi mundo")
    def test_whitespace(self): self.assertEqual(evaluate("  echo   oi  "),"oi")
    def test_empty(self): self.assertRaises(CommandError,parse," ")
    def test_unknown(self): self.assertRaises(CommandError,parse,"rm -rf /")
    def test_extra_help(self): self.assertRaises(CommandError,parse,"help extra")
    def test_exit(self): self.assertEqual(evaluate("exit"),"bye")
if __name__=="__main__": unittest.main()
