from node import Node
from collections import deque

# retira espaços e outros caracteres inúteis,
# explicita todos operandos
def preprocess(string):
    operators = '|*?+.()'
    output = ''
    last_char = ''
    string = string.replace(' ', '')
    string = string.replace('.', '')
    string = string.replace('()', '')

    for char in string:
        if (last_char):
            # condições para identificar um '.' implícito
            a = last_char not in operators
            b = char not in operators or char == '('
            c = last_char in ')*?+'
            d = char == ')'
            e = char == '('

            if (a and b) or (c and b) or (d and e):
                output += '.'

        output += char
        last_char = char

    return output

def parse_parenthesis(nodes):
    # pilha de lista de nodos
    stack = [[]]

    for node in nodes:
        char = node.value
        if char == '(':
            stack.append([])
        elif char == ')':
            new_node = parse_or(stack.pop())
            new_node.processed = True
            stack[-1].append(new_node)
        else:
            stack[-1].append(node)
    return parse_or(stack[0])
            
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
        
# divide lista de nodos em várias listas
# separadas por Node(char)
def split_nodes(nodes, char):
    lists = []
    sublist = []
    for node in nodes:
        if node.value == char and not node.processed:
            lists.append(sublist)
            sublist = []
        else:
            sublist.append(node)
    lists.append(sublist)
    return lists
    
def parse_or(nodes):
    lists = split_nodes(nodes, '|')
    nodes = [parse_concat(sublist) for sublist in lists]
    return treefy(nodes, '|')

def parse_concat(nodes):
    lists = split_nodes(nodes, '.')
    nodes = [parse_unary(sublist) for sublist in lists]
    return treefy(nodes, '.')

def parse_unary(nodes):
    child = None
    for node in nodes:
        if child:
            node.left = child
        child = node
    return child

# cria árvore a partir da string
def parse(string):
    string = preprocess(string)
    nodes = [Node(char) for char in string]
    return parse_parenthesis(nodes)

