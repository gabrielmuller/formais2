import unittest
from parser import *

class TestParser(unittest.TestCase):
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
        a = parse('wx(y () z)*')
        self.assertEqual(a.value, '.')
        self.assertEqual(a.left.value, '.')
        self.assertEqual(a.left.left.value, 'w')
        self.assertEqual(a.left.right.value, 'x')
        self.assertEqual(a.right.value, '*')
        self.assertEqual(a.right.left.value, '.')
        self.assertEqual(a.right.left.left.value, 'y')
        self.assertEqual(a.right.left.right.value, 'z')

if __name__ == "__main__":
    unittest.main()

