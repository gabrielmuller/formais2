from itertools import combinations
from misc import *
import copy
import json

class NFA:
    def __init__(self, transitions, initial, accepting):
        self.initial = initial
        self.transitions = transitions
        self.accepting = accepting

    def states(self):
        return self.transitions.keys()

    # TESTED OK
    def is_dfa(self):
        for state, transitions in self.transitions.items():
            if state is not self.initial and \
                "&" in transitions:
                return False
            for vt in transitions.keys():
                if type(self.transitions[state][vt]) is set \
                    and len(self.transitions[state][vt]) > 1:
                    return False    
        return True

    # TESTED OK
    # provavelmente não vai ser usado assim
    def accepts_nfa(self, word):
        states = {self.initial}
        for char in word:
            prev_states = states
            states = set()
            for state in prev_states:
                if state in self.transitions and \
                char in self.transitions[state]:
                    states = states.union(self.transitions[state][char])
        return list(filter(lambda s : s in self.accepting, states))

    # TESTED OK
    def accepts_dfa(self, word):
        state = self.initial
        for char in word:
            if state not in self.transitions or \
            char not in self.transitions[state]:
                return False
            state = next(iter(self.transitions[state][char]))
        return state if state in self.accepting else False

    def accepts(self, word):
        if self.is_dfa(): return self.accepts_dfa(word)
        else: return self.accepts_nfa(word)

    # [dfa.py]
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

    def alphabet(self):
        alphabet = set()
        for state in self.transitions.keys():
            for vt in self.transitions[state].keys():
                alphabet.add(vt)
        return alphabet

    # TESTED OK
    def determinize(self):
        if self.is_dfa(): return self
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
            char_to_state = {char : {set_to_str(state_set)} \
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

        self.transitions = copy.deepcopy(transitions)
        self.initial = copy.deepcopy(initial)
        self.accepting = copy.deepcopy(accepting)
        self.rename_states(0)
        #return NFA(transitions, initial, accepting)

    """
        Remover estado
    """
    # TESTED OK
    def remove_state(self, removed):
        # Evitar remover estado inicial
        # TODO: colocar exceção ou coisa assim
        if removed is self.initial:
            return
        # Remover estado
        if removed in self.transitions.keys():
            del self.transitions[removed]

        transitions_to_remove = {}
        for state in self.transitions.keys():
            for key, next_states in self.transitions[state].items():
                if any(removed == next_state \
                    for next_state in next_states):
                    transitions_to_remove[state] = key

        for state,symbol in transitions_to_remove.items():
            self.transitions[state][symbol] -= {removed}

    """
        Remover estados inacessíveis
    """
    # TESTED OK
    def remove_unreachable(self):
        reacheable = set()
        new_states = {self.initial}
        while not new_states <= reacheable:
            reacheable = reacheable | new_states
            temp = new_states.copy()
            new_states = set()
            for state in temp:
                if state in self.transitions:
                    for symbol in self.transitions[state]:
                        for next_state in self.transitions[state][symbol]:
                            new_states.add(next_state)
        for unreachable in self.transitions.keys() - reacheable:
            self.remove_state(unreachable)

    """
        Remover estados mortos
    """
    # TESTED OK
    def remove_dead(self):
        # TODO: colocar exceção ou coisa assim pra estado inicial
        alive = set()
        new_states = self.accepting.copy() if self.accepting else set()
        while not new_states <= alive:
            alive = alive | new_states
            new_states = set()
            for state in self.transitions.keys():
                for next_state in self.transitions[state].values():
                    if(next_state.issubset(alive)):
                        new_states.add(state)
        for dead in self.transitions.keys() - alive:
            self.remove_state(dead)

    """
        Tornar estados únicos
        Algoritmo: Myhill-Nerode Theorem
    """
    def merge_nondistinguishable(self):
        # TODO: testar se é completo e se não for:
        self.complete()

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
                            if (next(iter(sigma[pair[0]][key0])), \
                                next(iter(sigma[pair[1]][key0]))) in marked \
                                or (next(iter(sigma[pair[1]][key0])), \
                                    next(iter(sigma[pair[0]][key0]))) in marked:
                                marked.add(pair)
                                can_mark = True
            if not can_mark:
                break

        """
            Step 4 - Combinar pares não marcados (Qi, Qj) e 
            transformá-los em único estado no AF
        """
        nondistinguishable -= marked
        for state_a, state_b in nondistinguishable:
            remove = state_b
            keep = state_a
            if remove == self.initial or \
                keep not in self.transitions.keys():
                remove = state_a
                keep = state_b      
            for state in self.transitions.keys():
                for key, next_state in self.transitions[state].items():
                    if {remove}.issubset(next_state):
                        self.transitions[state][key] -= {remove}
                        self.transitions[state][key] |= {keep}
            self.remove_state(remove)

    """
        Minimização de AF
    """
    def minimize(self):
        self.determinize()
        self.remove_unreachable()
        self.remove_dead()
        self.merge_nondistinguishable()

    """
        Renomear estados do AF
        Renomeia estados a partir de "qi" sendo i definido
        pelo parâmetro "start"
    """
    # TESTED OK
    def rename_states(self, start):
        new_transitions = {}
        new_names = {} # Dicionário
        new_initial = ""
        new_accepting = set()

        for state in self.transitions.keys():
            new_names[state] = "q"+str(start) if start!=0 else "q0"
            if state is self.initial: 
                new_initial = new_names[state]
            if state in self.accepting: 
                new_accepting.add(new_names[state])
            start += 1

        # Renomear estados
        for state in self.transitions.keys():
            new_transitions[new_names[state]] = self.transitions[state]

        # Renomear estados nas transições
        for state, state_transitions in new_transitions.items():
            for vt, next_state in state_transitions.items():
                new_transitions[state][vt] = set()
                for i in next_state:
                    new_transitions[state][vt].add(new_names[i])

        self.initial = new_initial
        self.accepting = new_accepting
        self.transitions = new_transitions.copy()

    """ 
        Torna AFD Completo, i.e., todo estado tem transição
        definida para cada símbolo do alfabeto
    """
    # TESTED OK
    def complete(self):
        if not self.is_dfa(): 
            self.determinize()
        self.transitions["-"] = {}
        for state in self.transitions.keys():
            for symbol in self.alphabet():
                if symbol not in self.transitions[state]:
                    self.transitions[state][symbol] = {"-"}
                elif len(self.transitions[state][symbol])==0:
                    self.transitions[state][symbol].add("-")

    """     
        Complemento
        Transforma o AFD no autômato que reconhece o complemento
        da linguagem do AFD original
    """
    # TESTED OK
    def complement(self):
        self.complete()
        for state in self.transitions.keys():
            if state in self.accepting:
                self.accepting.remove(state)
            else:
                self.accepting.add(state)

    """
        União
        Retorna novo autômato
    """
    # TESTED OK
    def union(self, other):
        self.complete()
        other.complete()

        self.rename_states(1) #q1...qi
        other.rename_states(1+len(self.transitions.keys())) #qi+1..qj

        new_initial = "q0"
        new_transitions = {}
        new_accepting = set()

        if self.initial in self.accepting or \
            other.initial in other.accepting:
            new_accepting.add(new_initial)

        """
            Copiar transições
        """
        for state, transitions in {**self.transitions, \
            **other.transitions}.items():
            if state not in new_transitions:
                new_transitions[state] = {}
            for key, values in transitions.items():
                if key not in new_transitions[state]:
                    new_transitions[state][key] = set()
                new_transitions[state][key].add(next(iter(values)))

        new_transitions[new_initial] = {}
        for symbol in self.alphabet() | other.alphabet():
            new_transitions[new_initial][symbol] = {                    \
                next(iter(self.transitions[self.initial].get(symbol))), \
                next(iter(other.transitions[other.initial].get(symbol)))
            }

        new_accepting |= self.accepting | other.accepting

        return NFA(new_transitions, new_initial, new_accepting)

    """
        Diferença
        Retorna AFD que reconhece a diferença entre duas linguagens
        regulares representadas por AFDs
        L1-L2 = L1 ^ (~L2)
    """
    # TESTED OK
    def difference(self, other):
        m1 = copy.deepcopy(self)
        m2 = copy.deepcopy(other)
        m2.complement()

        return m1.intersection(m2)

    """
        Intersecção
        L1 ^ L2 = ~(~L1 v ~L2)
    """
    # TESTED OK
    def intersection(self, other):
        m1 = copy.deepcopy(self)
        m2 = copy.deepcopy(other)

        m1.complement()
        m2.complement() 

        m = m1.union(m2)

        m.complement()

        return m

    """
        Reverso
    """
    # TESTED OK
    def reverse(self):
        # reverter transições
        transitions = {}
        for states, char_to_next in self.transitions.items():
            for char, next_states  in char_to_next.items():
                for next_state in next_states:
                    if next_state not in transitions:
                        transitions[next_state] = {}
                    transitions[next_state][char] = states

        # criar novo estado inicial
        initial = "q0'"

        # criar transições do novo estado inicial
        transitions[initial] = {}

        for prev_accept in self.accepting:
            for char, next_states in transitions[prev_accept].items():
                if char not in transitions[initial]:
                    transitions[initial][char] = set()
                transitions[initial][char] = \
                    transitions[initial][char].union(next_states);

        # definir estados finais
        accepting = {self.initial}
        if self.initial in self.accepting:
            accepting.add(initial)

        return NFA(transitions, initial, accepting)

    """
        Conversão de GR para AF
        Retorna AF
    """
    # TESTED OK
    @staticmethod
    def from_rg(rg):
        productions = rg.productions

        transitions = {}
        initial = rg.initial

        """
            F = {A}
        """
        new_accepting_state = "X"
        if new_accepting_state in productions:
            new_accepting_state = "X'"
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
                if production[0] not in transitions[state]:
                    transitions[state][production[0]] = set()

                if len(production) == 1:
                    transitions[state][production].add(new_accepting_state)
                else:
                    transitions[state][production[0]].add(production[1:])

        transitions[new_accepting_state] = {}
        return NFA(transitions, initial, accepting)

    """
        Salva AF para arquivo JSON
    """
    def save(self, path):
        to_save = {}
        to_save["initial"] = self.initial
        to_save["accepting"] = self.accepting
        to_save["transitions"] = self.transitions
        json.dump(to_save, open(path, 'w'), cls=SetEncoder)

    """
        Carrega AF de arquivo JSON
    """
    @staticmethod
    def open(path):
        data = json.load(open(path, 'r'))
        initial = data["initial"]
        accepting = set(data["accepting"])
        transitions = {}

        for state in data["transitions"].keys():
            if state not in transitions: transitions[state] = {}
            for symbol, next_states in data["transitions"][state].items():
                if symbol not in transitions[state]: 
                    transitions[state][symbol] = set()
                for i in next_states:
                    transitions[state][symbol].add(i)
        return NFA(transitions, initial, accepting)


    # retorna FA em uma tabela legível
    def to_string(self):
        alphabet = sorted(list(self.alphabet()))
        first_line = [' '] + alphabet
        lines = [first_line]

        for state, char_to_next in self.transitions.items():
            prefix = '->' if state == self.initial else ''
            prefix += '*' if state in self.accepting else ''
            line = [prefix + state]
            for char in alphabet:
                next_states = {'-'}
                if char in char_to_next:
                    next_states = char_to_next[char]
                line.append(', '.join(next_states)) 
            lines.append(line)

        return matrix_to_table(lines)
                    
    #Para debugging
    def printer(self):
        print("----")
        special = "  "
        for state, transitions in self.transitions.items():
            if state is self.initial: special = "->"
            if state in self.accepting: special += " *"
            if special=="  ": special += "  "
            print(special, state, transitions)
            special = "  "
        print("----")

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
      if isinstance(obj, set):
         return list(obj)
      return json.JSONEncoder.default(self, obj)






