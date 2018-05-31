from itertools import combinations

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
        if removed in self.transitions.keys():
            del self.transitions[removed]

        # Remover transições para o estado removido
        # TODO: melhorar. Talvez falhe em alguns casos
        transitions_to_remove = {}
        for state in self.transitions.keys():
            for key, next_state in self.transitions[state].items():
                if next_state == removed:
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
        Tornar estados únicos
        Algoritmo: Myhill-Nerode Theorem
    """
    def merge_nondistinguishable(self):
        #TODO: resultado não determinístico (às vezes dá certo)
        F = self.accepting.copy()
        sigma = self.transitions

        nondistinguishable = set()
        marked = set()

        """
            Step 1 - pares de estados
        """
        for pair in combinations(self.transitions.keys(), 2):
            nondistinguishable.add(pair)

        """
            Step 2 - marcar (Qi, Qj) onde Qi in F e Qj not in F 
            ou vice versa
        """
        for pair in nondistinguishable:
            if (pair[0] in F and pair[1] not in F) \
                or (pair[1] in F and pair[0] not in F):
                marked.add(pair)

        """
            Step 3 - se existe  par (Qi, Qj) não marcado, marque
            se {sigma(Qi,A), sigma(Qj,A)} está marcado
            para algum símbolo do alfabeto
        """
        # b e a u t i f u l
        while(1):
            can_mark = False
            for pair in nondistinguishable - marked:
               for key0 in sigma[pair[0]].keys():
                    for key1 in sigma[pair[1]].keys():
                        if key0 == key1:
                            if (sigma[pair[0]][key0], \
                                sigma[pair[1]][key0]) in marked:
                                marked.add(pair)
                                can_mark = True
            if not can_mark:
                break

        """
            Step 4 - Combinar pares não marcados (Qi, Qj) e 
            transformá-los em único estado no DFA
        """
        nondistinguishable -= marked
        for state_a, state_b in nondistinguishable:
            if state_b == self.initial or \
                state_a not in self.transitions.keys():
                temp = state_a
                state_a = state_b
                state_b = temp
            for state in self.transitions.keys():
                for key, next_state in self.transitions[state].items():
                    if next_state == state_b:
                        self.transitions[state][key] = state_a
            self.remove_state(state_b)

    """
        Minimização de AF
    """
    def minimize(self):
        self.remove_unreachable()
        self.remove_dead()
        self.merge_nondistinguishable()

