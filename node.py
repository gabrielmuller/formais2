class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

        # filho da direita está acima?
        self.up = False

    # Nodo é um operador?
    def is_operator(self):
        return self.value in '*.+?|'

    # Para debug
    def to_string(self):
        r = self.right.to_string() if type(self.right) is Node and not self.up else ''
        l = self.left.to_string() if type(self.left) is Node else ''
        if r or l:
            return str(self.value) + ': (' + l + ', ' + r + ')' 
        else:
            return str(self.value) 

    # costura esse nodo com um nodo acima
    def thread(self, up_node):
        self.up = True
        self.right = up_node

    def in_order(self):
        l = self.left.in_order() if self.left else []
        r = self.right.in_order() if self.right else []
        return l + [self] + r
