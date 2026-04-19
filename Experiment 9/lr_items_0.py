from collections import defaultdict, deque

class LR0Parser:
    def __init__(self, productions, start_symbol):
        self.productions = productions
        self.start_symbol = start_symbol
        self.aug_start = start_symbol + "'"
        self.productions[self.aug_start] = [[start_symbol]]

    def closure(self, items):
        closure_set = set(items)
        changed = True

        while changed:
            changed = False
            new_items = set()

            for lhs, rhs, dot in closure_set:
                if dot < len(rhs):
                    symbol = rhs[dot]
                    if symbol in self.productions:
                        for prod in self.productions[symbol]:
                            item = (symbol, tuple(prod), 0)
                            if item not in closure_set:
                                new_items.add(item)

            if new_items:
                closure_set |= new_items
                changed = True

        return frozenset(closure_set)

    def goto(self, items, symbol):
        moved = set()

        for lhs, rhs, dot in items:
            if dot < len(rhs) and rhs[dot] == symbol:
                moved.add((lhs, rhs, dot + 1))

        return self.closure(moved) if moved else frozenset()

    def canonical_collection(self):
        start_item = (self.aug_start, tuple([self.start_symbol]), 0)
        I0 = self.closure({start_item})

        states = [I0]
        transitions = {}
        queue = deque([I0])

        while queue:
            I = queue.popleft()
            transitions[I] = {}

            symbols = set()
            for lhs, rhs, dot in I:
                if dot < len(rhs):
                    symbols.add(rhs[dot])

            for symbol in symbols:
                next_state = self.goto(I, symbol)
                if next_state and next_state not in states:
                    states.append(next_state)
                    queue.append(next_state)
                if next_state:
                    transitions[I][symbol] = next_state

        return states, transitions

    def display_item(self, item):
        lhs, rhs, dot = item
        rhs = list(rhs)
        rhs.insert(dot, ".")
        return f"{lhs} -> {' '.join(rhs)}"

    def print_states(self, states, transitions):
        for i, state in enumerate(states):
            print(f"\nI{i}:")
            for item in sorted(state):
                print("  " + self.display_item(item))

        print("\nTransitions:")
        for i, state in enumerate(states):
            for symbol, next_state in transitions.get(state, {}).items():
                j = states.index(next_state)
                print(f"I{i} --{symbol}--> I{j}")


def parse_grammar():
    n = int(input("Enter number of productions: "))
    productions = defaultdict(list)

    print("Enter productions in the form A->aB|b")
    for _ in range(n):
        prod = input().replace(" ", "")
        lhs, rhs = prod.split("->")
        alternatives = rhs.split("|")
        for alt in alternatives:
            productions[lhs].append(list(alt) if alt != "ε" else [])

    start_symbol = list(productions.keys())[0]
    return productions, start_symbol


def main():
    productions, start_symbol = parse_grammar()
    parser = LR0Parser(productions, start_symbol)
    states, transitions = parser.canonical_collection()
    parser.print_states(states, transitions)


if __name__ == "__main__":
    main()
