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

class Regex:
    # Semântica dos operadores
    down = \
    {'|': 'or',
    '.': lambda node: {node.left},
    '?': 'interro',
    '*': 'kleene'}

    up = \
    {'|': 'or',
    '.': lambda node: {node.right},
    '?': 'interro',
    '*': 'kleene'}

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
        return
