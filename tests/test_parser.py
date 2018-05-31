import unittest
from parser import *

class TestParser(unittest.TestCase):
    def setUp(self):
        return

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

if __name__ == "__main__":
    unittest.main()

