from model.reader import read_cfg

import copy, itertools

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
        """
        if not result:
            if self.prods: print(self)
            print ("!=")
            if other.prods: print(other)
        """
        return result

    # Representação em string.
    def __str__(self):

        if not self.initial:
            return 'Ø'

        # transforma as produções de um NT em string
        pstr = lambda nt: nt + ' -> ' + ' | '.join([' '.join(prod) for prod in self.prods[nt]])

        not_empty = {nt for nt, prods in self.prods.items() if prods}
        others = not_empty - {self.initial}
        return '\n'.join([pstr(nt) for nt in ([self.initial] + list(others))])

    # Retorna conjunto de terminais (Vt)
    def vt(self):
        vt = set()
        for vn in self.vn():
            for ld in self.prods[vn]:
                for v in ld:
                    if v.islower():
                        vt.add(v)
        return vt

    # Retorna conjunto de não-terminais (Vn)
    def vn(self):
        return self.prods.keys()

    # Retorna se símbolo é não terminal
    def is_vn(self, v):
        return v in self.prods.keys()

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
        # G sem produções simples
        g = self.rm_simple()

        for vn in g.prods.keys():
            reachables = set()
            next_reach = {vn}
            while next_reach:
                prev_reach = set(next_reach)
                next_reach = set()
                for nt in prev_reach | {vn}: 
                    for ld in g.prods[nt]:
                        new = {c for c in ld if c.isupper() and c not in reachables}
                        next_reach |= new
                reachables |= next_reach
            # Se vn alcança a si mesmo (sem produzir terminais)
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
        if start.isupper():
            f = set(firsts[start])
            if '&' in f:
                f.remove('&')
                return f.union(Grammar._first_star(prod[1:], firsts))
            else:
                return f
        else:
            return {start}

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
        firsts = {nt: set() for nt in self.vn()}

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
        follows = {nt: set() for nt in self.vn()}
        follows[self.initial] = {'$'}
        firsts = self.first()

        changed = True

        while changed:
            changed = False
            for nt, prods in self.prods.items():
                for prod in prods:
                    for index, symbol in enumerate(prod):
                        if not symbol.isupper(): continue

                        rest = prod[index+1:]
                        first = Grammar._first_star(rest, firsts)
                        to_add = first
                        if '&' in first:
                            to_add.remove('&')
                            to_add = to_add.union(follows[nt])

                        if not to_add.issubset(follows[symbol]):
                            follows[symbol] = follows[symbol].union(to_add)
                            changed = True


        return follows

    def _new_non_terminal(self, nt):
        new_nt = nt
        vn = self.vn()
        while(new_nt in vn):
            new_nt += "'"
        return new_nt

    def epsilon_free(self):
        eprods = {nt: prods - {('&',)} for nt, prods in self.prods.items()}
        nullables = self.nullable()

        einitial = self.initial
        if self.initial in nullables:
            einitial = self._new_non_terminal(self.initial)
            eprods[einitial] = {(self.initial,), ('&',)}

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
    
    # Retorna conjunto Vi (símbolos alcançáveis)
    def reachable(self):
        if not self.initial:
            return set()

        reachables = {self.initial}
        next_reach = {self.initial}
        next_vt_reach = set()
        reach_vt = set()
        vn = self.vn()
        vt = self.vt()

        while next_reach:
            prev_reach = set(next_reach)
            next_reach = set()
            for nt in prev_reach:
                for prod in self.prods[nt]:
                    new = {c for c in prod if c in vn and c not in reachables}
                    new_vt = {c for c in prod if c in vt and c not in reachables}
                    next_reach = next_reach.union(new)
                    next_vt_reach = next_vt_reach | new_vt
            reachables = reachables | next_reach | next_vt_reach

        return reachables

    # Retorna nova gramática sem NTs inalcançáveis.
    def rm_unreachable(self):
        reachables = self.reachable() - self.vt()

        result = Grammar()
        result.initial = self.initial
        result.prods = {nt: prods for nt, prods in self.prods.items() if nt in reachables}
        return result

    def rm_simple(self):
        efree = self.epsilon_free()
        nset = efree._simple_star()

        # Tira simples
        for nt, prods in efree.prods.items():
            to_remove = set()

            for prod in prods:
                if len(prod) is 1 and prod[0].isupper():
                    to_remove.add(prod)

            for rm in to_remove:
                prods.remove(rm)

        # Adiciona produções de Nx
        for nt in efree.prods.keys():
            for eq in nset[nt]:
                efree.prods[nt] = efree.prods[nt].union(efree.prods[eq])
        
        return efree

    # Retorna conjunto Nf (Vn férteis)
    def fertile(self):
        ni = set()
        i = 0
        changed = True
        while changed:
            ni_last = copy.deepcopy(ni) # Ni-1
            ni = copy.deepcopy(ni_last) # Ni = Ni-1

            # Todo A ∈ Vn - Ni-1
            for vn in self.vn() - ni_last:

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

    # Retorna se G é fatorável
    def is_factored(self):
        g = copy.deepcopy(self)
        first = self.first()
        vt = self.vt()

        for vn, prods in g.prods.items():
            for prod in prods:
                vtvt = any(prod[0] == p[0] for p in prods - {prod} if prod[0] in vt and p[0] in vt)
                vnvt = any(prod[0] in first[p[0]] for p in prods - {prod} if prod[0] in vt and p[0].isupper())
                vnvn = any(first[prod[0]] & first[p[0]] for p in prods - {prod} if prod[0].isupper() and p[0].isupper())
                if vtvt or vnvt or vnvn:
                    return False

        return True

    """
        Processo de fatoração:
        A -> α β | α γ
        para
        A  -> α A’
        A’ -> β | γ
    """
    def factor(self):
        cfg = copy.deepcopy(self)
        first = self.first()

        for vn, prods in self.prods.items():
            """ 
                Procura por não determinismo indireto 
                A -> α β | B λ
                B -> α γ | η
                E faz
                A -> α β | α γ | η λ
            """
            for prod in prods:
                if self.is_vn(prod[0]) and any(p[0] in first[prod[0]] for p in prods - {prod}):  
                    # Adiciona A -> α γ λ | η λ
                    cfg.prods[vn] |= {q+prod[1:] for q in cfg.prods[prod[0]]}
                    cfg.prods[vn] -= {prod} # Retira A -> B  


            # Combinações 2 a 2 de produções
            for prod_A, prod_B in itertools.combinations(prods,2):
                """ 
                    Procura por não determinismo indireto 
                    A -> C λ | B η
                    B -> α γ 
                    C -> α β
                    E faz
                    A -> α β λ | α γ η
                """
                if self.is_vn(prod_A[0]) and self.is_vn(prod_B[0]):
                    if any(q == p for p in first[prod_B[0]] for q in first[prod_A[0]]):
                        # Retirar A -> B, A- > C
                        cfg.prods[vn] -= {prod_A, prod_B} 
                        for q in cfg.prods[prod_A[0]]:
                            cfg.prods[vn] |= {q+prod_A[1:] for p in prods if q[0] in first[p[0]] and q[0] != "&" or (len(prod_A)==1)}
                            cfg.prods[vn] |= {prod_A[1:] for p in prods if q[0] in first[p[0]] and q[0] == "&" and len(prod_A)>1}
                        for q in cfg.prods[prod_B[0]]:
                            cfg.prods[vn] |= {q+prod_B[1:] for p in prods if q[0] in first[p[0]] and q[0] != "&" or (len(prod_B)==1)}
                            cfg.prods[vn] |= {prod_B[1:] for p in prods if q[0] in first[p[0]] and q[0] == "&" and len(prod_B)>1}

        """
            Procura determinismo direto
            A -> α β | α γ
        """
        alpha_dict = {}
        for vn, prods in cfg.prods.items():
            alpha_dict[vn] = set()
            for prod in prods:
                if prod[0] not in alpha_dict[vn] and (prod[0].islower() \
                or prod[0].isdigit()) and any(prod[0] == p[0] for p in prods - {prod}):
                    alpha_dict[vn].add(prod[0])

        for vn, alphas in alpha_dict.items():
            # Cada α tal que existe A -> α β | α γ
            for alpha in alphas:
                betas = set()   # Lado direito das produções, ie, β, γ...

                # Procura por A -> α β | α γ
                for prod in copy.deepcopy(cfg.prods[vn]):

                    if prod[0] == alpha:
                        
                        cfg.prods[vn] -= {prod}                     # Retira A -> α β
                        betas |= {prod[1:]} if prod[1:] else {("&",)}  # Salva β
                new_nt = self._new_non_terminal(vn)
                cfg.prods[vn] |= {(alpha, new_nt)}                  # Cria A  -> α A’
                cfg.prods[new_nt] = {(beta) for beta in betas}      # Cria A’ -> β | γ
        
        return cfg

    def factor_in_steps(self, steps):
        cfg = copy.deepcopy(self)
        for i in range(steps):
            if cfg.is_factored(): return cfg
            cfg = cfg.factor()
        if not cfg.is_factored():
            stepText = "passos" if steps>1 else "passo"
            raise ValueError("Gramática não é fatorável em %d %s. \
                \nGramática após %d %s de fatoração:\n" % (steps, stepText, steps, stepText) \
                + str(cfg))
        return cfg    

    # Retorna conjunto de não-terminais que possuem recursão a esquerda direta
    def has_direct_left_recursion(self):
        rec_vn = set()
        for vn, prods in self.prods.items():
            direct = {x for x in prods if x[0] == vn}
            if len(direct): rec_vn.add(vn)
        return rec_vn

    # Retorna conjunto de não-terminais que possuem recursão a esquerda indireta
    def has_indirect_left_recursion(self):
        rec_nt = set()
        first_nt = self.first_nt()
        for nt, prods in self.prods.items():
            for prod in prods:
                if nt in prod and prod[0] != nt:       # Evitar encontrar rec direta
                    i = list(prod).index(nt)
                    if all(other_nt in self.nullable() or other_nt in first_nt[nt] \
                        for other_nt in prod[:i]):
                        rec_nt.add(nt)
                elif any(x for x in prod if x in first_nt[nt]) and prod[0] != nt:
                    i = list(prod).index([x for x in prod if x in first_nt[nt]][0])
                    if not i: rec_nt.add(nt)       
                    elif all(other_nt in self.nullable() for other_nt in prod[:i]):
                        rec_nt.add(nt)   
        return rec_nt

    # Retorna G sem recursão direta
    def remove_direct_left_recursion(self):
        cfg = copy.deepcopy(self)
        for nt, prods in self.prods.items():
            direct = {x for x in prods if x[0] == nt}
            no_rec = prods - direct
            new_nt = self._new_non_terminal(nt)
            cfg.prods[nt] = {x + (new_nt,) for x in no_rec}
            cfg.prods[new_nt] = {x[1:] + (new_nt,) for x in direct} | {('&',)}
        return cfg

    # Retorna G sem recursão direta em um não-terminal <nt>
    def remove_direct_left_recursion_nt(self, nt):
        cfg = copy.deepcopy(self)
        direct = {x for x in cfg.prods[nt] if x[0] == nt}
        no_rec = cfg.prods[nt] - direct
        new_nt = self._new_non_terminal(nt)
        cfg.prods[nt] = {x + (new_nt,) for x in no_rec}
        cfg.prods[new_nt] = {x[1:] + (new_nt,) for x in direct} | {('&',)}
        return cfg

    # Retorna G sem recursão indireta
    def remove_indirect_left_recursion(self):
        cfg = copy.deepcopy(self)
        
        a = [""] + list(cfg.vn())       # ignorar posição 0
        for i in range(1,len(a)):       # i = 1, n
            for j in range(1, i):       # j = 1, i-1
                prods = {x for x in cfg.prods[a[i]] if x[0] is a[j]}
                cfg.prods[a[i]] -= prods
                cfg.prods[a[i]] |= {d+x[1:] for d in cfg.prods[a[j]] for x in prods}
            cfg = cfg.remove_direct_left_recursion_nt(a[i])

        return cfg

    # Retorna G sem recursão a esquerda
    def remove_left_recursion(self):
        if self.is_proper():
            if self.has_indirect_left_recursion():
                return self.remove_indirect_left_recursion()
            elif self.has_direct_left_recursion():
                return self.remove_direct_left_recursion()
            else:
                return self
        else:
            raise Exception(\
                "Algoritmo espera gramática própria")

    def proper(self):
        g = self.remove_infertile()
        g = g.rm_unreachable()
        g = g.epsilon_free()
        g = g.rm_simple()
        return g

    # Retorna se G é própria
    def is_proper(self):
        nf = self.fertile() == self.vn()
        vi = self.reachable() == self.vn() | self.vt()
        ne = len(self.nullable()) == 0 or self.nullable() == {self.initial}
        nx = all(len(na)==1 for na in self._simple_star().values())
        return nf and vi and ne and nx
