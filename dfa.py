class DFA:
    def __init__(self, transitions, initial, accepting):
        self.initial = initial

        # dicionário de dicionários
        self.transitions = transitions

        self.accepting = accepting

    def accepts(self, word):
        state = self.initial
        for char in word:
            if state not in self.transitions or \
            char not in self.transitions[state]:
                return False
            state = self.transitions[state][char]
        return state if state in self.accepting else False

    # lista de palavras da linguagem de certo tamanho
    def words_of_size(self, size):
        # (palavra, estado onde termina a palavra)
        words = [("", self.initial)]

        for i in range(size):
            prev_words = words
            words = set()
            for word in prev_words:
                for char, state in self.transitions[word[1]].items():
                    words.add((word[0] + char, state))

        valid = lambda i : i[1] in self.accepting
        return {i[0] for i in filter(valid, words)}

    """
        Remover estado
    """
    def remove_state(self, removed):
        # Remover estado
        del self.transitions[removed]

        # Remover transições para o estado removido
        # TODO: melhorar. Talvez falhe em alguns casos
        transitions_to_remove = {}
        for state in self.transitions.keys():
            print("state",state)
            for key, next_state in self.transitions[state].items():
                print("key", key, ", next", next_state)
                if next_state == removed:
                    print(next_state)
                    transitions_to_remove[state] = key

        for state,symbol in transitions_to_remove.items():
            del self.transitions[state][symbol]

    """
        Remover estados inacessíveis
    """
    def remove_unreachable(self):
        reacheable = set()
        new_states = {self.initial}
        while not new_states <= reacheable:
            reacheable = reacheable | new_states
            temp = new_states.copy()
            new_states = set()
            for state in temp:
                for symbol in self.transitions[state]:
                    new_states.add(self.transitions.get(state).get(symbol))
        for unreachable in self.transitions.keys() - reacheable:
            self.remove_state(unreachable)

    """
        Remover estados mortos
    """
    def remove_dead(self):
        alive = set()
        new_states = self.accepting.copy()
        while not new_states <= alive:
            alive = alive | new_states
            new_states = set()
            for state in self.transitions.keys():
                for next_state in self.transitions[state].values():
                    if(next_state in alive):
                        new_states.add(state)
        for dead in self.transitions.keys() - alive:
            self.remove_state(dead)

    """
        Minimização de AF
    """
    def minimize(self):
        self.remove_unreachable()
        self.remove_dead()
        #self.merge_nondistinguishable()

