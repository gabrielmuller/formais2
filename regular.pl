% AFND strings (a, b)* que terminam em 'bb'

state(q0).
state(q1).
state(q2).
state(q3).
state(q4).

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

path(From, String, To) :-
    state(From),
    state(To),
    [H|T] = String,
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

% accept_list([a, a, a]). false
% accept_list([a, b, b]). true

