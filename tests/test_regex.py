import unittest
from regex import Regex, Node

class TestRegex(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

        # árvore de strings para teste
        self.tree = Node('.')
        self.tree.left = Node('l')
        self.tree.right = Node('r')
        self.tree.right.left = Node('a')
        self.tree.right.right = Node('b')
        self.tree.left.left = Node('c')

        # 'ab' apenas
        self.ab = Regex('')

        self.ab.root = Node('.')
        self.ab.root.left = Node('a')
        self.ab.root.right = Node('b')

        self.ab.thread()

        # (ab | ac)* a
        self.abaca = Regex('')

        n = Node('|')
        n.left = Node('.')
        n.right = Node('.')
        n.left.left = Node('a')
        n.left.right = Node('b')
        n.right.left = Node('a')
        n.right.right = Node('c')

        r = Node('.')
        r.left = Node('+')
        r.right = Node('a')
        r.left.left = n

        self.abaca.root = r
        self.abaca.thread()

    def test_is_operator(self):
        self.assertTrue(self.ab.root.is_operator())
        self.assertFalse(self.ab.root.left.is_operator())
        self.assertFalse(self.ab.root.right.is_operator())
        self.assertFalse(self.ab.root.left.right.left.right.left.is_operator())
        
        self.assertTrue(self.abaca.root.left.left.left.is_operator())
        self.assertTrue(self.abaca.root.left.right.left.right.is_operator())
        self.assertFalse(self.abaca.root.right.is_operator())

    def test_in_order(self):
        nodes = self.tree.in_order()
        vals = map(lambda node: node.value, nodes)
        string = ''.join(vals)
        self.assertEqual(string, "cl.arb")

    def test_parse_simone(self):
        a = Regex("a")
        b = a.dfa
        self.assertTrue(b.accepts("a"))
        self.assertFalse(b.accepts(""))
        self.assertFalse(b.accepts("aa"))

        a = Regex("a*")
        b = a.dfa
        self.assertTrue(b.accepts("a"))
        self.assertTrue(b.accepts("aaaa"))
        self.assertTrue(b.accepts(""))
        self.assertFalse(b.accepts("b"))

        a = Regex("")
        b = a.dfa
        self.assertFalse(b.accepts(""))
        self.assertFalse(b.accepts("a"))

        a = Regex("ab|cde | f |   g")
        b = a.dfa
        self.assertTrue(b.accepts("ab"))
        self.assertTrue(b.accepts("cde"))
        self.assertTrue(b.accepts("f"))
        self.assertTrue(b.accepts("g"))
        self.assertFalse(b.accepts(""))
        self.assertFalse(b.accepts("a"))
        self.assertFalse(b.accepts("abcde"))
        self.assertFalse(b.accepts("fg"))

        a = Regex("a*bc* | 1*2")
        b = a.dfa
        self.assertTrue(b.accepts("ab"))
        self.assertTrue(b.accepts("aaaaabcc"))
        self.assertTrue(b.accepts("bccc"))
        self.assertTrue(b.accepts("b"))
        self.assertTrue(b.accepts("111112"))
        self.assertTrue(b.accepts("2"))
        self.assertFalse(b.accepts(""))
        self.assertFalse(b.accepts("b12"))
        self.assertFalse(b.accepts("aaaccc"))
        self.assertFalse(b.accepts("111"))
        self.assertFalse(b.accepts("ab2"))

        a = Regex("a+b*c | d| e?f")
        b = a.dfa
        self.assertTrue(b.accepts("aaaabbbc"))
        self.assertTrue(b.accepts("aaaac"))
        self.assertTrue(b.accepts("ac"))
        self.assertTrue(b.accepts("d"))
        self.assertTrue(b.accepts("ef"))
        self.assertTrue(b.accepts("f"))
        self.assertFalse(b.accepts(""))
        self.assertFalse(b.accepts("bbbc"))
        self.assertFalse(b.accepts("ab"))
        self.assertFalse(b.accepts("eef"))

        a = Regex("a (b | c)* (d(e|f))+ | (g | h)?")
        b = a.dfa
        self.assertTrue(b.accepts("acbbccbccdedfdfde"))
        self.assertTrue(b.accepts("acccde"))
        self.assertTrue(b.accepts("adfdfdf"))
        self.assertTrue(b.accepts("g"))
        self.assertTrue(b.accepts("h"))
        self.assertTrue(b.accepts(""))
        self.assertFalse(b.accepts("abcbc"))
        self.assertFalse(b.accepts("bcde"))
        self.assertFalse(b.accepts("gh"))
        self.assertFalse(b.accepts("abcdeg"))

        a = Regex("(a | (b|c)+)*")
        b = a.dfa
        self.assertTrue(b.accepts("abcbcabcbcba"))
        self.assertTrue(b.accepts("aaaa"))
        self.assertTrue(b.accepts("bcabcabab"))
        self.assertTrue(b.accepts("abcbacba"))
        self.assertTrue(b.accepts(""))
        self.assertFalse(b.accepts("ddd"))

        a = Regex("a++++")
        b = a.dfa
        self.assertTrue(b.accepts("a"))
        self.assertTrue(b.accepts("aaaa"))
        self.assertFalse(b.accepts(""))

        a = Regex("a++*++?*")
        b = a.dfa
        self.assertTrue(b.accepts("a"))
        self.assertTrue(b.accepts("aaaa"))
        self.assertTrue(b.accepts(""))

if __name__ == "__main__":
    unittest.main()

