from node import Node
from collections import deque

# explicita todos operandos
def preprocess(string):
    operators = '|*?+.()'
    output = ''
    last_char = ''
    string = string.replace(' ', '')

    for char in string:
        if (last_char):
            # condições para identificar um '.' implícito
            a = last_char not in operators
            b = char not in operators or char == '('
            c = last_char in ')*?+'
            d = char not in operators

            if (a and b) or (c and d):
                output += '.'

        output += char
        last_char = char

    return output

# coloca nodos da lista em folhas de uma árvore, retorna a raiz
# parent é o valor dos nodos não folha
def treefy(nodes, parent):
    next_queue = deque(nodes)

    while len(next_queue) > 1:
        queue = next_queue
        next_queue = deque([])
            
        while queue:
            if len(queue) >= 2:
                n = Node(parent)
                n.left = queue.popleft()
                n.right = queue.popleft()
                next_queue.append(n)
            elif len(queue) == 1:
                next_queue.append(queue.popleft())
    return next_queue.popleft()
        
def parse_or(string):
    substrs = string.split('|')
    nodes = list(map(parse_concat, substrs))
    return treefy(nodes, '|')

def parse_concat(string):
    substrs = string.split('.')
    nodes = list(map(parse_unary, substrs))
    return treefy(nodes, '.')

def parse_unary(string):
    return Node(string)

# cria árvore a partir da string
def parse(string):
    string = preprocess(string)
    return parse_or(string)

