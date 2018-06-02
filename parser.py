from node import Node
from collections import deque

# retira espaços e outros caracteres inúteis,
# explicita todos operandos
def preprocess(string):
    output = ''
    last_char = ''
    operators = '|*?+.()'
    unary = '*+?'
    string = string.replace(' ', '')
    string = string.replace('.', '')

    # ++ é equivalente a +
    while '++' in string:
        string = string.replace('++', '+')

    for op in unary:
        string = string.replace('()' + op, '')

    string = string.replace('()', '')

    if string[-1] == '|':
        raise SyntaxError("Expressão inválida: termina em '|'")
    if string[0] == '|':
        raise SyntaxError("Expressão inválida: começa em '|'")

    for char in string:
        # condições para identificar string inválida
        a = not last_char or last_char == '|'
        b = char in unary
        c = last_char + char

        if a and b or (c == '||'):
            raise SyntaxError("Expressão inválida: " + c)

        if (last_char):

            # condições para identificar um '.' implícito
            a = last_char not in operators
            b = char not in operators or char == '('
            c = last_char in ')*?+'
            d = char == ')'
            e = char == '('

            if (b and (a or c)) or (d and e):
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
            front(stack).append(new_node)
        else:
            front(stack).append(node)
    if len(stack) != 1:
        raise SyntaxWarning("Faltam fechar " + str(len(stack)-1) + 
            "parêntesis. Isso será feito automaticamente.")
    return parse_or(front(stack))

def front(stack):
    if len(stack) == 0:
        raise SyntaxError("Há um ')' sem '(' correspondente!")
    return stack[-1]
            
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
    if len(nodes) == 1:
        return nodes[0]
    elif len(nodes) == 2:
        nodes[1].left = nodes[0]
        return nodes[1]

    # como não há '++',
    # mais de um operador unário é equivalente a um único '*'
    elif len(nodes) > 2:
        node = Node('*')
        node.left = nodes[0]
        return node

# cria árvore a partir da string
def parse(string):
    string = preprocess(string)
    nodes = [Node(char) for char in string]
    return parse_parenthesis(nodes)

