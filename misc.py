def set_to_str(set_):
    string = ", ".join(sorted(list(set_)))
    return '[' + string + ']'

# a partir de uma matriz de strings,
# cria uma tabela legível.
def matrix_to_table(matrix):
    transpose = lambda m: list(zip(*m))
    matrix = transpose(matrix)
    nmatrix = []
    for col in matrix:
        length = max([len(line) for line in col])
        col = [line.center(length) for line in col]
        nmatrix.append(col)
    nmatrix = transpose(nmatrix)
    lines = '\n'.join(['  '.join(line) for line in nmatrix])
    return lines
