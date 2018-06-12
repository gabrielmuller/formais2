"""
    reader.py
    Funções para interpretar uma string
    como uma GLC.
"""
# retorna gramática regular a partir de string
def read_rg(string):
    string = string.replace(' ', '')
    initial = ''
    productions = {}
    lines = string.split('\n')

    
    for line in lines:
        i = line.find('->')

        if i < 0:
            raise SyntaxError("'->' não achado.")

        left = line[:i]
        right = line[i+2:]

        check_left(left, line)

        if not initial:
            initial = left

        check_right(right, line)

        rights = right.split('|')

        if left not in productions:
            productions[left] = set()
        for r in rights:
            check_r(r, left == initial)
            productions[left].add(r)

    return (initial, productions)

# checagem de erros em GR

def check_left(left, line):
    if not left[0].isupper():
        raise SyntaxError(\
            "Símbolo não-terminal " + left + " deve ser capitalizado.")

def check_right(right, line):
    if not right:
        raise SyntaxError(\
            "Lado direito não encontrado na linha " + line)
    if '|' == right[0]:
        raise SyntaxError(\
            "'|' é o primeiro símbolo no lado direito da linha " + line)
    if '|' == right[-1]:
        raise SyntaxError(\
            "'|' é o último símbolo no lado direito da linha " + line)
    if '||' in right:
        raise SyntaxError(\
            "dois '|' consecutivos na linha " + line)

def check_r(r, is_initial):
    if '&' in r and r is not '&':
        raise SyntaxError(\
            "'&' não pode aparecer acompanhado de outros símbolos.")
