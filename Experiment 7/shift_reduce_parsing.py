def shift_reduce_parse(input_string):
    stack = []
    grammar = ["E->E+E", "E->E*E", "E->(E)", "E->i"]

    print(f"{'STACK':<20}{'INPUT':<20}{'ACTION'}")
    print(f"{'$':<20}{input_string + '$':<20}Start")

    i = 0
    while i < len(input_string):
        stack.append(input_string[i])
        i += 1
        remaining = input_string[i:] + "$"
        print(f"{''.join(stack):<20}{remaining:<20}Shift")

        reduced = True
        while reduced:
            reduced = False
            stack_str = ''.join(stack)

            if stack_str.endswith("i"):
                stack[-1] = "E"
                print(f"{''.join(stack):<20}{remaining:<20}Reduce E->i")
                reduced = True

            elif stack_str.endswith("E+E"):
                stack = stack[:-3] + ["E"]
                print(f"{''.join(stack):<20}{remaining:<20}Reduce E->E+E")
                reduced = True

            elif stack_str.endswith("E*E"):
                stack = stack[:-3] + ["E"]
                print(f"{''.join(stack):<20}{remaining:<20}Reduce E->E*E")
                reduced = True

            elif stack_str.endswith("(E)"):
                stack = stack[:-3] + ["E"]
                print(f"{''.join(stack):<20}{remaining:<20}Reduce E->(E)")
                reduced = True

    while True:
        reduced = False
        stack_str = ''.join(stack)

        if stack_str.endswith("i"):
            stack[-1] = "E"
            print(f"{''.join(stack):<20}{'$':<20}Reduce E->i")
            reduced = True
        elif stack_str.endswith("E+E"):
            stack = stack[:-3] + ["E"]
            print(f"{''.join(stack):<20}{'$':<20}Reduce E->E+E")
            reduced = True
        elif stack_str.endswith("E*E"):
            stack = stack[:-3] + ["E"]
            print(f"{''.join(stack):<20}{'$':<20}Reduce E->E*E")
            reduced = True
        elif stack_str.endswith("(E)"):
            stack = stack[:-3] + ["E"]
            print(f"{''.join(stack):<20}{'$':<20}Reduce E->(E)")
            reduced = True

        if not reduced:
            break

    if len(stack) == 1 and stack[0] == "E":
        print(f"{''.join(stack):<20}{'$':<20}Accept")
    else:
        print(f"{''.join(stack):<20}{'$':<20}Reject")


# Example input
expr = input("Enter the input string using i, +, *, (, ): ")
shift_reduce_parse(expr)
