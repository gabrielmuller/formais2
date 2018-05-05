from dfa import DFA
from nfa import NFA

def test_all():
    dfa_test_1()
    nfa_test_1()

def test_fa(dfa, accept, reject):
    for word in accept:
        assert dfa.accepts(word)
    for word in reject:
        assert not dfa.accepts(word)

def dfa_test_1():
    transitions = {
            "start" : {'a' : "one a", 'b' : "start"},
            "one a" : {'a' : "two a", 'b' : "start"},
            "two a" : {'b' : "start"}
            }


    no_aaa = DFA(transitions, "start", {"start", "one a", "two a"})

    test_fa(no_aaa, 
            ["", "a", "aa", "baa", "aabbaa", "bababaab"],
            ["aaaba", "bbbbaaab", "abaaa", "baaa", "aaa"] 
            )
    three = {"aab", "aba", "abb", "baa", "bab", "bba", "bbb"}
    assert no_aaa.words_of_size(3) == three

def nfa_test_1():
    transitions = {
            "start" : {'a': {"start", "one a"}, 'b': {"start"}},
            "one a" : {'a': {"two a"}}
            }
    ends_in_aa = NFA(transitions, "start", {"two a"})

    test_fa(ends_in_aa, 
            ["babaa", "baa", "aaaa", "aa", "bababaa", "aabaa"],
            ["baba", "aba", "aaba", "baaaaba", "bbbb", "aaab"]
            )
