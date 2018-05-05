import unittest
from dfa import DFA
from nfa import NFA

class TestFA(unittest.TestCase):
    def setUp(self):
        transitions = {
                "start" : {'a' : "one a", 'b' : "start"},
                "one a" : {'a' : "two a", 'b' : "start"},
                "two a" : {'b' : "start"}
                }


        self.no_aaa = DFA(transitions, "start", {"start", "one a", "two a"})

        transitions = {
                "start" : {'a': {"start", "one a"}, 'b': {"start"}},
                "one a" : {'a': {"two a"}}
                }
        self.ends_in_aa = NFA(transitions, "start", {"two a"})

        self.no_aaa_accept = ["", "a", "aa", "baa", "aabbaa", "bababaab"]
        self.no_aaa_reject = ["aaaba", "bbbbaaab", "abaaa", "baaa", "aaa"] 
        self.ends_in_aa_accept = ["babaa", "baa", "aaaa",
                "aa", "bababaa", "aabaa"]
        self.ends_in_aa_reject = ["baba", "aba", "aaba",
                "baaaaba", "bbbb", "aaab"]
    def check_strings(self, fa, accept, reject):
        for word in accept:
            self.assertTrue(fa.accepts(word))
        for word in reject:
            self.assertFalse(fa.accepts(word))

    def test_dfa_accept(self):
        self.check_strings(self.no_aaa, self.no_aaa_accept,
                self.no_aaa_reject)

    def test_dfa_strings_of_size(self):
        three = {"aab", "aba", "abb", "baa", "bab", "bba", "bbb"}
        self.assertEqual(self.no_aaa.words_of_size(3), three)

    def test_nfa_accepts(self):
        self.check_strings(self.ends_in_aa, self.ends_in_aa_accept,
                self.ends_in_aa_reject)

    def test_determinize(self):
        det = self.ends_in_aa.determinize()
        self.check_strings(det, self.ends_in_aa_accept,
                self.ends_in_aa_reject)

if __name__ == "__main__":
    unittest.main()
