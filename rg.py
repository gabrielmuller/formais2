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

        self.rg_str = "Gramática "
        # Dicionário de conjunto
        self.productions = productions


    """
        Conversão de AF para GR
    """
    @staticmethod
    def from_nfa(nfa):
        nfa.determinize()
        
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
                for i in transitions[vt]:
                    productions[state].add(vt+i)

                """
                    Se C in F, adicione B->a
                """
                if transitions[vt].issubset(nfa.accepting):
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

    """
        União de duas GR
        Retorna uma GR nova
    """
    def union(self, other):
        """
            1 - Adicionar produções com não-terminais renomeados
            para evitar não-terminais diferentes com mesmo
            nome
        """
        a = self._rename_productions("1")
        b = other._rename_productions("2")
        productions = {**a, **b}

        """
            2 - Criar novo não-terminal inicial e replicar as
            produções dos iniciais de G1(self) e G2(other)
            no novo inicial
        """
        initial = "S"
        productions[initial] = set()

        for production in productions[self.initial+"1"]:
            productions[initial].add(production)
        for production in productions[other.initial+"2"]:
            productions[initial].add(production)

        return RegularGrammar(initial, productions)
        
    """
        Concatenação de duas GR
        Retorna uma GR nova
    """
    def concatenation(self, other):
        """
            1 - Adicionar produções com não-terminais renomeados
            para evitar não-terminais diferentes com mesmo
            nome
        """
        a = self._rename_productions("1")
        b = other._rename_productions("2")
        productions = {**a, **b}

        """
            Símbolos iniciais S1 e S2
        """
        initial1 = self.initial+"1"
        initial2 = other.initial+"2"

        """
            2 - Para toda regra A->a em G1, 
            substitui por A->aS2 onde S2 é o símbolo inicial
            de G2 renomeado
        """
        add_later = {}
        for vn, values in a.items(): 
            for i in values:
                if len(i) == 1 and i != "&":
                    # Se "S2->&", adicionar (depois) A->a 
                    if "&" in productions[initial2]:
                        add_later[vn] = i
                    productions[vn].remove(i)
                    productions[vn].add(i+initial2)

        """
            3 - Se "S1->&" pertence as produções de G1,
            replica as produções de S2 em S1.
        """
        if "&" in a[initial1]:
            for production in productions[initial2]:
                productions[initial1].add(production)

        """
            4 - Se "S2->&" pertence às produções de G2, 
            retira a produção da GR final e adiciona
            produções A->a de G1
        """
        if "&" in productions[initial2]:
            productions[initial2] -= {"&"}
            for key, value in add_later.items():
                productions[key].add(value)
        
        return RegularGrammar(initial1, productions)

    """
        Fechamento de uma GR
        Retorna uma GR nova
    """
    def kleene_closure(self):
        """
            1 - Remover &
        """
        productions = self.productions
        initial = self.initial
        productions[initial].discard("&")

        """
            2 - Para toda regra A->a em G, 
            adicionar A->aS onde S é o símbolo inicial de G
        """
        new_productions = {}
        for vn, values in productions.items():
            for i in values:
                if len(i) == 1 and i != "&":
                    if vn not in new_productions: 
                        new_productions[vn] = set()
                    new_productions[vn].add(i+initial)

        for key,value in new_productions.items():
            productions[key] |= value

        """
            3 - Se "S->&" pertence as produções de G,
            cria novo estado inicial S' e S'->&
        """
        initial += "'"
        productions[initial] = {"&"}
        for production in productions[self.initial]:
            productions[initial].add(production)
       
        return RegularGrammar(initial, productions)


    def printer(self):
        print("----")
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
        print(string)
        print("----")










            
