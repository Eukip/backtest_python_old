

async def infixToPostfix(infix):
    result = ""
    precedence = {'&': 2, '|':3, '(':1}
    a = None
    b = None
    calc_stack = []
    stack = []

    for i in infix:
        if i.isdigit():
            result += str(i)
        else:
            if i == ' ':
                result = result
            elif i == '(':
                stack.append(i)

            elif i == ')':
                top = stack.pop()
                while top != '(':
                    result += top
                    top = stack.pop()
            else:
                while (not stack == []) and \
                        (precedence[stack[len(stack)-1]] >= precedence[i]):
                    result += stack.pop()
                stack.append(i)
    while not stack == []:
        result += stack.pop()

    for i in result:
        if i.isdigit():
            calc_stack.append(int(i))

        elif len(calc_stack) > 1:
            a = calc_stack.pop()
            b = calc_stack.pop()

            if i == '&':
                res = a and b
                calc_stack.append(res)
            elif i == '|':
                res = a or b
                calc_stack.append(res)
    res = calc_stack.pop()

    return res
