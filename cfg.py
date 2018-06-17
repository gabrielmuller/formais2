from reader import read_cfg

import copy

"""
    Gramática Livre de Contexto
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
        self.initial = ""
        self.prods = {}
        if string is not None:
            self.initial, self.prods = read_cfg(string)
            self.complete()
        self.name = name

    # Igualdade entre gramáticas
    def __eq__(self, other):
        result = self.initial == other.initial and \
                self.prods == other.prods
        """if not result:
            print(self)
            print ("!=")
            print(other)"""
        return result

    # Representação em string.
    def __str__(self):

        # transforma as produções de um NT em string
        pstr = lambda nt: nt + ' -> ' + ' | '.join([' '.join(prod) for prod in self.prods[nt]])

        not_empty = {nt for nt, prods in self.prods.items() if prods}
        others = not_empty - {self.initial}
        return '\n'.join([pstr(nt) for nt in ([self.initial] + list(others))])

    def isEmpty(self):
        return self.remove_infertile() == Grammar()

    def isFinite(self):
        # Gramática vazia não é infinita (?)
        if self.isEmpty():
            return False

        """
        for vn, prods in self.prods.items():
            for ld in prods:
                # Se A-> α ^ A in α ^ A->α não é simples, é infinita
                if vn in ld and len(ld) > 1:
                    return False
        """

        # Simbolos alcançaveis por cada Vn
        # nao funciona com produção simples
        # TODO: transformar em Propria primeiro
        for vn in self.prods.keys():
            reachables = set()
            next_reach = {vn}
            while next_reach:
                prev_reach = set(next_reach)
                next_reach = set()
                for nt in prev_reach | {vn}: 
                    for ld in self.prods[nt]:
                        new = {c for c in ld if c.isupper() and c not in reachables}
                        next_reach |= new
                reachables |= next_reach
            # Se vn alcança a si mesmo
            if vn in reachables:
                return False
        
        return True

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

    # Retorna conjunto Nf (Vn férteis)
    def fertile(self):
        ni = set()
        i = 0
        changed = True
        while changed:
            ni_last = copy.deepcopy(ni) # Ni-1
            ni = copy.deepcopy(ni_last) # Ni = Ni-1

            # Todo A ∈ Vn - Ni-1
            for vn in self.prods.keys() - ni_last:

                # Todo A -> α ^ α ∈ (Vt U Ni-1)*
                fertile_prod = {ld for ld in self.prods[vn] 
                    if all(c in (self.vt() | ni_last | {"&"}) for c in list(ld)) }
                
                # Ni = Ni-1 U A
                if len(fertile_prod) != 0:
                    ni.add(vn)

            # While Ni != Ni-1
            if (len(ni) > len(ni_last)):
                changed = True
            else:
                changed = False

        return ni

    # Remover símbolos inférteis
    def remove_infertile(self):
        cfg = copy.deepcopy(self)

        fertile = self.fertile()
        infertile = cfg.prods.keys() - fertile

        # Remover não-terminais inférteis
        for vn in infertile:
            del cfg.prods[vn]

        # Remover produções com não-terminais inférteis
        for vn, prods in copy.deepcopy(cfg.prods).items():
            for ld in prods:
                if any(i in ld for i in infertile):
                    cfg.prods[vn].remove(ld)

        if len(cfg.prods) == 0:
            return Grammar()
        return cfg

    # Retorna conjunto de terminais (Vt)
    def vt(self):
        vt = set()
        for vn in self.prods.keys():
            for ld in self.prods[vn]:
                for v in ld:
                    if v.islower():
                        vt.add(v)
        return vt
