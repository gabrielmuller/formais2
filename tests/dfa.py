from dfa import DFA
def test_dfa(dfa, accept, reject):
    for word in accept:
        assert dfa.accepts(word)
    for word in reject:
        assert not dfa.accepts(word)

def test_all():
    transitions = {
        ("start", 'a') : "one a",
        ("one a", 'a') : "two a",
        ("start", 'b') : "start",
        ("one a", 'b') : "start",
        ("two a", 'b') : "start"
        }

    no_aaa = DFA(transitions, "start", {"start", "one a", "two a"})

    test_dfa(no_aaa, 
            ["", "a", "aa", "baa", "aabbaa", "bababaab"],
            ["aaaba", "bbbbaaab", "abaaa", "baaa", "aaa"] 
            )
