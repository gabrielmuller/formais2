import unittest
import copy
from rg import RegularGrammar
from nfa import NFA

class TestFA(unittest.TestCase):
    def setUp(self):
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

    def check_strings(self, fa, accept, reject):
        for word in accept:
            self.assertTrue(fa.accepts(word))
        for word in reject:
            self.assertFalse(fa.accepts(word))

    def test_grammar(self):
        fa = NFA.from_rg(self.no_aaa)
        self.check_strings(fa, self.no_aaa_accept,
            self.no_aaa_reject)
        print("Ran test_grammar")

    def test_conversion(self):
        # Faz GR -> NFA -> GR -> NFA
        fa = NFA.from_rg(self.no_aaa)
        
        gr = RegularGrammar.from_nfa(fa)

        fa = NFA.from_rg(gr)
        self.check_strings(fa, self.no_aaa_accept,
           self.no_aaa_reject)
        print("Ran test_conversion")

if __name__ == "__main__":
    unittest.main()
