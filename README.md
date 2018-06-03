# Editor de linguagens regulares
Projeto feito por Gabriel Müller e Juliana Pinheiro para disciplina de Linguagens Formais e Compiladores na UFSC. Feito na linguagem Python3 com o framework gráfico PyQt5.

## Instalação
TODO
## Funcionamento

### Autômatos (`class NFA`)
O trabalho usa extensivamente as estruturas de dados da linguagem para representações formais. As transições de um autômato são um `dict` (mapeamento) de estados para outros mapeamentos, de símbolo para um conjunto de estados. Além disso, há um conjunto de estados de aceitação e um estado inicial. Os estados são representado por strings.

    transitions = {
    'qo': {'a': {'q1', ' 'q2'}, 'b': {'q1'}},
    'q1': {'a': {'q0'}},
    'q2': {}
     }
### Expressões regulares (`class Regex`)
Utiliza-se o algoritmo de Simone para converter a árvore sintática de ER para um AFD. As semânticas dos operadores são representados for funções `lambda`. Uma diferença é o uso de semânticas de subida e descida também para o operador '+':

    down = \
    {'|': lambda node: {Move(node.left, DOWN), Move(node.right, DOWN)},
    '.': lambda node: {Move(node.left, DOWN)},
    '?': lambda node: {Move(node.left, DOWN), Move(node.right, UP)},
    '+': lambda node: {Move(node.left, DOWN)},
    '*': lambda node: {Move(node.left, DOWN), Move(node.right, UP)}}
        
    up = \
    {'|': or_up_semantics,
    '.': lambda node: {Move(node.right, DOWN)},
    '?': lambda node: {Move(node.right, UP)},
    '+': lambda node: {Move(node.left, DOWN), Move(node.right, UP)},
    '*': lambda node: {Move(node.left, DOWN), Move(node.right, UP)}}
    
    semantics = {DOWN: down, UP: up}
    
    leaf_up = lambda node: {Move(node.right, UP)}

A `class Node` representa nodos de uma árvore, enquanto a `class Move` representa um `Node` em conjunto com uma direção (subida ou descida). Há detecção de loops infinitos em casos como `(a | (b|c)*)*`, quando a árvore costurada apresenta ciclos entre nodos operadores.
### Gramáticas Regulares (`class RegularGrammar`)
TODO
### Operações
A maior parte das operações entre autômatos ou gramáticas são feitas por algoritmos conhecidos. Em especial, a eliminação de estados equivalentes na minimização usa o teorema de Myhill-Nerode:
TODO
### Análise (`parser.py`)
O parsing de expressões regulares e gramáticas regulares é feito respectivamente por `parse(string)` e `parse_rg(string)`. O parser ignora espaços e símbolos explícitos de concatenação ('.'). Há detecção de erro para vários casos de expressões inválidas.
