from reader import read_cfg

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

    # Cria a gramática a partir do parse de uma string.
    def __init__(self, string, name="Gramática"):
        self.initial, self.prods = read_cfg(string)
        self.name = name

    # Representação em string.
    def __str__(self):

        # transforma as produções de um NT em string
        pstr = lambda nt: nt + ' -> ' + ' | '.join([' '.join(prod) for prod in self.prods[nt]])

        others = self.prods.keys() - {self.initial}
        return '\n'.join([pstr(nt) for nt in ([self.initial] + list(others))])

    # Retorna first de cada NT
    def first(self):
        firsts = {}

        # adiciona terminais e &
        for nt, prods in self.prods.items():
            firsts[nt] = set()
            for prod in prods:
                start = prod[0]
                if start.islower() or start is '&':
                    firsts[nt].add(start)

        changed = True

        # beautiful
        while changed:
            changed = False
            for nt, prods in self.prods.items():
                for prod in prods:
                    to_add = Grammar._first_star(prod, firsts)
                    if not to_add.issubset(firsts[nt]):
                        firsts[nt] = firsts[nt].union(to_add)
                        changed = True

        return firsts

    # Auxiliar
    @staticmethod
    def _first_star(prod, firsts):
        if not prod: return '&'

        start = prod[0]
        if start is '&' or start.islower():
            return {start}
        elif start.isupper():
            f = set(firsts[start])
            if '&' in f:
                f.remove('&')
                return f.union(Grammar._first_star(prod[1:], firsts))
            else:
                return f
            
