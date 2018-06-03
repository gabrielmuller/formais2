from parser import *
from nfa import NFA
from misc import crop

# Alias para claridade
DOWN = False
UP = True


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

        visited = {UP: set(), DOWN: set()}

        while moves:
            next_moves = set()

            for move in moves:
                if move.node == '&':
                    leaves.add(move)
                    continue
                if move.node.is_operator() :
                    if move.node not in visited[move.dir]:
                        func = Regex.semantics[move.dir][move.node.value]
                        next_moves = next_moves.union(func(move.node))
                        visited[move.dir].add(move.node)
                else:
                    if first:
                        func = Regex.leaf_up
                        next_moves = next_moves.union(func(move.node))
                    else:
                        leaves.add(move)

            moves = next_moves
            first = False

        return leaves

# semântica de subida do '|', a mais complicada
def or_up_semantics(node):
    while type(node) is Node and not node.up:
        node = node.right


    if type(node) is Node:
        return {Move(node.right, UP)}
    else:
        return {Move(node, UP)}

class Regex:

    # Semântica dos operadores
    # Operadores são mapeados a lambdas que 
    # têm como entrada um node e saída um conjunto de moves
    down = \
    {'|': lambda node: {Move(node.left, DOWN), Move(node.right, DOWN)},
    '.': lambda node: {Move(node.left, DOWN)},
    '?': lambda node: {Move(node.left, DOWN), Move(node.right, UP)},
    '+': lambda node: {Move(node.left, DOWN)},
    '*': lambda node: {Move(node.left, DOWN), Move(node.right, UP)}}

    up = \
    {'|': or_up_semantics,
    '.': lambda node: {Move(node.right, DOWN)},
    '?': lambda node: {Move(node.right, UP)},
    '+': lambda node: {Move(node.left, DOWN), Move(node.right, UP)},
    '*': lambda node: {Move(node.left, DOWN), Move(node.right, UP)}}

    semantics = {DOWN: down, UP: up}

    leaf_up = lambda node: {Move(node.right, UP)}


    # faz parse da string para criar a árvore de Simone
    def __init__(self, regex_str):
        self.regex_str = regex_str
        self.root = None
        if regex_str:
            self.root = parse(regex_str)
            self.thread()
        self.dfa = self.simone()
        self.dfa.name = crop("Regex " + self.regex_str)

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
        # se não há raiz, linguagem vazia
        if not self.root:
            return NFA({}, "q0", {})

        # se raiz é terminal, só uma palavra de um caracter
        if not self.root.is_operator():
            return NFA({"q0": {self.root.value: {"q1"}}, "q1": {}}, "q0", {"q1"})


        self.index = 0
        self.comp_to_state = {}
        self.accepting = set()
        self.transitions = {}
        self.initial = self.moves_to_state({Move(self.root, DOWN)})

        return NFA(self.transitions, self.initial, self.accepting)

    # a partir de um conjunto de moves (composição),
    # retorna o estado associado.
    # se o estado não existir é criado um novo estado.
    # a função se chama até que não hajam mais estados
    # a criar.
    def moves_to_state(self, moves):
        # leaves é a união da composição de cada move
        leaves = set()
        for move in moves:
            leaves = leaves.union(move.simone_leaves())

        # nodos dos moves para identificar o estado
        # set imutável é hashable, para usar em dict
        nodes = frozenset(map(lambda leaf: leaf.node, leaves))

        state = ''

        if not nodes:
            return (leaves, '-')
        # se o estado já existe, retorna o mesmo
        if nodes in self.comp_to_state:
            state = self.comp_to_state[nodes]
            return state

        # senão cria o estado

        # estado qi
        state = 'q' + str(self.index)
        self.transitions[state] = {}

        # é accepting se '&' faz parte da composição
        if '&' in nodes:
            self.accepting.add(state)

        self.index += 1
        self.comp_to_state[nodes] = state
        # print('\n&' if '&' in nodes else '')
        # print(state)
        # print([n.value for n in nodes if type(n) is Node])

        # '&' já foi tratado, pode ser retirado
        empty = {leaf for leaf in leaves if leaf.node == '&'}
        for leaf in empty:
            leaves.remove(leaf)

        # dict para separar atual composição por caracter
        char_to_comp = {leaf.node.value: set() for leaf in leaves}
        for char in char_to_comp:
            char_to_comp[char] = \
                    {leaf for leaf in leaves if leaf.node.value == char}

        for char in char_to_comp:
            next_state = self.moves_to_state(char_to_comp[char])
            if next_state != '-':
                self.transitions[state][char] = {next_state}

        return state

