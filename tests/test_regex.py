import unittest
from regex import Regex, Node

class TestRegex(unittest.TestCase):
    def setUp(self):
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

    '''
    def test_simone(self):
        dfa_abaca = self.abaca.simone()
        dfa_ab = self.ab.simone()
        self.assertTrue(dfa_abaca.accepts("aba"))
        self.assertTrue(dfa_abaca.accepts("abaca"))
        self.assertTrue(dfa_abaca.accepts("abacababaca"))
        self.assertFalse(dfa_abaca.accepts("abacababacab"))
        self.assertFalse(dfa_abaca.accepts("cababacab"))
        self.assertFalse(dfa_abaca.accepts("a"))

        self.assertTrue(dfa_ab.accepts("ab"))
        self.assertFalse(dfa_ab.accepts(""))
        self.assertFalse(dfa_ab.accepts("a"))
        self.assertFalse(dfa_ab.accepts("b"))
    '''

    def test_parse_simone(self):
        p = Regex("a")
        l = p.dfa
        self.assertTrue(l.accepts("a"))
        self.assertFalse(l.accepts(""))
        self.assertFalse(l.accepts("aa"))

        e = Regex("")
        f = e.dfa
        self.assertFalse(f.accepts(""))
        self.assertFalse(f.accepts("a"))

        r = Regex("ab|cde | f |   g")
        m = r.dfa
        self.assertTrue(m.accepts("ab"))
        self.assertTrue(m.accepts("cde"))
        self.assertTrue(m.accepts("f"))
        self.assertTrue(m.accepts("g"))
        self.assertFalse(m.accepts(""))
        self.assertFalse(m.accepts("a"))
        self.assertFalse(m.accepts("abcde"))
        self.assertFalse(m.accepts("fg"))

        q = Regex("a*bc* | 1*2")
        n = q.dfa
        self.assertTrue(n.accepts("ab"))
        self.assertTrue(n.accepts("aaaaabcc"))
        self.assertTrue(n.accepts("bccc"))
        self.assertTrue(n.accepts("b"))
        self.assertTrue(n.accepts("111112"))
        self.assertTrue(n.accepts("2"))
        self.assertFalse(n.accepts(""))
        self.assertFalse(n.accepts("b12"))
        self.assertFalse(n.accepts("aaaccc"))
        self.assertFalse(n.accepts("111"))
        self.assertFalse(n.accepts("ab2"))

        s = Regex("a+b*c | d| e?f")
        o = s.dfa
        self.assertTrue(o.accepts("aaaabbbc"))
        self.assertTrue(o.accepts("aaaac"))
        self.assertTrue(o.accepts("ac"))
        self.assertTrue(o.accepts("d"))
        self.assertTrue(o.accepts("ef"))
        self.assertTrue(o.accepts("f"))
        self.assertFalse(o.accepts(""))
        self.assertFalse(o.accepts("bbbc"))
        self.assertFalse(o.accepts("ab"))
        self.assertFalse(o.accepts("eef"))

        t = Regex("a (b | c)* (d(e|f))+ | (g | h)?")
        a = t.dfa
        self.assertTrue(a.accepts("acbbccbccdedfdfde"))
        self.assertTrue(a.accepts("acccde"))
        self.assertTrue(a.accepts("adfdfdf"))
        self.assertTrue(a.accepts("g"))
        self.assertTrue(a.accepts("h"))
        self.assertTrue(a.accepts(""))
        self.assertFalse(a.accepts("abcbc"))
        self.assertFalse(a.accepts("bcde"))
        self.assertFalse(a.accepts("gh"))
        self.assertFalse(a.accepts("abcdeg"))



if __name__ == "__main__":
    unittest.main()

