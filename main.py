from rg import RegularGrammar
from dfa import DFA
from nfa import NFA

if __name__ == '__main__':

    transitions = {
        "A" : {'a' : 'G', 'b' : 'B'},
        "B" : {'a' : 'F', 'b' : 'E'},
        "C" : {'a' : 'C', 'b' : 'G'},
        "D" : {'a' : 'A', 'b' : 'H'},
        "E" : {'a' : 'E', 'b' : 'A'},
        "F" : {'a' : 'B', 'b' : 'C'},
        "G" : {'a' : 'G', 'b' : 'F'},
        "H" : {'a' : 'H', 'b' : 'D'},
    }

    exemplo = DFA(transitions, "A", {"A","D","G"})

    """
        Esperado:
        { 
            "A" : {'a' : "A", 'b' : "B"},
            "B" : {'a' : "B", 'b' : "C"},
            "A" : {'a' : "C", 'b' : "A"},
        }
    
    """

    exemplo.minimize()
    print(exemplo.transitions)







    
    

