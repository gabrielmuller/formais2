import unittest
from regex import Regex, Node

class TestRegex(unittest.TestCase):
    def setUp(self):
        # 'ab' apenas
        self.ab = Regex('hello')

        self.ab.root = Node('.')
        self.ab.root.left = Node('a')
        self.ab.root.right = Node('b')

        # (ab | ac)* a
        self.abaca = Regex('oi')

        n = Node('|')
        n.left = Node('.')
        n.right = Node('.')
        n.left.left = Node('a')
        n.left.right = Node('b')
        n.right.left = Node('a')
        n.right.right = Node('b')

        r = Node('.')
        r.left = Node('*')
        r.right = Node('a')
        r.left.left = n

        r.left.right = r
        n.left.left.right = n.left
        n.left.right.right = n
        n.right.left.right = n.right
        n.right.right.right = r.left
        r.right.right = '&'

        self.abaca.root = r

    def test_is_operator(self):
        self.assertTrue(self.ab.root.is_operator())
        self.assertFalse(self.ab.root.left.is_operator())
        self.assertFalse(self.ab.root.right.is_operator())
        
        self.assertTrue(self.abaca.root.left.left.left.is_operator())
        self.assertTrue(self.abaca.root.left.right.left.right.is_operator())
        self.assertFalse(self.abaca.root.right.is_operator())

if __name__ == "__main__":
    unittest.main()

