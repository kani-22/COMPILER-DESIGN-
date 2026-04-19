class DAGNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class DAG:
    def __init__(self):
        self.nodes = {}
        self.temp_count = 1

    def get_node(self, value):
        if value not in self.nodes:
            self.nodes[value] = DAGNode(value)
        return self.nodes[value]

    def build_from_postfix(self, postfix):
        stack = []

        for token in postfix:
            if token.isalnum():
                stack.append(self.get_node(token))
            else:
                right = stack.pop()
                left = stack.pop()
                temp = f"t{self.temp_count}"
                self.temp_count += 1

                node = self.get_node(temp)
                node.left = left
                node.right = right
                node.value = temp

                stack.append(node)

        return stack[-1]

    def print_dag(self, root, visited=None):
        if visited is None:
            visited = set()

        if root is None or root.value in visited:
            return

        visited.add(root.value)

        if root.left and root.right:
            print(f"{root.value} -> ({root.left.value}, {root.right.value})")
            self.print_dag(root.left, visited)
            self.print_dag(root.right, visited)
        else:
            print(f"{root.value}")

def infix_to_postfix(expr):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
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
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(ch, 0):
                output.append(stack.pop())
            stack.append(ch)

    while stack:
        output.append(stack.pop())

    return output

def main():
    expr = input("Enter infix expression: ")
    postfix = infix_to_postfix(expr)

    dag = DAG()
    root = dag.build_from_postfix(postfix)

    print("\nPostfix:", ''.join(postfix))
    print("\nDAG Representation:")
    dag.print_dag(root)

if __name__ == "__main__":
    main()
