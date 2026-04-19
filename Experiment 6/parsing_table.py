from collections import defaultdict

EPSILON = 'e'

class Grammar:
    def __init__(self):
        self.productions = defaultdict(list)
        self.non_terminals = []
        self.terminals = set()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)

    def add_production(self, lhs, rhs_list):
        if lhs not in self.non_terminals:
            self.non_terminals.append(lhs)
        for rhs in rhs_list:
            self.productions[lhs].append(rhs)

    def compute_terminals(self):
        nts = set(self.non_terminals)
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                for sym in rhs:
                    if sym != EPSILON and sym not in nts:
                        self.terminals.add(sym)

    def first_of_symbol(self, symbol):
        if symbol == EPSILON:
            return {EPSILON}
        if symbol not in self.productions:
            return {symbol}
        return self.first[symbol]

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for rhs in self.productions[nt]:
                    if rhs == EPSILON:
                        if EPSILON not in self.first[nt]:
                            self.first[nt].add(EPSILON)
                            changed = True
                        continue

                    add_epsilon = True
                    for symbol in rhs:
                        before = len(self.first[nt])
                        self.first[nt].update(self.first_of_symbol(symbol) - {EPSILON})
                        if len(self.first[nt]) != before:
                            changed = True

                        if EPSILON not in self.first_of_symbol(symbol):
                            add_epsilon = False
                            break

                    if add_epsilon:
                        if EPSILON not in self.first[nt]:
                            self.first[nt].add(EPSILON)
                            changed = True

    def first_of_string(self, symbols):
        result = set()
        if not symbols:
            result.add(EPSILON)
            return result

        for symbol in symbols:
            result.update(self.first_of_symbol(symbol) - {EPSILON})
            if EPSILON not in self.first_of_symbol(symbol):
                break
        else:
            result.add(EPSILON)

        return result

    def compute_follow(self, start_symbol):
        self.follow[start_symbol].add('$')
        changed = True

        while changed:
            changed = False
            for lhs in self.non_terminals:
                for rhs in self.productions[lhs]:
                    for i, B in enumerate(rhs):
                        if B not in self.productions:
                            continue

                        beta = rhs[i + 1:]
                        first_beta = self.first_of_string(beta)

                        before = len(self.follow[B])
                        self.follow[B].update(first_beta - {EPSILON})
                        if len(self.follow[B]) != before:
                            changed = True

                        if EPSILON in first_beta or not beta:
                            before = len(self.follow[B])
                            self.follow[B].update(self.follow[lhs])
                            if len(self.follow[B]) != before:
                                changed = True


def build_predictive_parsing_table(grammar):
    terminals = sorted(list(grammar.terminals)) + ['$']
    table = {nt: {t: '' for t in terminals} for nt in grammar.non_terminals}

    for lhs in grammar.non_terminals:
        for rhs in grammar.productions[lhs]:
            first_rhs = grammar.first_of_string(rhs)

            for terminal in first_rhs - {EPSILON}:
                table[lhs][terminal] = f"{lhs}->{rhs}"

            if EPSILON in first_rhs:
                for terminal in grammar.follow[lhs]:
                    table[lhs][terminal] = f"{lhs}->{rhs}"

    return table, terminals


def display_sets(grammar):
    print("FIRST sets:")
    for nt in grammar.non_terminals:
        print(f"FIRST({nt}) = {{ {', '.join(sorted(grammar.first[nt]))} }}")

    print("\nFOLLOW sets:")
    for nt in grammar.non_terminals:
        print(f"FOLLOW({nt}) = {{ {', '.join(sorted(grammar.follow[nt]))} }}")


def display_table(table, terminals, non_terminals):
    print("\nPredictive Parsing Table:")
    print(f"{'':8}", end="")
    for t in terminals:
        print(f"{t:12}", end="")
    print()

    for nt in non_terminals:
        print(f"{nt:8}", end="")
        for t in terminals:
            print(f"{table[nt][t]:12}", end="")
        print()


def main():
    g = Grammar()

    n = int(input("Enter number of productions: "))
    print("Enter productions in the form A->aB|b|e")
    for _ in range(n):
        prod = input().replace(" ", "")
        lhs, rhs = prod.split("->")
        rhs_list = rhs.split("|")
        g.add_production(lhs, rhs_list)

    g.compute_terminals()
    g.compute_first()
    start_symbol = g.non_terminals[0]
    g.compute_follow(start_symbol)

    display_sets(g)

    table, terminals = build_predictive_parsing_table(g)
    display_table(table, terminals, g.non_terminals)


if __name__ == "__main__":
    main()
