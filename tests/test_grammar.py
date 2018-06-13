from itertools import combinations
import unittest

from glc import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)
        # L1 = {(a,b)* ^ no "aaa"}
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

    """

    Análise não foi implementada ainda...
    def test_grammar(self):
        fa = NFA.from_glc(self.no_aaa)
        self.check_strings(fa, self.no_aaa_accept,
            self.no_aaa_reject)
        fa = NFA.from_glc(self.b_div_3)
        self.check_strings(fa, self.b_div_3_accept,
            self.b_div_3_reject)
        fa = NFA.from_glc(self.even_a)
        self.check_strings(fa, self.even_a_accept,
            self.even_a_reject)
        fa = NFA.from_glc(self.bin_3)
        self.check_strings(fa, self.bin_3_accept,
            self.bin_3_reject)
    """

if __name__ == "__main__":
    unittest.main()
