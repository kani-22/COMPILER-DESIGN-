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
    result = []

    for ch in expr:
        if ch.isalnum():
            result.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            if stack:
                stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(ch):
                result.append(stack.pop())
            stack.append(ch)

    while stack:
        result.append(stack.pop())

    return ''.join(result)

def infix_to_prefix(expr):
    expr = expr[::-1]
    expr = expr.replace('(', 'temp').replace(')', '(').replace('temp', ')')
    postfix = infix_to_postfix(expr)
    return postfix[::-1]

def postfix_to_prefix(postfix):
    stack = []
    for ch in postfix:
        if ch.isalnum():
            stack.append(ch)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append(ch + op1 + op2)
    return stack[-1]

def prefix_to_postfix(prefix):
    stack = []
    for ch in prefix[::-1]:
        if ch.isalnum():
            stack.append(ch)
        else:
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op1 + op2 + ch)
    return stack[-1]

expr = input("Enter infix expression: ")
postfix = infix_to_postfix(expr)
prefix = infix_to_prefix(expr)

print("Postfix:", postfix)
print("Prefix:", prefix)

print("Postfix to Prefix:", postfix_to_prefix(postfix))
print("Prefix to Postfix:", prefix_to_postfix(prefix))
