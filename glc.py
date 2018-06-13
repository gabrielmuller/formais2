from reader import read_glc

"""
    Gramática regular
    Representada pelo símbolo inicial e por suas produções.
    Para as produções, tem-se um dicionário de conjuntos de tuplas.
    Exemplo:
    S -> a A1
    A1 -> a A1 | a
    {
        "S": {("a", "A1")},
        "A1": {("a", "A1"), ("a")}
    }
"""

class Grammar():
    
    """
        Cria a gramática a partir do parse de uma string.
    """
    def __init__(self, string, name="Gramática"):
        self.initial, self.prods = read_glc(string)
        self.name = name

    """
        Representação em string.
    """
    def __str__(self):
        # transforma as produções de um Vn em string
        pstr = lambda vn: vn + ' -> ' + ' | '.join([' '.join(prod) for prod in self.prods[vn]])

        others = self.prods.keys() - {self.initial}
        return '\n'.join([pstr(vn) for vn in ([self.initial] + list(others))])


        
