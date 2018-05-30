from dfa import DFA

# Alias para claridade
DOWN = False
UP = True

class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

        # filho da direita está acima?
        self.up = False

    # Nodo é um operador?
    def is_operator(self):
        return self.value in Regex.up

    # costura esse nodo com um nodo acima
    def thread(self, up_node):
        self.up = True
        self.right = up_node

    def in_order(self):
        l = self.left.in_order() if self.left else []
        r = self.right.in_order() if self.right else []
        return l + [self] + r

class Move:
    # 'move' é um nodo associado a uma direção (subida ou descida)
    def __init__(self, node, direction):
        self.node = node
        self.dir = direction

    # retorna folhas alcançadas a partir desse move
    def simone_leaves(self):
        if self.node == '&':
            return set()

        leaves = set()
        moves = {self}
        first = True

        while moves:
            next_moves = set()

            for move in moves:
                if move.node == '&':
                    leaves.add(move)
                    continue
                if move.node.is_operator():
                    func = Regex.semantics[move.dir][move.node.value]
                    next_moves = next_moves.union(func(move.node))
                else:
                    if first:
                        func = Regex.leaf_up
                        next_moves = next_moves.union(func(move.node))
                    else:
                        leaves.add(move)

            moves = next_moves
            first = False

        #return set(map(lambda l: l.node, leaves))
        return leaves

# semântica de subida do '|', a mais complicada
def or_up_semantics(node):
    while node.is_operator():
        node = node.right

    return {Move(node.right, UP)}

class Regex:

    # Semântica dos operadores
    # Operadores são mapeados a um conjunto de moves
    down = \
    {'|': lambda node: {Move(node.left, DOWN), Move(node.right, DOWN)},
    '.': lambda node: {Move(node.left, DOWN)},
    '?': lambda node: {Move(node.left, DOWN), Move(node.right, UP)},
    '*': lambda node: {Move(node.left, DOWN), Move(node.right, UP)}}

    up = \
    {'|': or_up_semantics,
    '.': lambda node: {Move(node.right, DOWN)},
    '?': lambda node: {Move(node.right, UP)},
    '*': lambda node: {Move(node.left, DOWN), Move(node.right, UP)}}

    semantics = {DOWN: down, UP: up}

    leaf_up = lambda node: {Move(node.right, UP)}


    # faz parse da string para criar a árvore de Simone
    # por enquanto apenas teste
    def __init__(self, regex_str):
        return

    # costura toda árvore
    def thread(self):
        sequence = self.in_order()
        parent = None

        for node in sequence:
           if parent:
                parent.thread(node)

           parent = None if node.right else node

        if parent:
            parent.thread('&')

    def in_order(self):
        return self.root.in_order()

    def simone(self):
        self.index = 0
        self.comp_to_state = {}
        self.initial = ''
        self.accepting = set()
        transitions = {}

        # fila de conjuntos de move para computar transições
        self.queue = [{Move(self.root, DOWN)}]
        while self.queue:
            moves = self.queue.pop()
            (leaves, state) = self.moves_to_state(moves)

            # dict para separar atual composição por caracter
            char_to_comp = {leaf.node.value: set() for leaf in leaves}
            for char in char_to_comp:
                char_to_comp[char] = \
                        {leaf for leaf in leaves if leaf.node.value == char}

            for char in char_to_comp:
                (leaves, next_state) = self.moves_to_state(char_to_comp[char])
                if state not in transitions:
                    transitions[state] = {}
                transitions[state][char] = next_state

        return DFA(transitions, self.initial, self.accepting)

    # a partir de um conjunto de moves, retorna a composição (folhas)
    # e o estado associado
    def moves_to_state(self, moves):
        # leaves é a união da composição de cada move
        leaves = set()
        for move in moves:
            leaves = leaves.union(move.simone_leaves())

        # nodos dos moves para identificar o estado
        # set imutável é hashable, para usar em dict
        nodes = frozenset(map(lambda leaf: leaf.node, leaves))

        state = ''

        # se o estado já existe, retorna o mesmo
        # senão cria o estado
        if nodes in self.comp_to_state:
            state = self.comp_to_state[nodes]
        else:
            # estado qi
            state = 'q' + str(self.index)

            # estado é inicial se ainda não há estado inicial
            if not self.initial:
                self.initial = state

            # é accepting se '&' faz parte da composição
            if '&' in nodes:
                self.accepting.add(state)

            self.index += 1
            self.comp_to_state[nodes] = state

            # coloca composição de moves na fila para
            # criar as transições
            self.queue.append(leaves)

        # '&' já foi tratado, pode ser retirado
        empty = {leaf for leaf in leaves if leaf.node == '&'}
        for leaf in empty:
            leaves.remove(leaf)

        return (leaves, state)
