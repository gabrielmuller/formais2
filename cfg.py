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
    def __init__(self, string=None, name="Gramática"):
        if string is not None:
            self.initial, self.prods = read_cfg(string)
            self.complete()
        self.name = name

    # Igualdade entre gramáticas
    def __eq__(self, other):
        result = self.initial == other.initial and \
                self.prods == other.prods
        if not result:
            print(self)
            print ("!=")
            print(other)
        return result

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
        if not prod: return {'&'}

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
        return self._first_nt(False)

    # Nx para prod simples
    def _simple_star(self):
        nset = self._first_nt(True)
        for nt, s in nset.items():
            s.add(nt)
        return nset

    def _first_nt(self, simple_only):
        nullables = self.nullable()
        firsts = {nt: set() for nt in self.prods.keys()}

        changed = False

        # passo base
        for nt, prods in self.prods.items():
            for prod in prods:
                start = prod[0]
                if start.isupper() and (len(prod) is 1 or not simple_only):
                    firsts[nt].add(start)
                    changed = True

        while changed:
            changed = False
            for nt, prods in self.prods.items():
                for prod in prods:
                    if simple_only and len(prod) > 1:
                        continue
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

    def follow(self):
        follows = {nt: set() for nt in self.prods.keys()}
        follows[self.initial] = {'$'}
        firsts = self.first()

        changed = True

        while changed:
            changed = False
            for nt, prods in self.prods.items():
                for prod in prods:
                    for index, symbol in enumerate(prod):
                        if not symbol.isupper(): continue

                        rest = prod[index:]
                        first = Grammar._first_star(rest, firsts)
                        to_add = follows[nt] if '&' in first else first

                        if not to_add.issubset(follows[symbol]):
                            follows[symbol] = follows[symbol].union(to_add)
                            changed = True

        return follows

    def epsilon_free(self):
        eprods = {nt: prods - {('&',)} for nt, prods in self.prods.items()}
        nullables = self.nullable()

        einitial = self.initial
        if self.initial in nullables:
            einitial = 'S1'
            eprods['S1'] = {('S',), ('&',)}

        for e in nullables:
            new_prods = {nt: set() for nt in eprods.keys()}
            for nt, prods in eprods.items():
                for prod in prods:
                    occurrences = []
                    enp = list(enumerate(prod))

                    for i, symbol in enp:
                        if symbol is e:
                            occurrences.append(i)

                    for combo in Grammar._combinations(occurrences):
                         # possivelmente a linha de código mais linda e horrível
                         to_add = [c for i, c in enp if c is not e or i in combo]

                         if to_add: new_prods[nt].add(tuple(to_add))
            eprods = dict(eprods, **new_prods)
                            
        gr = Grammar()
        gr.prods = eprods
        gr.initial = einitial
        return gr

    # Retorna todas combinações de elementos da lista l
    def _combinations(l):
        result = []
        bformat = "{0:0"+str(len(l))+"b}"
        binary = lambda n: bformat.format(n)
        combos = map(binary, range(2**len(l)))
        for combo in combos:
            matches = list(zip(combo, l))
            result.append([match[1] for match in matches if int(match[0])])

        return result
    
    # Retorna nova gramática sem NTs inalcançáveis.
    def rm_unreachable(self):
        reachables = {self.initial}
        next_reach = {self.initial}

        while next_reach:
            prev_reach = set(next_reach)
            next_reach = set()
            for nt in prev_reach:
                for prod in self.prods[nt]:
                    new = {c for c in prod if c.isupper() and c not in reachables}
                    next_reach = next_reach.union(new)
            reachables = reachables.union(next_reach)

        result = Grammar()
        result.initial = self.initial
        result.prods = {nt: prods for nt, prods in self.prods.items() if nt in reachables}

        return result

    def rm_simple(self):
        efree = self.epsilon_free()
        nset = efree._simple_star()
        return
