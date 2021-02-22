import random

flag = "HSCTF{i_seriously_hope_you_didnt_solve_the_math_by_hand}"

equations = []
operators = ["^", "*", "+", "-", "<<", ">>", "~"]


for i in range(len(flag)):
    for _ in range(3):
        operator = random.choice(operators)
        if operator == "~":
            result = ~(ord(flag[i]))
            equations.append((-1, "~", i, result))
        elif operator == "<<" or operator == ">>":
            y = random.randint(1, 7)
            result = eval("(ord(flag[i]) " + operator + " y)")
            equations.append((i, operator, y, result))
        else:
            y = random.randint(0, len(flag)-1)
            result = eval("(ord(flag[i]) " + operator + " ord(flag[y]))")
            equations.append((i, operator, y, result))

random.shuffle(equations)

for i in range(len(equations)):
    x, operator, y, result = equations[i]
    if operator == "~":
        print(f"~flag[{y}] == {result}")
    elif operator == "<<" or operator == ">>":
        print(f"flag[{x}] {operator} {y} == {result}")
    else:
        print(f"flag[{x}] {operator} flag[{y}] == {result}")
