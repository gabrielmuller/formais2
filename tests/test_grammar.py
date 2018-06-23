import unittest
from cfg import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)

    def test_from_to_str(self):
        # Testes antigos
        a = "S  -> a a a a a S18 S18\n\n  S18 -> b b b"
        r = Grammar(a)
        c  = str(r)
        b = "S -> a a a a a S18 S18\nS18 -> b b b"
        self.assertEqual(b, c)

        a = "S1->a S1 b S45 A99\nS45  ->  &"
        r = Grammar(a)
        c  = str(r)
        b = "S1 -> a S1 b S45 A99\nS45 -> &"
        self.assertEqual(b, c)

        a = "S1->( * B * ) | C b b H\nC-> c C | &\nB->b b b"
        b = "S1 -> C b b H | ( * B  * ) \nC -> & | c C\nB ->b b b"
        self.assertEqual(Grammar(a), Grammar(b))

    def test_first(self):
        # caso com linguagem vazia
        g = """
        S -> S S | A
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
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C
        B -> b B
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
        S -> A C | C e B | B a | Z a | Z
        A -> a A | B C
        C -> c C
        B -> b B
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
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C
        B -> b B | A B
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
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C | &
        B -> b B | A B | &
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
        S -> A B C
        A -> a A | &
        B -> b B | A C d
        C -> c C | &
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
        S -> A B C
        A -> a A | &
        B -> b B | A C d | A H A H A
        C -> c C | &
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
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C | &
        B -> b B | A B | &
    """
        gr = Grammar(g)
        f = {'S': {'$'},
                'A': {'c', 'a', 'b', '$'},
                'C': {'e', '$', 'a', 'b', 'c'},
                'B': {'a', 'c', '$', 'b'}}
        self.assertEqual(gr.follow(), f)

        g = """
        S -> A B
        A -> a A | a B
        B -> b B B
    """
        gr = Grammar(g)
        f = {'S': {'$'},
                'A': {'b'},
                'B': {'b', '$'}}
        self.assertEqual(gr.follow(), f)

        g = """
        E -> T E1
        E1 -> + T E1|&
        T -> F T1
        T1 -> * F T1 | &
        F -> ( E ) | id
    """
        gr = Grammar(g)
        f = {'E': {'$', ')'},
                'E1': {'$', ')'},
                'T' : {'+', '$', ')'},
                'T1': {'+', '$', ')'},
                'F' : {'*', '+', '$', ')'}}

        self.assertEqual(gr.follow(), f)

        g = """
            S -> A C B | C b b | B a
            A -> d a | B C
            B-> g | &
            C-> h | &
    """
        gr = Grammar(g)
        f = {'S': {'$'},
            'A': {'h', 'g', '$'},
            'B': {'a', '$', 'h', 'g'},
            'C': {'b', 'g', '$', 'h'}}
        self.assertEqual(gr.follow(), f)

    def test_nullable(self):
        g = """
        S -> A B C | z z
        A -> a A | a
        B -> b B | A C d | H
        C -> c C | c
    """
        gr = Grammar(g)
        n = set()
        self.assertEqual(gr.nullable(), n)

        g = """
        S -> A B C | z z
        A -> a A | a
        B -> b B | A C d | H
        C -> c C | &
    """
        gr = Grammar(g)
        n = {'C'}
        self.assertEqual(gr.nullable(), n)

        g = """
        S -> A B C H | z z
        A -> a A | &
        B -> b B | A C | H
        C -> c C | &
    """
        gr = Grammar(g)
        n = {'C', 'A', 'B'}
        self.assertEqual(gr.nullable(), n)

        g = """
        S -> A B C| z z
        A -> a A | &
        B -> b B | A C | H
        C -> c C | &
    """
        gr = Grammar(g)
        n = {'S', 'A', 'B', 'C'}
        self.assertEqual(gr.nullable(), n)
        
        g = """
        X -> a b c | B a b c
        A -> B A | &
        B -> A A | b
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
        S -> A B
        A -> a A | &
        B -> b B | &
    """
        gr = Grammar(g)
        e = """
        S' -> S | &
        S -> A B | A | B
        A -> a A | a
        B -> b B | b
    """
        er = Grammar(e)
        self.assertEqual(gr.epsilon_free(), er)

        g = """
        S -> A z B z A
        A -> B B | a
        B -> b B | &
    """
        gr = Grammar(g)
        e = """
        S -> A z B z A | A z B z | A z z A | A z z | z B z A | z B z | z z A | z z
        A -> B B | B | a
        B -> b B | b
    """
        er = Grammar(e)
        self.assertEqual(gr.epsilon_free(), er)
    
    def test_fertile(self):
        # Caso simples
        g = """
        S -> a S | B C | B D
        A -> c C | A B
        C -> a A | B C
        B -> b B | &
        D -> d D d | c
        """
        gr = Grammar(g)
        n = {'S', 'B', 'D'}
        self.assertEqual(gr.fertile(), n)

        # Caso com G vazia
        g = """
        S -> A C|C e B|B a
        A -> a A | B C
        C -> c C
        B -> b B
        """
        gr = Grammar(g)
        n = set()
        self.assertEqual(gr.fertile(), n)

        # caso com &
        g = """
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C | &
        B -> b B | A B | &
        """
        gr = Grammar(g)
        n = {'S', 'A', 'C', 'B'}
        self.assertEqual(gr.fertile(), n)

        g = """
        S -> a S
        """
        gr = Grammar(g)
        n = set()
        self.assertEqual(gr.fertile(), n)

    def test_remove_infertile(self):
        # Caso simples
        g = """
        S -> a S | B C | B D
        A -> c C | A B
        C -> a A | B C
        B -> b B | &
        D -> d D d | c
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
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C
        B -> b B
        """
        gr = Grammar(g)
        self.assertEqual(gr.remove_infertile(), Grammar())

        # caso com & e sem infertéis
        g = """
        S -> A C | C e B | B a
        A -> a A | B C
        C -> c C | &
        B -> b B | A B | &
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
        S -> F G H
        F -> G | a
        G -> d G | H | b
        H -> c
    """
        gr = Grammar(g)
        nset = gr._simple_star()
        e = {"S": {'S'},
            "F": {'F', 'G', 'H'},
            "G": {'G', 'H'},
            "H": {'H'}}
        f = """
        S -> F G H
        F -> a | d G | b | c
        G -> d G | b | c
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

    def test_is_factored(self):
        # exemplo de fatoravel
        g = """
            S -> a S | a B | d S
            B -> b B | b
            """
        gr = Grammar(g)

        self.assertFalse(gr.is_factored())

        # exemplo de fatorada
        g = """
            S  -> a S' | d S
            S' -> S | B
            B  -> b B'
            B' -> B | & 
            """
        gr = Grammar(g)

        self.assertTrue(gr.is_factored())

        #exemplo de nao fatoravel indireta
        g = """
            S -> a S | A
            A -> a A c | &
            """
        gr = Grammar(g)

        self.assertFalse(gr.is_factored())

    def test_factorate(self):
        # exemplo de fatoravel
        g = """
            S -> a S | a B | d S
            B -> b B | b
            """
        gr = Grammar(g)
        g = """
            S  -> a S' | d S
            S' -> S | B
            B  -> b B'
            B' -> B | & 
            """
        gf = Grammar(g)
        self.assertEqual(gr.factor(), gf)

        #exemplo de fatoravel indireta em 1 passo
        g = """
        S -> a | A
        A -> a | a A
        """
        gr = Grammar(g)
        g = """
            S  -> a S'
            S' -> A | &
            A  -> a A'
            A' -> A | &
        """
        gf = Grammar(g)
        self.assertEqual(gr.factor_in_steps(1), gf)

        #exemplo de não fatoravel indireta
        g = """ 
            S -> a S | A
            A -> a A c | &
        """
        gr = Grammar(g)
        g = """
            S -> a S' | &
            S' -> & | a S'' | c
            S'' -> A c c | S'
            A -> & | a A c
        """
        gf = Grammar(g)
        self.assertEqual(gr.factor_in_steps(2), gf)

        g = """
            S -> S a | b | c
        """
        gr = Grammar(g)
        g = """
            S -> b S' | c S' | S a a
            S' -> & | a
        """
        gf = Grammar(g)
        self.assertEqual(gr.factor_in_steps(1), gf)

    def test_has_left_recursion(self):
        # G com recursão direta
        g = """
            S -> S a | b | c
            """
        gr = Grammar(g)
        self.assertTrue(gr.has_direct_left_recursion())
        self.assertFalse(gr.has_indirect_left_recursion())
        # G com recursão direta e indireta
        g = """
            S -> A a | S b
            A -> S c | d
            """
        gr = Grammar(g)
        self.assertTrue(gr.has_direct_left_recursion())
        self.assertTrue(gr.has_indirect_left_recursion())
        # G sem recursão
        g = """
            S -> aS | b | c
            """
        gr = Grammar(g)
        self.assertFalse(gr.has_direct_left_recursion())
        self.assertFalse(gr.has_indirect_left_recursion())

    def test_remove_left_recursion(self):
        g = """
            S -> A a | S b
            A -> S c | d
            """
        gr = Grammar(g)
        g = """
            S -> A a S'
            A' -> & | a S' c A'
            S' -> b S' | &
            A -> d A'
            """
        gf = Grammar(g)
        self.assertEqual(gr.remove_left_recursion(), gf)

    def test_is_proper(self):
        g = """
        S -> S a | b | c
        """
        gr = Grammar(g)
        self.assertTrue(gr.is_proper())
        # G com produção simples
        g = """
        S -> A a | S b
        A -> S c | d | S
        """
        gr = Grammar(g)
        self.assertFalse(gr.is_proper())
        # G não &-livre
        g = """
        S -> A a | S b
        A -> S c | d | &
        """
        gr = Grammar(g)
        self.assertFalse(gr.is_proper())
        # G com símbolos inúteis
        g = """
        S -> A a | S b
        A -> S c | d 
        B -> bB
        """
        gr = Grammar(g)
        self.assertFalse(gr.is_proper())




if __name__ == "__main__":
    unittest.main()
