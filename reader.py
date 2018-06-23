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
    if '$' in string:
        raise SyntaxError(\
            "Símbolo especial '$' não permitido.")

    initial = ''
    productions = {}
    lines = string.split('\n')
    lines = [x for x in lines if x.split() != []]

    
    for line in lines:
        if not line: continue
        if line.count('->') > 1:
            raise SyntaxError(\
                "'->' achado mais de uma vez na linha.")

        i = line.find('->')

        if i < 0:
            raise SyntaxError("'->' não achado.")

        left = line[:i].strip()
        right = line[i+2:]

        check_left(left, line)

        if not initial:
            initial = left

        check_rights(right, line)

        rights = right.split('|')

        if left not in productions:
            productions[left] = set()

        for right in rights:
            check_right(right,line)

            right = right.split()

            prod = []

            for char in right:
                if char.isupper():
                    prod.append(char)
                elif char[0].isupper() and len(char)>1:
                    if char[1:].isdigit():
                        prod.append(char)
                    else:
                        raise SyntaxError(\
                            "Não terminal deve ser composto apenas de 1 letra capitalizada \
                                e dígitos" + line)
                else:
                    prod.append(char)
            productions[left].add(tuple(prod))

    return (initial, productions)

# checagem de erros em GR

def check_left(left, line):
    if not left[0].isupper():
        raise SyntaxError(\
            "Símbolo não-terminal " + left + " deve ser capitalizado.")

def check_rights(right, line):
    if not right.split():
        raise SyntaxError(\
            "Lado direito não encontrado na linha " + line)
    if '|' == right[0]:
        raise SyntaxError(\
            "'|' é o primeiro símbolo no lado direito da linha " + line)
    if '|' == right[-1]:
        raise SyntaxError(\
            "'|' é o último símbolo no lado direito da linha " + line)

def check_right(right,line):
    if '&' in right and right.strip() is not '&':
        raise SyntaxError(\
            "'&' não pode aparecer concatenado")
    if not right.split():
        raise SyntaxError(\
            "dois '|' consecutivos na linha " + line)

