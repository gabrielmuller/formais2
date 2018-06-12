import unittest
from reader import *
from rg import RegularGrammar 

class TestReader(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

    """
    def test_read_rg(self):
        a = RegularGrammar(read_rg("S -> aS | bB \n B -> cS | f"))
        self.assertTrue(a.accepts('aaaaabcaaaabf'))
        self.assertTrue(a.accepts('bf'))
        self.assertTrue(a.accepts('bcaaaabf'))
        self.assertTrue(a.accepts('abcabcabcabf'))
        self.assertFalse(a.accepts('bcf'))
        self.assertFalse(a.accepts('aaaacf'))
        self.assertFalse(a.accepts(''))

        a = RegularGrammar(read_rg("S -> a | cB | & \n B -> f"))
        self.assertTrue(a.accepts('a'))
        self.assertTrue(a.accepts('cf'))
        self.assertTrue(a.accepts(''))
        self.assertFalse(a.accepts('c'))
        self.assertFalse(a.accepts('f'))
        self.assertFalse(a.accepts('acf'))
        
        a = RegularGrammar(read_rg("S -> a \n S -> cB | & \n B -> f"))
        self.assertTrue(a.accepts('a'))
        self.assertTrue(a.accepts('cf'))
        self.assertTrue(a.accepts(''))
        self.assertFalse(a.accepts('c'))
        self.assertFalse(a.accepts('f'))
        self.assertFalse(a.accepts('acf'))

        a = RegularGrammar(read_rg("Start -> fZ \n Z -> zZ | yZ | z"))
        self.assertTrue(a.accepts('fyz'))
        self.assertTrue(a.accepts('fz'))
        self.assertTrue(a.accepts('fzzyyzz'))
        self.assertFalse(a.accepts('z'))
        self.assertFalse(a.accepts('fzzzy'))
        self.assertFalse(a.accepts(''))
    """

    def test_read_rg_error(self):
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg(""))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("S"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("SA"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("S1E"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("S -> aS | a |"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("B -> aA \n S -> aS | | a"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("S aA | a"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("s -> aA | a"))
        with self.assertRaises(SyntaxError):
            a = RegularGrammar(read_rg("S -> aA | a \n A -> a | a&"))

    def test_rg_tostr(self):
        return
        

if __name__ == "__main__":
    unittest.main()

