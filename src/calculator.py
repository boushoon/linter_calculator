def tokenize(expr: str) -> list[str]:
    tokens = []
    i = 0
    length = len(expr)
    while i < length:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == '.':
            j = i
            dot_count = 0
            while j < length and (expr[j].isdigit() or expr[j] == '.'):
                if expr[j] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError(f"Некорректный формат числа в позиции {i}")
                j += 1
            token = expr[i:j]
            if token == ".":
                raise ValueError(f"Некорректный формат числа: '{token}'")
            tokens.append(token)
            i = j
        elif ch in '+-*/()':
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Неподдерживаемый символ '{ch}' в выражении")
    return tokens


def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


def infix_to_rpn(tokens: list[str]) -> list[str]:
    output_queue: list[str] = []
    op_stack: list[str] = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    for token in tokens:
        if is_number(token):
            output_queue.append(token)
        elif token in precedence:
            while op_stack and op_stack[-1] in precedence:
                top_op = op_stack[-1]
                if ((precedence[top_op] > precedence[token]) or
                        (precedence[top_op] == precedence[token])):
                    output_queue.append(op_stack.pop())
                else:
                    break
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if not op_stack or op_stack[-1] != '(':
                raise ValueError("Несбалансированные скобки: отсутствует '('.")
            op_stack.pop()
        else:
            raise ValueError(f"Неожиданный токен '{token}'")
    while op_stack:
        top = op_stack.pop()
        if top in ('(', ')'):
            raise ValueError("Несбалансированные скобки в выражении.")
        output_queue.append(top)
    return output_queue


def evaluate_rpn(rpn_tokens: list[str]) -> float:
    stack: list[float] = []
    for token in rpn_tokens:
        if is_number(token):
            stack.append(float(token))
        elif token in ('+', '-', '*', '/'):
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                res = a / b
            stack.append(res)
        else:
            raise ValueError(f"Неожиданный токен в RPN: '{token}'")
    if len(stack) != 1:
        raise ValueError(
            "Некорректное выражение: не хватает операторов")
    return stack[0]


def calculate(expr: str) -> float:
    tokens = tokenize(expr)
    rpn = infix_to_rpn(tokens)
    return evaluate_rpn(rpn)


def main():
    print("Интерактивный режим. Введите выражение или 'exit' для выхода.")
    while True:
        expr = input(">>> ")
        if not expr or expr.strip().lower() in ('exit', 'quit'):
            break
        try:
            result = calculate(expr)
            print(result)
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
