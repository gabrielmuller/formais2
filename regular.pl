% AFND strings (a, b)* que terminam em 'bb'

state(q0).
state(q1).
state(q2).

accept_state(q2).

char(a).
char(b).

transition(a, q0, q0).
transition(b, q0, q0).

transition(b, q0, q1).
transition(b, q1, q2).
transition(b, q2, q2).

transition(a, q1, q0).
transition(a, q2, q0).

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
    path(q0, List, F),
    accept_state(F).

accept_list_size(List, Size) :-
    length(List, Size),
    accept_list(List).

strings_of_size(Strings, Size) :-
    findall(String, 
    (accept_list_size(List, Size),
    atomic_list_concat(List, '', Atom),
    atom_string(Atom, String)),
    L),
    sort(L, Strings).

% ?- strings_of_size(String, 5).
