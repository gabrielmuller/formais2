from itertools import combinations
import unittest

from cfg import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

    # não testa '|' porque não é possível determinar a ordem.
    def test_from_to_str(self):
        a = "S  -> aaaaaS18S18\n\n  S18 - > bbb"
        r = Grammar(a)
        c  = str(r)
        b = "S -> a a a a a S18 S18\nS18 -> b b b"
        self.assertEqual(b, c)

        a = "S1->aS1bS45A99\nS45  ->  &"
        r = Grammar(a)
        c  = str(r)
        b = "S1 -> a S1 b S45 A99\nS45 -> &"
        self.assertEqual(b, c)

    def test_first(self):
        # caso com linguagem vazia
        g = """
        S -> SS | A
    """
        gr = Grammar(g)
        f = {'S': set(),
                'A': set()}
        fnt = {'S': {'S', 'A'},
                'A': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

        # caso simples
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC
        B -> bB
    """
        gr = Grammar(g)
        f = {'S': {'a', 'b', 'c'},
                'A': {'a', 'b'},
                'C': {'c'},
                'B': {'b'}}
        fnt = {'S': {'A', 'B', 'C'},
                'A': {'B'},
                'B': set(),
                'C': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

        # caso com NTs sem produções
        g = """
        S -> AC|CeB|Ba|Za|Z
        A -> aA|BC
        C -> cC
        B -> bB
    """
        gr = Grammar(g)
        f = {'S': {'a', 'b', 'c'},
                'A': {'a', 'b'},
                'C': {'c'},
                'B': {'b'},
                'Z': set()}
        fnt = {'S': {'A', 'B', 'C', 'Z'},
                'A': {'B'},
                'B': set(),
                'C': set(),
                'Z': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

        # caso com firsts equivalentes (A e B)
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC
        B -> bB|AB
    """
        gr = Grammar(g)
        f = {'S': {'a', 'b', 'c'},
                'A': {'a', 'b'},
                'C': {'c'},
                'B': {'a', 'b'}}
        fnt = {'S': {'A', 'B', 'C'},
                'A': {'A', 'B'},
                'B': {'A', 'B'},
                'C': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

        # caso com &
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC|&
        B -> bB|AB|&
    """
        gr = Grammar(g)
        f = {'S': {'a', 'b', 'c', 'e', '&'},
                'A': {'a', 'b', 'c', '&'},
                'C': {'c', '&'},
                'B': {'a', 'b', 'c', '&'}}
        fnt = {'S': {'A', 'B', 'C'},
                'A': {'A', 'B', 'C'},
                'B': {'A', 'B', 'C'},
                'C': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

        g = """
        S -> ABC
        A -> aA|&
        B -> bB|ACd
        C -> cC|&
    """
        gr = Grammar(g)
        f = {'S': {'a', 'b', 'c', 'd'},
                'A': {'a', '&'},
                'B': {'a', 'b', 'c', 'd'},
                'C': {'c', '&'}}
        fnt = {'S': {'A', 'B', 'C'},
                'A': set(),
                'B': {'A', 'C'},
                'C': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

        g = """
        S -> ABC
        A -> aA|&
        B -> bB|ACd|AHAHA
        C -> cC|&
    """
        gr = Grammar(g)
        f = {'S': {'a', 'b', 'c', 'd'},
                'A': {'a', '&'},
                'B': {'a', 'b', 'c', 'd'},
                'C': {'c', '&'},
                'H': set()}
        fnt = {'S': {'A', 'B', 'C', 'H'},
                'A': set(),
                'B': {'A', 'C', 'H'},
                'C': set(),
                'H': set()}
        self.assertEqual(gr.first(), f)
        self.assertEqual(gr.first_nt(), fnt)

    def test_follow(self):
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC|&
        B -> bB|AB|&
    """
        gr = Grammar(g)
        f = {'S': {'$'},
                'A': {'c', 'a', 'b', '$'},
                'C': {'e', '$', 'a', 'b', 'c'},
                'B': {'a', 'c', '$', 'b'}}
        self.assertEqual(gr.follow(), f)
    def test_nullable(self):
        g = """
        S -> ABC|zz
        A -> aA|a
        B -> bB|ACd|H
        C -> cC|c
    """
        gr = Grammar(g)
        n = set()
        self.assertEqual(gr.nullable(), n)

        g = """
        S -> ABC|zz
        A -> aA|a
        B -> bB|ACd|H
        C -> cC|&
    """
        gr = Grammar(g)
        n = {'C'}
        self.assertEqual(gr.nullable(), n)

        g = """
        S -> ABCH|zz
        A -> aA|&
        B -> bB|AC|H
        C -> cC|&
    """
        gr = Grammar(g)
        n = {'C', 'A', 'B'}
        self.assertEqual(gr.nullable(), n)

        g = """
        S -> ABC|zz
        A -> aA|&
        B -> bB|AC|H
        C -> cC|&
    """
        gr = Grammar(g)
        n = {'S', 'A', 'B', 'C'}
        self.assertEqual(gr.nullable(), n)
        
        g = """
        X -> abc | Babc
        A -> BA | &
        B -> AA | b
    """
        gr = Grammar(g)
        n = {'A', 'B'}
        self.assertEqual(gr.nullable(), n)

    def test_combinations(self):
        l = [8, 9, 'foo']
        c = [[], ['foo'], [9], [9, 'foo'], [8],
            [8, 'foo'], [8, 9], [8, 9, 'foo']]
        self.assertEqual(Grammar._combinations(l), c)

        l = [9]
        c = [[], [9]]
        self.assertEqual(Grammar._combinations(l), c)

        l = []
        c = [[]]
        self.assertEqual(Grammar._combinations(l), c)
    def test_epsilon_free(self):
        g = """
        S -> AB
        A -> aA | &
        B -> bB | &
    """
        gr = Grammar(g)
        e = """
        S1 -> S | &
        S -> AB | A | B
        A -> aA | a
        B -> bB | b
    """
        er = Grammar(e)
        self.assertEqual(gr.epsilon_free(), er)

        g = """
        S -> AzBzA
        A -> BB | a
        B -> bB | &
    """
        gr = Grammar(g)
        e = """
        S -> AzBzA | AzBz | AzzA | Azz | zBzA | zBz | zzA | zz
        A -> BB | B | a
        B -> bB | b
    """
        er = Grammar(e)
        self.assertEqual(gr.epsilon_free(), er)

    def test_unreachable(self):
        g = """
        S -> a S a | d D d       
        A -> a B | C c | a        
        B -> d D | b B | b
        C -> A a | d D | c
        D -> b b B | d     
    """
        gr = Grammar(g)
        e = """
        S -> a S a | d D d       
        B -> d D | b B | b
        D -> b b B | d     
    """
        er = Grammar(e)
        self.assertEqual(gr.rm_unreachable(), er)

if __name__ == "__main__":
    unittest.main()
