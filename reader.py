"""
    reader.py
    Funções para interpretar uma string
    como uma GLC.
"""
# retorna gramática regular a partir de string
def read_cfg(string):
    if not string:
        raise SyntaxError(\
            "Gramática vazia.")

    string = string.replace(' ', '')
    initial = ''
    productions = {}
    lines = string.split('\n')

    
    for line in lines:
        # aqui tem um continuiu
        if not line: continue

        i = line.find('->')

        if i < 0:
            raise SyntaxError("'->' não achado.")

        left = line[:i]
        right = line[i+2:]

        check_left(left, line)

        if not initial:
            initial = left

        check_rights(right, line)

        rights = right.split('|')

        if left not in productions:
            productions[left] = set()

        #beautiful
        for right in rights:
            check_right(right)

            symbol = ''
            prod = []

            for char in right:
                if not symbol:
                    if char.isupper():
                        symbol = char
                    else:
                        prod.append(char)
                elif char.isupper():
                    prod.append(symbol)
                    symbol = char
                elif char.islower():
                    prod.append(symbol)
                    prod.append(char)
                    symbol = ''
                elif char.isdigit():
                    symbol += char
                else:
                    raise SyntaxError("Caracter inválido " + char)

            if symbol:
                prod.append(symbol)
            productions[left].add(tuple(prod))

    return (initial, productions)

# checagem de erros em GR

def check_left(left, line):
    if not left[0].isupper():
        raise SyntaxError(\
            "Símbolo não-terminal " + left + " deve ser capitalizado.")

def check_rights(right, line):
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

def check_right(right):
    if '&' in right and right is not '&':
        raise SyntaxError(\
            "'&' não pode aparecer concatenado")

