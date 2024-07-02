from stack import *
from tokenizer import *

class ParenthesesError(Exception):
    pass

class InvalidOperatorError(Exception):
    pass

class InvalidExpressionError(Exception):
    pass

class CalculusError(Exception):
    pass

ALLOWED_CHARACTERS = "0123456789."

priority = {
    '+': 0,
    '-': 0,
    '_': 0,
    '*': 2,
    '/': 2,
    '^': 3
}


def calculate_operation(operation, number_1, number_2 = 0):
    if operation == '+':
        return number_1 + number_2
    elif operation == '-':
        return number_1 - number_2
    elif operation == '*':
        return number_1 * number_2
    elif operation == '/':
        if number_2 == 0:
            raise CalculusError("Neispravan izraz: deljenje nulom.")
        return number_1 / number_2
    elif operation == '^':
        return number_1 ** number_2
    elif operation == '_':
        return -number_1
    

def isNumber(str):
    return all(char in ALLOWED_CHARACTERS for char in str)


def validation(expression):
    open_parentheses = 0
    open_parentheses_index = 0
    close_parentheses = 0

    tokens = tokenize(expression)

    if len(tokens) == 0:
        raise EmptyExpressionError("Neispravan izraz: prazan string.")
    if tokens[0] in ("+-*/^"):
        raise InvalidOperatorError("Neispravan izraz: operator na prvom mestu u izrazu.")
    if len(tokens) == 1 and tokens[0] == '_':
        raise InvalidOperatorError("Neispravan izraz: postoji samo operator.")
    if tokens[-1] in ("+-*/^_"):
        raise InvalidOperatorError("Neispravan izraz: operator na kraju izraza.")
    
    for i in range(len(tokens)):
        if tokens[i] == '(':
            open_parentheses += 1
            open_parentheses_index = i
        elif tokens[i] == ')':
            close_parentheses += 1
            if i < open_parentheses_index:
                raise ParenthesesError("Neispravan izraz: zatvorena zagrada pre otvorene.")
            if i == open_parentheses_index + 1:
                raise ParenthesesError("Neispravan izraz: prazne zagrade.")
        elif tokens[i] in ("+-*/^"):
            if tokens[i+1] in ("+-*/^_"):
                raise InvalidOperatorError("Neispravan izraz: dva operatora jedan za drugim.")
            if i+1 < len(tokens) and tokens[i+1] == ')':
                raise InvalidExpressionError("Neispravan izraz: operator ispred zatvorene zagrade.")
            if tokens[i-1] == '(':
                raise InvalidExpressionError("Neispravan izraz: operator nakon otvorene zagrade.")
        elif isNumber(tokens[i]):
            if i+1 < len(tokens) and isNumber(tokens[i+1]):
                raise InvalidExpressionError("Neispravan izraz: dva broja jedan za drugim.")
        elif tokens[i] == '_':
            if i+1 < len(tokens) and not (isNumber(tokens[i+1]) or tokens[i+1] == '('):
                raise InvalidOperatorError("Neispravan izraz: unarni minus se ne nalazi pre cifre.")
    if open_parentheses != close_parentheses:
        raise ParenthesesError("Neispravan izraz: broj otvorenih i zatvorenih zagrada se ne poklapa.")
    
    return tokens


def infix_to_postfix(expression):
    tokens = validation(expression)
    stack = Stack()
    postfix = []

    for i in range(len(tokens)):
        if i+2 < len(tokens) and tokens[i] == '_' and isNumber(tokens[i+1]) and tokens[i+2] in ('+-)'):
            postfix.append('-' + tokens[i+1])
        elif isNumber(tokens[i]):
            if i + 1 < len(tokens) and i >= 1 and tokens[i-1] == '_' and tokens[i+1] in ('+-)'):
                continue
            postfix.append(tokens[i])
        elif tokens[i] == '(':
            stack.push(tokens[i])
        elif tokens[i] == ')':
            while stack.top() != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while not stack.is_empty() and stack.top() != '(' and priority[tokens[i]] <= priority[stack.top()]:
                postfix.append(stack.pop())
            stack.push(tokens[i])

    while not stack.is_empty():
        postfix.append(stack.pop())

    return postfix
    

def calculate_postfix(token_list):
    stack = Stack()
    for i in range(len(token_list)):
        if token_list[i] == '_':
            if stack.is_empty():
                raise CalculusError("Neispravan izraz: unarni minus bez broja.")
            number = stack.pop()
            stack.push(calculate_operation(token_list[i], float(number)))
        elif token_list[i] in ('+', '-', '*', '/', '^'):
            if stack.__len__() < 2:
                raise CalculusError("Neispravan izraz: nedovoljno operanada za operaciju.")
            number_1 = stack.pop()
            number_2 = stack.pop()
            stack.push(calculate_operation(token_list[i], float(number_2), float(number_1)))
        elif len(token_list[i]) > 1 and token_list[i][0] == '-':
            stack.push(-float(token_list[i][1:]))
        elif isNumber(token_list[i]):
            stack.push(token_list[i])
    
    if stack.__len__() != 1:
        raise CalculusError("Neispravan izraz: višak operanada.")
    
    try:
        result = float(stack.pop())
        if result.is_integer():
            return int(result)
        return result
    except TypeError:
        raise CalculusError("Neispravan izraz: rezultat je kompleksan broj.")


def calculate_infix(expression):
    postfix = infix_to_postfix(expression)
    return calculate_postfix(postfix)


if __name__ == '__main__':
    pass