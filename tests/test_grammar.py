from itertools import combinations
import unittest

from cfg import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

        """
        productions = {
            "S": {"aA", "a", "bT", "b", "&"},
            "T": {"aA", "a", "bT", "b"},
            "A": {"aB", "a", "bT", "b"},
            "B": {"bT", "b"}
        }

        self.no_aaa = Grammar("S", productions)
        self.no_aaa_accept = ["", "a", "aa", "baa", 
            "aabbaa", "bababaab", "bbb"]
        self.no_aaa_reject = ["aaaba", "bbbbaaab", 
            "abaaa", "baaa", "aaa", "aaaa"]

        # L2 = {(b)* ^ #b's /3}
        productions = {
            "S": {"bB", "&"},
            "A": {"bB"},
            "B": {"bC"},
            "C": {"bA", "b"},
        }
        self.b_div_3 = Grammar("S", productions)
        self.b_div_3_accept = ["", "bbb", "bbbbbb"]
        self.b_div_3_reject = ["b", "bb", "bbbb", "bbbbb"]

        # L3 = {(a)* ^ #a's é par}
        productions = {
            "S": {"aB", "&"},
            "A": {"aB"},
            "B": {"aA", "a"},
        }
        self.even_a = Grammar("S", productions)
        self.even_a_accept = ["", "aa", "aaaa", "aaaaaa"]
        self.even_a_reject = ["a", "aaa", "aaaaa"]

        # L4 = {(0,1)* ^ x é bin /3}
        productions = {
            "S": {"0A", "1B", "0"},
            "A": {"0A", "1B", "0"},
            "B": {"0C", "1A", "1"},
            "C": {"0B", "1C"},
        }
        self.bin_3 = Grammar("S", productions)
        self.bin_3_accept = ["0", "11", "1001","1100"]
        self.bin_3_reject = ["", "1", "10", "100", "101", "111"]

    def check_strings(self, fa, accept, reject):
        for word in accept:
            self.assertTrue(fa.accepts(word))
        for word in reject:
            self.assertFalse(fa.accepts(word))

    """

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
    
    def test_fertile(self):
        # Caso simples
        g = """
        S -> aS | BC | BD
        A -> cC | AB
        C -> aA | BC
        B -> bB | &
        D -> dDd | c
        """
        gr = Grammar(g)
        n = {'S', 'B', 'D'}
        self.assertEqual(gr.fertile(), n)

        # Caso com G vazia
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC
        B -> bB
        """
        gr = Grammar(g)
        n = set()
        self.assertEqual(gr.fertile(), n)

        # caso com &
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC|&
        B -> bB|AB|&
        """
        gr = Grammar(g)
        n = {'S', 'A', 'C', 'B'}
        self.assertEqual(gr.fertile(), n)

        g = """
        S -> aS
        """
        gr = Grammar(g)
        n = set()
        self.assertEqual(gr.fertile(), n)

    def test_remove_infertile(self):
        # Caso simples
        g = """
        S -> aS | BC | BD
        A -> cC | AB
        C -> aA | BC
        B -> bB | &
        D -> dDd | c
        """
        gr = Grammar(g)
        f = """
        S -> a S | B D
        B -> & | b B
        D -> d D d | c
        """
        gf = Grammar(f)
        self.assertEqual(gr.remove_infertile(), gf)

        # Caso com G vazia
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC
        B -> bB
        """
        gr = Grammar(g)
        self.assertEqual(gr.remove_infertile(), Grammar())

        # caso com & e sem infertéis
        g = """
        S -> AC|CeB|Ba
        A -> aA|BC
        C -> cC|&
        B -> bB|AB|&
        """
        gr = Grammar(g)
        self.assertEqual(gr.remove_infertile(), gr)

if __name__ == "__main__":
    unittest.main()
