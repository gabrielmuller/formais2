from misc import set_to_str
class NFA:
    def __init__(self, transitions, initial, accepting):
        self.initial = initial
        self.transitions = transitions
        self.accepting = accepting

    def accepts(self, word):
        states = {self.initial}
        for char in word:
            prev_states = states
            states = set()
            for state in prev_states:
                if state in self.transitions and \
                char in self.transitions[state]:
                    states = states.union(self.transitions[state][char])
        return list(filter(lambda s : s in self.accepting, states))

