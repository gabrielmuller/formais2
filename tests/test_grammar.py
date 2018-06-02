from itertools import combinations
import unittest
import copy

from rg import RegularGrammar
from nfa import NFA

class TestFA(unittest.TestCase):
    def setUp(self):
        print('Running ' + self._testMethodName)
        # L1 = {(a,b)* ^ no "aaa"}
        productions = {
            "S": {"aA", "a", "bT", "b", "&"},
            "T": {"aA", "a", "bT", "b"},
            "A": {"aB", "a", "bT", "b"},
            "B": {"bT", "b"}
        }

        self.no_aaa = RegularGrammar("S", productions)
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
        self.b_div_3 = RegularGrammar("S", productions)
        self.b_div_3_accept = ["", "bbb", "bbbbbb"]
        self.b_div_3_reject = ["b", "bb", "bbbb", "bbbbb"]

        # L3 = {(a)* ^ #a's é par}
        productions = {
            "S": {"aB", "&"},
            "A": {"aB"},
            "B": {"aA", "a"},
        }
        self.even_a = RegularGrammar("S", productions)
        self.even_a_accept = ["", "aa", "aaaa", "aaaaaa"]
        self.even_a_reject = ["a", "aaa", "aaaaa"]

        # L4 = {(0,1)* ^ x é bin /3}
        productions = {
            "S": {"0A", "1B", "0"},
            "A": {"0A", "1B", "0"},
            "B": {"0C", "1A", "1"},
            "C": {"0B", "1C"},
        }
        self.bin_3 = RegularGrammar("S", productions)
        self.bin_3_accept = ["0", "11", "1001","1100"]
        self.bin_3_reject = ["", "1", "10", "100", "101", "111"]

    def check_strings(self, fa, accept, reject):
        for word in accept:
            self.assertTrue(fa.accepts(word))
        for word in reject:
            self.assertFalse(fa.accepts(word))

    def test_grammar(self):
        fa = NFA.from_rg(self.no_aaa)
        self.check_strings(fa, self.no_aaa_accept,
            self.no_aaa_reject)
        fa = NFA.from_rg(self.b_div_3)
        self.check_strings(fa, self.b_div_3_accept,
            self.b_div_3_reject)
        fa = NFA.from_rg(self.even_a)
        self.check_strings(fa, self.even_a_accept,
            self.even_a_reject)
        fa = NFA.from_rg(self.bin_3)
        self.check_strings(fa, self.bin_3_accept,
            self.bin_3_reject)

    def test_conversion(self):
        # Faz GR -> NFA -> GR -> NFA
        fa = NFA.from_rg(self.no_aaa)
        
        gr = RegularGrammar.from_nfa(fa)

        fa = NFA.from_rg(gr)
        self.check_strings(fa, self.no_aaa_accept,
           self.no_aaa_reject)

    def test_union(self):
        union = self.b_div_3.union(self.even_a)
        union_accept = list(set().union(self.b_div_3_accept,
            self.even_a_accept))
        union_reject = list(set().union(self.b_div_3_reject,
            self.even_a_reject))
        fa = NFA.from_rg(union)
        self.check_strings(fa, union_accept,
           union_reject)

    def test_concatenation(self):
        concat = self.b_div_3.concatenation(self.even_a)
        
        concat_words = []
        for i in self.b_div_3_accept:
            for j in self.even_a_accept:
                concat_words.append(i+j)

        concat_accept = list(set().union(self.b_div_3_accept,
            self.even_a_accept, concat_words))

        concat_words = []
        for i in self.b_div_3_reject:
            for j in self.even_a_reject:
                concat_words.append(i+j)

        concat_reject = list(set().union(self.b_div_3_reject,
            self.even_a_reject,concat_words))
        fa = NFA.from_rg(concat)
        self.check_strings(fa, concat_accept,
           concat_reject)

    def test_kleene(self):
        kleene = self.bin_3.kleene_closure()
        kleene_words = [x+y for (x,y) in combinations(self.bin_3_accept, 2)]
        kleene_words = list(set().union(self.bin_3_accept,
            kleene_words))
        if "" in self.bin_3_reject: self.bin_3_reject.remove("")
        fa = NFA.from_rg(kleene)
        self.check_strings(fa, kleene_words,
            self.bin_3_reject)

if __name__ == "__main__":
    unittest.main()
