class State:
    def __init__(self):
        self.transitions = {}   # symbol -> set of next states
        self.epsilon = set()    # epsilon transitions
        self.is_final = False


class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def add_transition(state, symbol, next_state):
    if symbol not in state.transitions:
        state.transitions[symbol] = set()
    state.transitions[symbol].add(next_state)


def insert_concat(regex):
    result = ""
    symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    prev = None

    for c in regex:
        if prev:
            if (prev in symbols or prev == '*' or prev == ')') and (c in symbols or c == '('):
                result += '.'
        result += c
        prev = c
    return result


def to_postfix(regex):
    prec = {'*': 3, '.': 2, '|': 1, '+': 1}
    output = []
    stack = []

    for c in regex:
        if c.isalnum():
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and prec.get(stack[-1], 0) >= prec.get(c, 0):
                output.append(stack.pop())
            stack.append(c)

    while stack:
        output.append(stack.pop())

    return ''.join(output)


def symbol_nfa(symbol):
    s1 = State()
    s2 = State()
    add_transition(s1, symbol, s2)
    return NFA(s1, s2)


def concat_nfa(nfa1, nfa2):
    nfa1.end.epsilon.add(nfa2.start)
    return NFA(nfa1.start, nfa2.end)


def union_nfa(nfa1, nfa2):
    s = State()
    e = State()
    s.epsilon.add(nfa1.start)
    s.epsilon.add(nfa2.start)
    nfa1.end.epsilon.add(e)
    nfa2.end.epsilon.add(e)
    return NFA(s, e)


def star_nfa(nfa):
    s = State()
    e = State()
    s.epsilon.add(nfa.start)
    s.epsilon.add(e)
    nfa.end.epsilon.add(nfa.start)
    nfa.end.epsilon.add(e)
    return NFA(s, e)


def plus_nfa(nfa1, nfa2):
    return union_nfa(nfa1, nfa2)


def regex_to_nfa(regex):
    regex = insert_concat(regex)
    postfix = to_postfix(regex)
    stack = []

    for c in postfix:
        if c.isalnum():
            stack.append(symbol_nfa(c))
        elif c == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat_nfa(nfa1, nfa2))
        elif c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))
        elif c == '+':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))
        elif c == '*':
            nfa = stack.pop()
            stack.append(star_nfa(nfa))

    result = stack.pop()
    result.end.is_final = True
    return result


def print_nfa(start_state):
    visited = set()
    queue = [start_state]
    state_id = {start_state: 0}
    count = 1

    while queue:
        state = queue.pop(0)
        sid = state_id[state]
        if state in visited:
            continue
        visited.add(state)

        if state.is_final:
            print(f"State q{sid} [final]")

        for symbol, next_states in state.transitions.items():
            for nxt in next_states:
                if nxt not in state_id:
                    state_id[nxt] = count
                    count += 1
                    queue.append(nxt)
                print(f"q{sid} --{symbol}--> q{state_id[nxt]}")

        for nxt in state.epsilon:
            if nxt not in state_id:
                state_id[nxt] = count
                count += 1
                queue.append(nxt)
            print(f"q{sid} --ε--> q{state_id[nxt]}")


# Example usage
regex = input("Enter regular expression: ")
nfa = regex_to_nfa(regex)
print("\nNFA transitions:")
print_nfa(nfa.start)
