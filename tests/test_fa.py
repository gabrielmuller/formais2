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

    def check_strings(self, fa, accept, reject):
        for word in accept:
            self.assertTrue(fa.accepts(word))
        for word in reject:
            self.assertFalse(fa.accepts(word))

    def test_dfa_accept(self):
        self.check_strings(self.no_aaa, 
                ["", "a", "aa", "baa", "aabbaa", "bababaab"],
                ["aaaba", "bbbbaaab", "abaaa", "baaa", "aaa"] 
                )

    def test_dfa_strings_of_size(self):
        three = {"aab", "aba", "abb", "baa", "bab", "bba", "bbb"}
        self.assertEqual(self.no_aaa.words_of_size(3), three)

    def test_nfa_accepts(self):
        self.check_strings(self.ends_in_aa, 
                ["babaa", "baa", "aaaa", "aa", "bababaa", "aabaa"],
                ["baba", "aba", "aaba", "baaaaba", "bbbb", "aaab"]
                )

if __name__ == "__main__":
    unittest.main()
