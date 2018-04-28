path(From, List, To) :-
    state(From),
    state(To),
    [H|T] = List,
    char(H),

    transition(H, From, Next),
    state(Next),
    path(Next, T, To).

path(From, [], To) :-
    state(From),
    state(To),
    From = To.

accept_list(List) :-
    path(S, List, F),
    start_state(S),
    accept_state(F).

accept_list_size(List, Size) :-
    length(List, Size),
    accept_list(List).

list_string(List, String) :-
    var(String),
    atom_chars(Atom, List),
    atom_string(Atom, String), !.

list_string(List, String) :-
    var(List),
    atom_string(Atom, String),
    atom_chars(Atom, List), !.

accept_string(String) :-
    list_string(List, String),
    accept_list(List), !.

strings_of_size(Strings, Size) :-
    findall(String, 
    (accept_list_size(List, Size),
    list_string(List, String)), L),
    sort(L, Strings).

% ?- strings_of_size(Strings, 5).
