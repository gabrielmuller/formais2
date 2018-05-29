class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

    # Nodo é um operador?
    def is_operator(self):
        return self.value in Regex.up

class Regex:
    # semantics
    up = \
    {'|': 'or',
    '.': 'concat',
    '?': 'interro',
    '*': 'kleene'}

    down = \
    {'|': 'or',
    '.': 'concat',
    '?': 'interro',
    '*': 'kleene'}
    # faz parse da string para criar a árvore de Simone
    # por enquanto apenas teste
    def __init__(self, regex_str):
        return

    def simone(self):
        return
