from misc import set_to_str
from dfa import DFA
class NFA:
    def __init__(self, transitions, initial, accepting):
        self.initial = initial
        self.transitions = transitions
        self.accepting = accepting

    # provavelmente não vai ser usado assim
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

    def determinize(self):
        initial = ""
        accepting = set()

        # lista de conjuntos
        states_to_add = [{self.initial}]
        states_added = []

        transitions = {}

        while states_to_add:
            # conjunto de estados a adicionar como único estado
            states = states_to_add.pop()

            # para conjunto de estados, mapeia caracter para
            # conjunto de estados resultantes
            char_to_set = {}

            accept = False
            for state in states:
                # é estado de aceitação se algum estado for
                if state in self.accepting:
                    accept = True

                if state in self.transitions:
                    for char, state_set in self.transitions[state].items():
                        if char not in char_to_set:
                            char_to_set[char] = state_set
                        else:
                            char_to_set[char] = \
                                    char_to_set[char].union(state_set)

            # estados novos precisam ser adicionados
            for char, state_set in char_to_set.items():
                if state_set not in states_added:
                    states_to_add.append(state_set)

            # transforma conjunto de estados em um estado (string)
            char_to_state = {char : set_to_str(state_set) \
                    for char, state_set in char_to_set.items()}
            str_states = set_to_str(states)

            # primeira transicao é inicial
            if not transitions:
                initial = str_states

            # se houver um estado de aceitação, aceita
            if accept:
                accepting.add(str_states)

            transitions[str_states] = char_to_state
                    
            # marca estado como já especificado
            states_added.append(states)

        return DFA(transitions, initial, accepting)

    """
        Conversão de GR para AF
    """
    @staticmethod
    def from_rg(rg):
        productions = rg.productions

        transitions = {}
        initial = rg.initial

        """
            F = {A}
        """
        new_accepting_state = "A"
        if new_accepting_state in productions:
            new_accepting_state = "A'"
        accepting = {new_accepting_state}
        
        """
            F = {A, S} se S -> & in P
        """
        if "&" in productions[initial]: 
            accepting.add(initial)

        for state in productions:
            # Adiciona estado
            if state not in transitions:
                transitions[state] = {}

            for production in productions[state]:
                if production == "&":
                    continue
                """
                    Se B->a in P adiciona (B,a)=A
                    Se B->aC in P adiciona (B,a)=C
                """
                if len(production) == 1:
                    transitions[state][production] = \
                        new_accepting_state
                else:
                    transitions[state][production[0]] = \
                        production[1]

        return NFA(transitions, initial, accepting)






