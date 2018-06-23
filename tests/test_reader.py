import unittest
from model.reader import *
from model.cfg import Grammar 

class TestReader(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

    def test_read_cfg(self):
        a = "S1 -> 0 S1 0 | 1 S1 1 | 0 0 | 1 1"
        r = Grammar(a)
        prods = {"S1" : {('0', 'S1', '0'), ('1', 'S1', '1'), ('0', '0'), ('1', '1')}}
        self.assertEqual(r.prods, prods)

    def test_read_cfg_error(self):
        with self.assertRaises(SyntaxError):
            a = Grammar("")
        with self.assertRaises(SyntaxError):
            a = Grammar("S")
        with self.assertRaises(SyntaxError):
            a = Grammar("S A")
        with self.assertRaises(SyntaxError):
            a = Grammar("S1 E")
        with self.assertRaises(SyntaxError):
            a = Grammar("S -> a S | a |")
        with self.assertRaises(SyntaxError):
            a = Grammar("S ->   \n\n")
        with self.assertRaises(SyntaxError):
            a = Grammar("S ->  ")
        with self.assertRaises(SyntaxError):
            a = Grammar("S ->  a $ b")
        with self.assertRaises(SyntaxError):
            a = Grammar("S ->  a b -> a b b")
        with self.assertRaises(SyntaxError):
            a = Grammar("B -> a A \n S -> a S | | a")
        with self.assertRaises(SyntaxError):
            a = Grammar("S a A | a")
        with self.assertRaises(SyntaxError):
            a = Grammar("s -> a A | a")
        with self.assertRaises(SyntaxError):
            a = Grammar("S -> a A | a \n A -> a | a &")


if __name__ == "__main__":
    unittest.main()
