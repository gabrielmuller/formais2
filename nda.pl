% AFND strings (a, b)* que terminam em 'bb'

state(q0).
state(q1).
state(q2).

start_state(q0).
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
