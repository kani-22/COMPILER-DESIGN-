def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    if op == '^':
        return 3
    return 0

def infix_to_postfix(expr):
    stack = []
    output = []
    for ch in expr.replace(" ", ""):
        if ch.isalnum():
            output.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(ch):
                output.append(stack.pop())
            stack.append(ch)
    while stack:
        output.append(stack.pop())
    return output

def generate_quadruples(postfix):
    stack = []
    quadruples = []
    temp_count = 1

    for token in postfix:
        if token.isalnum():
            stack.append(token)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = f"t{temp_count}"
            temp_count += 1
            quadruples.append((token, op1, op2, temp))
            stack.append(temp)

    return quadruples

def generate_triples(postfix):
    stack = []
    triples = []
    temp_index = 0

    for token in postfix:
        if token.isalnum():
            stack.append(token)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            triples.append((token, op1, op2))
            stack.append(f"({temp_index})")
            temp_index += 1

    return triples

def generate_indirect_triples(triples):
    pointer_table = list(range(len(triples)))
    return pointer_table, triples

def display_quadruples(quadruples):
    print("\nQuadruples:")
    print(f"{'No.':<5}{'Op':<8}{'Arg1':<8}{'Arg2':<8}{'Result':<8}")
    for i, q in enumerate(quadruples):
        op, arg1, arg2, result = q
        print(f"{i:<5}{op:<8}{arg1:<8}{arg2:<8}{result:<8}")

def display_triples(triples):
    print("\nTriples:")
    print(f"{'No.':<5}{'Op':<8}{'Arg1':<8}{'Arg2':<8}")
    for i, t in enumerate(triples):
        op, arg1, arg2 = t
        print(f"{i:<5}{op:<8}{arg1:<8}{arg2:<8}")

def display_indirect_triples(pointer_table, triples):
    print("\nIndirect Triples:")
    print(f"{'Ptr':<5}{'Triple Index':<12}")
    for i, p in enumerate(pointer_table):
        print(f"{i:<5}{p:<12}")

    print("\nReferenced Triples:")
    for i, t in enumerate(triples):
        op, arg1, arg2 = t
        print(f"{i}: ({op}, {arg1}, {arg2})")

def main():
    expr = input("Enter infix expression: ")
    postfix = infix_to_postfix(expr)

    print("\nPostfix expression:", ''.join(postfix))

    quadruples = generate_quadruples(postfix)
    triples = generate_triples(postfix)
    pointer_table, triples_ref = generate_indirect_triples(triples)

    display_quadruples(quadruples)
    display_triples(triples)
    display_indirect_triples(pointer_table, triples_ref)

if __name__ == "__main__":
    main()
