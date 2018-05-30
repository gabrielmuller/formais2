from nfa import NFA

"""
    Gramática regular
    Representada pelo símbolo inicial e por suas produções.
    Para as produções, tem-se um dicionário de conjuntos.
    Exemplo:
    S-> aA
    A -> aA | a
    {
        "S": {"aA"},
        "A": {"aA", "a"}
    }
"""
class RegularGrammar():
    
    def __init__(self, initial, productions):
        self.initial = initial

        # Dicionário de conjunto
        self.productions = productions


    """
        Conversão de AF para GR
    """
    @staticmethod
    def from_nfa(nfa):
        """
            q0 = S
        """
        initial = nfa.initial
        productions = {}

        # state type = str
        # transitions type = Dict
        for state, transitions in nfa.transitions.items():
            """
                Se (B,a) = C, adicione B->aC
            """
            if state not in productions:
                # Adiciona não terminal
                productions[state] = set()
            for vt in transitions:
                # Adiciona produção
                productions[state].add(vt+transitions[vt])
                """
                    Se C in F, adicione B->a
                """
                if transitions[vt] in nfa.accepting:
                    productions[state].add(vt)

        """
            Se q0 in F, então epsilon in T(M)
            Cria novo símbolo inicial S', replica transições de S,
            e adiciona S'-> &
        """
        if nfa.initial in nfa.accepting:
            new_initial = initial + "'"
            productions[new_initial] = productions[initial]
            productions[new_initial].add("&")
            initial = new_initial

        return RegularGrammar(initial, productions)

    def to_string(self):
        for vn in self.productions:
            prod = vn+"-> "
            for ld in self.productions[vn]:
                prod+=ld
                prod+=" | "
            print(prod)






            