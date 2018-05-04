class DFA:
    def __init__(self, transitions, initial, accepting):
        self.initial = initial
        self.transitions = transitions
        self.accepting = accepting

    def accepts(self, word):
        state = self.initial
        for char in word:
            if (state, char) not in self.transitions:
                return False
            state = self.transitions[(state, char)]
        return (state in self.accepting)

