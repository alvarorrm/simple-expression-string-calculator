

def count_occurrences(char: str, string: str) -> int:
    """ Count the number of occurrences of a character inside a string """
    if not isinstance(string, str):
        raise TypeError(" the parameter <string> must be of type str")

    total = 0
    for c in string:
        if c == char:
            total += 1
    return total


def get_parenthesis_depths(expression):

    if ")(" in expression or "()" in expression:
        raise SyntaxError("')(' and '()' are not allowed")

    depths = []
    current_depth = 0
    for char in expression:
        if char == "(":
            current_depth += 1
            depths.append(current_depth)
        elif char == ")":
            depths.append(current_depth)
            current_depth -= 1
        else:
            depths.append(current_depth)
        if current_depth < 0:
            raise SyntaxError("Mismatched parentheses: missing opening parenthesis")

    if current_depth != 0:
        raise SyntaxError("Mismatched parentheses: missing closed parenthesis")

    return depths


def eval_simple_expression(expression):

    digits = "0123456789"
    special_characters = "+-*/^."
    valid_characters = digits + special_characters

    # Check format
    if expression[0] in "*/^.":
        raise SyntaxError("The expression can't start with any of these characters '*/^.'")
    if expression[-1] in "*/^.+-":
        raise SyntaxError("The expression can't end with any of these characters '*/^.+-'")

    for i, char in enumerate(expression):
        if char not in valid_characters:
            raise SyntaxError("The only valid characters are: '0123456789+-*/^.()'")
        if 0 < i < len(expression)-1 and char in special_characters and expression[i - 1] in special_characters:
            if not (char == "-" and expression[i + 1] in digits):
                raise SyntaxError("There can't be two special characters in a row (special characters = '+-*/^.'")

    # Remove leading "+"
    if expression[0] == "+":
        expression = expression[1:]

    # Split the expression into tokens
    # A token is either a number (including rational and negative numbers) or a special character

    tokens = []
    token = ""
    leading_negative = False

    # Add leading "-" to first token
    if expression[0] == "-":
        token = "-"
        leading_negative = True
        expression = expression[1:]

    # Split into tokens
    for char in expression:
        if char in digits + ".":
            token += char
        else:
            if token != "":
                tokens.append(token)
                token = ""
            tokens.append(char)
    if token != "":
        tokens.append(token)

    # Add negative signs to corresponding tokens
    tokens_with_negative_numbers = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "-" and tokens[i-1] in special_characters:
            tokens_with_negative_numbers.append("-" + tokens[i+1])
            i += 2
        else:
            tokens_with_negative_numbers.append(tokens[i])
            i += 1

    # Check there are not more than one decimal points in any token
    for token in tokens_with_negative_numbers:
        if count_occurrences(".", token) > 1:
            raise SyntaxError("There can't be a number with two decimal points: " + str(token))

    # Convert number tokens to their python types
    numeric_tokens = []
    for token in tokens_with_negative_numbers:
        if token in special_characters:
            numeric_tokens.append(token)
        else:
            if "." in token:
                numeric_tokens.append(float(token))
            else:
                numeric_tokens.append(int(token))

    # Fist pass to solve exponents
    tokens_after_powers = []
    i = len(numeric_tokens)-1
    while i >= 0:
        token = numeric_tokens[i]
        if token == "^":
            exponent = tokens_after_powers.pop(0)
            base = numeric_tokens[i-1]
            tokens_after_powers.insert(0, base**exponent)
            i -= 2
        else:
            tokens_after_powers.insert(0, token)
            i -= 1

    # Second pass to solve multiplications and divisions
    tokens_after_multdiv = []
    i = 0
    while i < len(tokens_after_powers):
        token = tokens_after_powers[i]
        if token == "*":
            a = tokens_after_multdiv.pop()
            b = tokens_after_powers[i+1]
            tokens_after_multdiv.append(a * b)
            i += 2
        elif token == "/":
            a = tokens_after_multdiv.pop()
            b = tokens_after_powers[i + 1]
            tokens_after_multdiv.append(a / b)
            i += 2
        else:
            tokens_after_multdiv.append(token)
            i += 1

    # Third pass to solve addition and subtraction
    tokens_after_addsub = []
    i = 0
    while i < len(tokens_after_multdiv):
        token = tokens_after_multdiv[i]
        if token == "+":
            a = tokens_after_addsub.pop()
            b = tokens_after_multdiv[i+1]
            tokens_after_addsub.append(a + b)
            i += 2
        elif token == "-":
            a = tokens_after_addsub.pop()
            b = tokens_after_multdiv[i + 1]
            tokens_after_addsub.append(a - b)
            i += 2
        else:
            tokens_after_addsub.append(token)
            i += 1

    return tokens_after_addsub[0]


def eval_expression(expression):
    parenthesis_depths = get_parenthesis_depths(expression)
    max_depth = max(parenthesis_depths)

    if all([i == 0 for i in parenthesis_depths]):
        result = eval_simple_expression(expression)

    splittable_exp = ""
    for i, char in enumerate(expression):
        if parenthesis_depths[i] == 0:
            splittable_exp += "#"
        else:
            splittable_exp += char

    subexpressions = [subexpression[1:-1] for subexpression in splittable_exp.split("#") if subexpression[1:-1] != ""]

    final_expression = ""
    subexpression_ix = 0
    prev_depth = 0
    for i, char in enumerate(expression):
        if parenthesis_depths[i] == 0:
            final_expression += char
            prev_depth = 0
        elif parenthesis_depths[i] == 1 and prev_depth == 0:
            final_expression += str(eval_expression(subexpressions[subexpression_ix]))
            subexpression_ix += 1
            prev_depth = 1

    return eval_simple_expression(final_expression)


expression_string = "((-4+(3-6)^(4*2-1))^(3*(2+3)))^(0.005)"

print(eval_expression(expression_string))

