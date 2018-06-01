import unittest
import copy
from nfa import NFA

class TestFA(unittest.TestCase):
    def setUp(self):
        # L1 = {(a,b)* ^ no "aaa"} DFA Incompleto
        transitions = {
            "S" : {'a' : {"A"}, 'b' : {"S"}},
            "A" : {'a' : {"B"}, 'b' : {"S"}},
            "B" : {'b' : {"S"}}
        }

        self.no_aaa = NFA(transitions, "S", {"S", "A", "B"})
        self.no_aaa_accept = ["", "a", "aa", "baa", 
            "aabbaa", "bababaab", "bbb"]
        self.no_aaa_reject = ["aaaba", "bbbbaaab", 
            "abaaa", "baaa", "aaa", "aaaa"]

        # L2 = {(a,b)* ^ no "bbb"} DFA Incompleto
        transitions = {
            "S" : {'a' : {"S"}, 'b' : {"A"}},
            "A" : {'a' : {"S"}, 'b' : {"B"}},
            "B" : {'a' : {"S"}}
        }
        self.no_bbb = NFA(transitions, "S", {"S", "A", "B"})
        self.no_bbb_accept = ["", "b", "bb", "abb",
            "bbaabb", "abababba", "aaa"]
        self.no_bbb_reject = ["bbbab", "aaaabbba",
            "babbb", "abbb", "bbb", "bbbb"]

        # L3 = {(a,b)* ^ termina com "aa"} NFA Incompleto
        transitions = {
            "S" : {'a' : {"S", "A"}, 'b' : {"S"}},
            "A" : {'a' : {"B"}},
            "B" : {}
        }
        self.ends_in_aa = NFA(transitions, "S", {"B"})
        self.ends_in_aa_accept = ["babaa", "baa", "aaaa",
                "aa", "bababaa", "aabaa"]
        self.ends_in_aa_reject = ["baba", "aba", "aaba",
                "baaaaba", "bbbb", "aaab"]

    def check_strings(self, fa, accept, reject):
        for word in accept:
            self.assertTrue(fa.accepts(word))
        for word in reject:
            self.assertFalse(fa.accepts(word))

    def test_fa(self):
        self.check_strings(self.no_aaa, self.no_aaa_accept,
            self.no_aaa_reject)
        self.check_strings(self.no_bbb, self.no_bbb_accept,
            self.no_bbb_reject)
        print("Ran test_fa")

    def test_is_dfa(self):
        self.assertTrue(self.no_aaa.is_dfa())
        self.assertTrue(self.no_bbb.is_dfa())
        self.assertFalse(self.ends_in_aa.is_dfa())
        print("Ran test_is_dfa")

    def test_determinize(self):
        det = copy.deepcopy(self.ends_in_aa)
        det.determinize()
        self.check_strings(det, self.ends_in_aa_accept,
            self.ends_in_aa_reject)
        print("Ran test_determinize")

    def test_complete(self):
        # Completar um DFA
        complete_1 = copy.deepcopy(self.no_aaa)
        complete_1.complete()
        self.check_strings(complete_1, self.no_aaa_accept,
            self.no_aaa_reject)

        #Completar um NFA
        complete_3 = copy.deepcopy(self.ends_in_aa)
        complete_3.complete()
        self.check_strings(complete_3, self.ends_in_aa_accept,
            self.ends_in_aa_reject)
        print("Ran test_complete")

    def test_complement(self):
        complement_1 = copy.deepcopy(self.no_aaa)
        complement_1.complement()
        self.check_strings(complement_1, 
                self.no_aaa_reject,
                self.no_aaa_accept)

        complement_2 = copy.deepcopy(self.no_bbb)
        complement_2.complement()
        self.check_strings(complement_2, 
                self.no_bbb_reject,
                self.no_bbb_accept)

        complement_3 = copy.deepcopy(self.ends_in_aa)
        complement_3.complement()
        self.check_strings(complement_3, 
                self.ends_in_aa_reject,
                self.ends_in_aa_accept)
        print("Ran test_complement")

    def test_union(self):
        # União de dois DFA incompletos
        union_1 = self.no_aaa.union(self.no_bbb)
        union_1_accepts = list(set().union(self.no_aaa_accept,
            self.no_bbb_accept))
        union_1_rejects = ["aaabbb", "abbbaaa"]
        self.check_strings(union_1, union_1_accepts,
            union_1_rejects)

        # União de DFA e NFA incompletos
        union_2 = self.no_aaa.union(self.ends_in_aa)
        #union_2.printer()
        union_2_accepts = list(set().union(self.no_aaa_accept,
            self.ends_in_aa_accept))
        union_2_rejects = ["aaab", "aaabb", "aaaba"]
        self.check_strings(union_2, union_2_accepts,
            union_2_rejects)
        
        print("Ran test_union")

    def test_rename(self):
        renamed_1 = copy.deepcopy(self.no_aaa)
        renamed_1.rename_states(0)
        self.check_strings(renamed_1, self.no_aaa_accept,
            self.no_aaa_reject)

        renamed_2 = copy.deepcopy(self.ends_in_aa)
        renamed_2.rename_states(0)
        self.check_strings(renamed_2, self.ends_in_aa_accept,
            self.ends_in_aa_reject)
        print("Ran test_rename")
        

if __name__ == "__main__":
    unittest.main()
