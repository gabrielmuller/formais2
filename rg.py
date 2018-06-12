from reader import read_rg

"""
    Gramática regular
    Representada pelo símbolo inicial e por suas produções.
    Para as produções, tem-se um dicionário de conjuntos de listas.
    Exemplo:
    S -> a A1
    A1 -> a A1 | a
    {
        "S": {["a", "A1"]},
        "A1": {["a", "A1"], ["a"]}
    }
"""

class RegularGrammar():
    
    """
        Cria a gramática a partir do parse de uma string.
    """
    def __init__(self, string, name="Gramática"):
        self.initial, self.prods = parse_rg(string)
        self.name = name

    """
        Representação em string.
    """
    def __repr__(self):
        # transforma as produções de um Vn em string
        pstr = lambda vn: vn + ' -> ' + ' | '.join(' '.join(self.prods[vn]))

        others = self.prods.keys() - {self.initial}
        return [pstr(vn) for vn in ([self.initial] + list(others))]


        
