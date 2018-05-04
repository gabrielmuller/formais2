class DFA:
    def __init__(self, transitions, initial, accepting):
        self.initial = initial

        # dicionário de dicionários
        self.transitions = transitions

        self.accepting = accepting

    def accepts(self, word):
        state = self.initial
        for char in word:
            if state not in self.transitions or \
            char not in self.transitions[state]:
                return False
            state = self.transitions[state][char]
        return (state in self.accepting)

    # lista de palavras da linguagem de certo tamanho
    def words_of_size(self, size):
        valid = lambda i : i[1] in self.accepting
        return {i[0] for i in filter(valid, self.word_state_size(size))}

    # função recursiva auxiliar
    # retorna conjunto de palavras de tamanho e o estado onde elas estão
    # não necessariamente em estados de aceitação
    def word_state_size(self, size):
        if size == 0:
            return [("", self.initial)]

        prev_words = self.word_state_size(size-1)
        words = set()

        for word in prev_words:
            for char, state in self.transitions[word[1]].items():
                words.add((word[0] + char, state))

        return words

