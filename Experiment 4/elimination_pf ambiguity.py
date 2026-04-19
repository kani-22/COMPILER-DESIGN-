from collections import deque

def nfa_to_dfa(nfa, start_state, final_states, alphabet):
    def move(states, symbol):
        result = set()
        for state in states:
            result |= nfa.get(state, {}).get(symbol, set())
        return result

    dfa_states = []
    dfa_transitions = {}
    dfa_final_states = set()

    start = frozenset([start_state])
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()
        dfa_states.append(current)
        dfa_transitions[current] = {}

        if any(state in final_states for state in current):
            dfa_final_states.add(current)

        for symbol in alphabet:
            next_state = frozenset(move(current, symbol))
            dfa_transitions[current][symbol] = next_state

            if next_state and next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)

    return dfa_states, dfa_transitions, start, dfa_final_states


def print_dfa(dfa_states, dfa_transitions, start_state, final_states):
    print("DFA States:")
    for state in dfa_states:
        print("{" + ",".join(sorted(state)) + "}")

    print("\nStart State:")
    print("{" + ",".join(sorted(start_state)) + "}")

    print("\nFinal States:")
    for state in final_states:
        print("{" + ",".join(sorted(state)) + "}")

    print("\nTransition Table:")
    for state in dfa_states:
        for symbol, next_state in dfa_transitions[state].items():
            print(f"{{{','.join(sorted(state))}}} --{symbol}--> {{{','.join(sorted(next_state))}}}")


# Example NFA
# NFA transition format:
# nfa[state][symbol] = set of next states
nfa = {
    'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
    'q1': {'1': {'q2'}},
    'q2': {}
}
start_state = 'q0'
final_states = {'q2'}
alphabet = ['0', '1']

dfa_states, dfa_transitions, start, dfa_finals = nfa_to_dfa(
    nfa, start_state, final_states, alphabet
)

print_dfa(dfa_states, dfa_transitions, start, dfa_finals)
