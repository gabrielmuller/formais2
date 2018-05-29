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
        self.ab = Regex('hello')

        self.ab.root = Node('.')
        self.ab.root.left = Node('a')
        self.ab.root.right = Node('b')

        self.ab.thread()

        # (ab | ac)* a
        self.abaca = Regex('oi')

        n = Node('|')
        n.left = Node('.')
        n.right = Node('.')
        n.left.left = Node('a')
        n.left.right = Node('b')
        n.right.left = Node('a')
        n.right.right = Node('c')

        r = Node('.')
        r.left = Node('*')
        r.right = Node('a')
        r.left.left = n

        self.abaca.root = r

        self.abaca.thread()

        self.abaca.simone()

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


if __name__ == "__main__":
    unittest.main()

