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

def generate_three_address_code(postfix):
    stack = []
    temp_count = 1
    code = []

    for token in postfix:
        if token.isalnum():
            stack.append(token)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = f"t{temp_count}"
            temp_count += 1
            code.append(f"{temp} = {op1} {token} {op2}")
            stack.append(temp)

    return code, stack[-1]

def main():
    expr = input("Enter infix expression: ")
    postfix = infix_to_postfix(expr)
    code, result = generate_three_address_code(postfix)

    print("\nPostfix Expression:", ''.join(postfix))
    print("\nGenerated Code:")
    for line in code:
        print(line)

    print("\nFinal Result Stored In:", result)

if __name__ == "__main__":
    main()
