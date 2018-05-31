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
                # Adiciona produções (NFA)
                if type(transitions[vt]) is set:
                    for i in transitions[vt]:
                        productions[state].add(vt+i)

                # Adiciona produção (DFA)
                if type(transitions[vt]) is str:
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
        string = ""
        first = True
        for vn in self.productions:
            if not first:
                string+="\n"
            prod = vn+"-> "
            for ld in self.productions[vn]:
                prod+=ld
                prod+=" | "
            string+=prod
            first = False
        return string


    """
        Método auxiliar
        Retorna conjunto de produções da gramática, com
        não-terminais renomeados com a adição de uma string str
    """
    def _rename_productions(self, str):
        productions = {}
        for vn, values in self.productions.items():
            if vn+str not in productions:
                productions[vn+str] = set()
            for i in values:
                if len(i) == 1:
                    productions[vn+str].add(i)
                else:
                    productions[vn+str].add(i+str)
        return productions

    @staticmethod
    def union(grammar_a, grammar_b):
        """
            1 - Adicionar produções com não-terminais renomeados
            para evitar não-terminais diferentes com mesmo
            nome
        """
        a = grammar_a._rename_productions("1")
        b = grammar_b._rename_productions("2")
        productions = {**a, **b}

        """
            2 - Criar novo não-terminal inicial e replicar as
            produções dos iniciais das Gramáticas A e B
            no novo inicial
        """
        initial = "S"
        productions[initial] = set()

        for production in productions[grammar_a.initial+"1"]:
            productions[initial].add(production)
        for production in productions[grammar_b.initial+"2"]:
            productions[initial].add(production)

        return RegularGrammar(initial, productions)
        








            