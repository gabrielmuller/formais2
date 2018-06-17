import unittest
from cfg import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

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

        a = "S1->(*B*)|CbbH\nC->cC|&\nB->bbb"
        b = "S1 -> C b b H | ( * B  * ) \nC - > & | c C\nB ->bbb"
        self.assertEqual(Grammar(a), Grammar(b))

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

        g = """
        S -> AB
        A -> aA | aB
        B -> bBB
    """
        gr = Grammar(g)
        f = {'S': {'$'},
                'A': {'b'},
                'B': {'b', '$'}}
        self.assertEqual(gr.follow(), f)

        g = """
        E -> T E1
        E1 -> +T E1|&
        T -> F T1
        T1 -> *F T1 | &
        F -> (E) | id
    """
        gr = Grammar(g)
        f = {'E': {'$', ')'},
                'E1': {'$', ')'},
                'T' : {'+', '$', ')'},
                'T1': {'+', '$', ')'},
                'F' : {'*', '+', '$', ')'}}

        self.assertEqual(gr.follow(), f)

        g = """
            S -> ACB|Cbb|Ba
            A -> da|BC
            B-> g|&
            C-> h| &
    """
        gr = Grammar(g)
        f = {'S': {'$'},
            'A': {'h', 'g', '$'},
            'B': {'a', '$', 'h', 'g'},
            'C': {'b', 'g', '$', 'h'}}
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

    def test_simple(self):
        g = """
        S -> FGH
        F -> G | a
        G -> dG | H | b
        H -> c
    """
        gr = Grammar(g)
        nset = gr._simple_star()
        e = {"S": {'S'},
            "F": {'F', 'G', 'H'},
            "G": {'G', 'H'},
            "H": {'H'}}
        f = """
        S -> FGH
        F -> a | dG | b | c
        G -> dG | b | c
        H -> c
    """
        self.assertEqual(nset, e)
        self.assertEqual(Grammar(f), gr.rm_simple())

        g = """
        S -> a B c D e
        B -> b B | E | F
        D -> d D | F | d
        E -> e E | e
        F -> f F | f
    """
        gr = Grammar(g)
        nset = gr._simple_star()
        e = {"S": {'S'},
            "B": {'B', 'E', 'F'},
            "D": {'D', 'F'},
            "E": {'E'},
            "F": {'F'}}
        f = """
        S -> a B c D e
        B -> b B | e E | e | f F | f
        D -> d D | d | f F | f
        E -> e E | e
        F -> f F | f
    """
        self.assertEqual(nset, e)
        self.assertEqual(Grammar(f), gr.rm_simple())

if __name__ == "__main__":
    unittest.main()
