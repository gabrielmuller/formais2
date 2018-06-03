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
O programa permite criação de uma gramática, edição de gramática, exportar e importar (.txt), e operações de união, concatenação e fechamento. A edição de gramáticas na interface gráfica se dá apenas pela definição de suas produções, sem necessidade de definir alfabeto, Vn e Vt. Gramáticas também podem ser obtidas através da conversão de autômatos, bem como podem ser convertidas para autômatos.

A classe `RegularGrammar` é definida por um símbolo inicial e um dicionário de conjuntos representando as produções. Segue um exemplo de como as produções de uma gramática G são representadas:
    
    G: P = { S -> aA | ε 
             A -> aA | a }

    productions = {
        "S": {"aA", "&"},
        "A": {"aA", "a"}
    }
   
### Operações
Foram implementas as seguintes operações em Autômatos Finitos:
1. Complemento
2. União
3. Diferença
4. Intersecção
5. Reverso
6. Minimização
7. Determinização
8. Transformação em AFD Completo

E em Gramáticas Regulares:
1. Concatenação
2. União
3. Fechamento

A maior parte das operações entre autômatos ou gramáticas são feitas por algoritmos conhecidos. Em especial, a eliminação de estados equivalentes na minimização usa o teorema de Myhill-Nerode:
TODO
### Análise (`parser.py`)
O parsing de expressões regulares e gramáticas regulares é feito respectivamente por `parse(string)` e `parse_rg(string)`. O parser ignora espaços e símbolos explícitos de concatenação ('.'). Há detecção de erro para vários casos de expressões inválidas.
