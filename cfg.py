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
        self.complete()
        self.name = name

    # Representação em string.
    def __str__(self):

        # transforma as produções de um NT em string
        pstr = lambda nt: nt + ' -> ' + ' | '.join([' '.join(prod) for prod in self.prods[nt]])

        not_empty = {nt for nt, prods in self.prods.items() if prods}
        others = not_empty - {self.initial}
        return '\n'.join([pstr(nt) for nt in ([self.initial] + list(others))])

    # Adiciona NTs sem produções no dict para garantir
    # consistência na representação
    def complete(self):
        to_add = set()
        for nt, prods in self.prods.items():
            for prod in prods:
                for symbol in prod:
                    if symbol.isupper() and symbol not in self.prods:
                       to_add.add(symbol) 
        
        for nt in to_add:
            self.prods[nt] = set()

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

    # conjunto de símbolos de Vn que podem 
    # iniciar sequências derivadas de A para todo A ∈ Vn
    def first_nt(self):
        nullables = self.nullable()
        firsts = {nt: set() for nt in self.prods.keys()}

        changed = False

        # passo base
        for nt, prods in self.prods.items():
            for prod in prods:
                start = prod[0]
                if start.isupper():
                    firsts[nt].add(start)
                    changed = True

        while changed:
            changed = False
            for nt, prods in self.prods.items():
                for prod in prods:
                    to_add = Grammar._first_nt_star(prod, firsts, nullables)
                    if not to_add.issubset(firsts[nt]):
                        firsts[nt] = firsts[nt].union(to_add)
                        changed = True

        return firsts
            
    # Auxiliar
    @staticmethod
    def _first_nt_star(prod, firsts, nullables):
        if not prod or not prod[0].isupper(): return set()

        start = prod[0]
        f = firsts[start].union({start})
        if start in nullables:
            return f.union(Grammar._first_nt_star(prod[1:], firsts, nullables))
        else:
            return f

    # Conjunto de NTs que derivam &
    def nullable(self):
        partial = {nt for nt, prods in self.prods.items() if ('&',) in prods}
        changed = bool(partial)

        while changed:
            changed = False
            for nt, prods in self.prods.items():
                if prods and nt not in partial:
                    nt_is_null = False
                    for prod in prods:
                        prod_is_null = True
                        for symbol in prod:
                            if symbol not in partial:
                                prod_is_null = False
                        nt_is_null = nt_is_null or prod_is_null

                    if nt_is_null:
                        partial.add(nt)
                        changed = True
        return partial

