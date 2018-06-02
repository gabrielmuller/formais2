import unittest
from parser import *
from nfa import NFA

class TestParser(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

    def test_preprocess(self):
        s = 'ab | bac (ba)*b?a+'
        self.assertEqual(preprocess(s), 'a.b|b.a.c.(b.a)*.b?.a+')
    
    def test_treefy(self):
        a = Node('a')
        b = Node('b')
        c = Node('c')
        d = Node('d')
        e = Node('e')
        tree = treefy([a, b, c, d, e], 'R')
        inorder = ''.join([v.value for v in tree.in_order()])
        self.assertEqual(inorder.count('R'), 4)
        self.assertEqual(inorder.count('RR'), 0)
    
    def test_parse(self):
        a = parse('wx(y .... () ()*()? z)*')
        self.assertEqual(a.value, '.')
        self.assertEqual(a.left.value, '.')
        self.assertEqual(a.left.left.value, 'w')
        self.assertEqual(a.left.right.value, 'x')
        self.assertEqual(a.right.value, '*')
        self.assertEqual(a.right.left.value, '.')
        self.assertEqual(a.right.left.left.value, 'y')
        self.assertEqual(a.right.left.right.value, 'z')

    def test_parse_rg(self):
        a = NFA.from_rg(parse_rg("S -> aS | bB \n B -> cS | f"))
        self.assertTrue(a.accepts('aaaaabcaaaabf'))
        self.assertTrue(a.accepts('bf'))
        self.assertTrue(a.accepts('bcaaaabf'))
        self.assertTrue(a.accepts('abcabcabcabf'))
        self.assertFalse(a.accepts('bcf'))
        self.assertFalse(a.accepts('aaaacf'))
        self.assertFalse(a.accepts(''))

        a = NFA.from_rg(parse_rg("S -> a | cB | & \n B -> f"))
        self.assertTrue(a.accepts('a'))
        self.assertTrue(a.accepts('cf'))
        self.assertTrue(a.accepts(''))
        self.assertFalse(a.accepts('c'))
        self.assertFalse(a.accepts('f'))
        self.assertFalse(a.accepts('acf'))

        a = NFA.from_rg(parse_rg("S -> fZ \n Z -> zZ | yZ | z"))
        self.assertTrue(a.accepts('fyz'))
        self.assertTrue(a.accepts('fz'))
        self.assertTrue(a.accepts('fzzyyzz'))
        self.assertFalse(a.accepts('z'))
        self.assertFalse(a.accepts('fzzzy'))
        self.assertFalse(a.accepts(''))

    def test_parse_rg_error(self):
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> aS | bB \n B -> cS | f \n SA -> u"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> | aS | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> aS | a |"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("B -> aA \n S -> aS | | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S > aA | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S > aA | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("s -> aA | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> AA | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> aa | a"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> aA | A"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> aA | a \n A -> a | &"))
        with self.assertRaises(SyntaxError):
            a = NFA.from_rg(parse_rg("S -> aA | a \n A -> a | a&"))

    def test_parse_regex_error(self):
        with self.assertRaises(SyntaxError):
            parse('a|*b')
        with self.assertRaises(SyntaxError):
            parse('*a')
        with self.assertRaises(SyntaxError):
            parse('a | +b')
        with self.assertRaises(SyntaxError):
            parse('a||||b')
        with self.assertRaises(SyntaxError):
            parse('a||||b')
        with self.assertRaises(SyntaxError):
            parse('a|b|')
        with self.assertRaises(SyntaxError):
            parse('|a|b')
        with self.assertRaises(SyntaxError):
            parse('a(a(bb)))')
        with self.assertRaises(SyntaxError):
            parse('a(b))c(')
        with self.assertRaises(SyntaxWarning):
            parse('a(aa*(a) *')
        with self.assertRaises(SyntaxWarning):
            parse('a(a(a(a( (( (')

if __name__ == "__main__":
    unittest.main()

