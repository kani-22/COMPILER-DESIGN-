from collections import defaultdict

def parse_grammar():
    n = int(input("Enter number of productions: "))
    grammar = defaultdict(list)

    print("Enter productions in the form A->aB|b")
    for _ in range(n):
        prod = input().replace(" ", "")
        lhs, rhs = prod.split("->")
        alternatives = rhs.split("|")
        grammar[lhs].extend(alternatives)

    return grammar


def is_non_terminal(ch):
    return ch.isupper()


def compute_leading(grammar):
    leading = {nt: set() for nt in grammar}

    changed = True
    while changed:
        changed = False
        for lhs in grammar:
            for rhs in grammar[lhs]:
                if not rhs:
                    continue

                first = rhs[0]

                if not is_non_terminal(first):
                    if first not in leading[lhs]:
                        leading[lhs].add(first)
                        changed = True
                else:
                    for sym in leading[first]:
                        if sym not in leading[lhs]:
                            leading[lhs].add(sym)
                            changed = True

                    if len(rhs) > 1 and not is_non_terminal(rhs[1]):
                        if rhs[1] not in leading[lhs]:
                            leading[lhs].add(rhs[1])
                            changed = True

    return leading


def compute_trailing(grammar):
    trailing = {nt: set() for nt in grammar}

    changed = True
    while changed:
        changed = False
        for lhs in grammar:
            for rhs in grammar[lhs]:
                if not rhs:
                    continue

                last = rhs[-1]

                if not is_non_terminal(last):
                    if last not in trailing[lhs]:
                        trailing[lhs].add(last)
                        changed = True
                else:
                    for sym in trailing[last]:
                        if sym not in trailing[lhs]:
                            trailing[lhs].add(sym)
                            changed = True

                    if len(rhs) > 1 and not is_non_terminal(rhs[-2]):
                        if rhs[-2] not in trailing[lhs]:
                            trailing[lhs].add(rhs[-2])
                            changed = True

    return trailing


def display_sets(title, sets_dict):
    print(f"\n{title}:")
    for nt in sorted(sets_dict.keys()):
        values = ", ".join(sorted(sets_dict[nt]))
        print(f"{title}({nt}) = {{ {values} }}")


def main():
    grammar = parse_grammar()
    leading = compute_leading(grammar)
    trailing = compute_trailing(grammar)

    display_sets("LEADING", leading)
    display_sets("TRAILING", trailing)


if __name__ == "__main__":
    main()
