#!/usr/bin/env python3

def good(equation):
    ex = 0
    equal = 0
    valid_chars = "X^+-=*/. 0123456789"
    for ch in equation:
        if ch not in valid_chars:
            return False
    for x in range(len(equation)):
        if equation[x] == "X":
            ex = 1
        elif equation[x] == "=":
            equal += 1
    if ex == 0 or equal != 1:
        return False
    return True 

def deg(equation):
    degr = []
    for x in range(len(equation)):
        if equation[x] == "^" and x != len(equation):
            degr.append(equation[x + 1])
    if len(degr) > 0:
        return max(degr)
    return 1

def check_part(part):
    part = part.strip()
    final = ""
    star,plus,moins,a, ex = 0,0,0,0,0
    for x in range(len(part)):
        if part[x] == "*":
            star = 1
        elif part[x] == "+":
            plus = 1
        elif part[x] == "X":
            ex = 1
        elif part[x] == "-":
            moins = 1
        elif part[x] == "^":
            a = 1
    if star == 0 and good(part):
        if a == 0 and moins == 1:
            final = "- 1 " + part[1:] + "^1"
        elif a == 0 and plus == 1:
            final = "+ 1 " + part[1:] + "^1"
        elif a == 0 and plus == 0 and moins == 0:
            final = "+ 1 " + part + "^1"   
        elif moins == 1:
            final = "- 1 *" + part[1:]
        elif plus == 1:
            final = "+ 1 *" + part[1:]
    elif star == 1 and good(part) and a == 0:
        final = part + "^1"
    elif star == 1 and ex == 0:
        final = str(eval(part))   
    else:
        return part
    return final


def redu(strs):
    import re
    x, power0, power1, power2, imagination, nondelta,impossible = 0, "X^0", "X^1", "X^2", 0, 1, 0
    x0, x1, x2, result = [], [], [], []
    total = {'x0': [], 'x1': [], 'x2': []}
    final = ""
    for x in range(len(strs)):
        if strs[x] == "=":
            break
    part1 = strs[:x].strip()
    part2 = strs[x + 1:].strip()
    part22 = ""
    for y in range(len(part2)):
        if part2[y] == "-":
            part22 = part22 + "+"
        elif part2[y] != "-" and y == 0:
            part22 = part22 + "-"
            part22 = part22 + part2[y]
        elif part2[y] == "+":
            part22 = part22 + "-"
        else:
            part22 = part22 + part2[y]
    reduced = part1 + part22
    parts = re.findall(r'[+-]?\s*[^+-]+', reduced)
    parts = [p.strip() for p in parts]
    for part in parts:
            part = check_part(part)
            for y in range(len(part)):
                if y + 1 < len(part) and part[y] == "^" and part[y + 1] == "0":
                    power0 = part[y-1:]
                    x0.append(part)
                    break
                elif y + 1 < len(part) and part[y] == "^" and part[y + 1] == "1":
                    power1 = part[y-1:]
                    x1.append(part)
                    break
                elif y + 1 < len(part) and part[y] == "^" and part[y + 1] == "2":
                    power2 = part[y-1:]
                    x2.append(part)
                    break
            else:
                x0.append(part)
    for part in x0:
        match = re.search(r'([+-]?\s*[\d.]+)', part)
        if match:
            num = float(match.group(1).replace(' ', ''))
            total['x0'].append(num)
    for part in x1:
        match = re.search(r'([+-]?\s*[\d.]+)', part)
        if match:
            num = float(match.group(1).replace(' ', ''))
            total['x1'].append(num)
    for part in x2:
        match = re.search(r'([+-]?\s*[\d.]+)', part)
        if match:
            num = float(match.group(1).replace(' ', ''))
            total['x2'].append(num)
    
    total['x0'] = sum(total['x0']) if total['x0'] else 0
    total['x1'] = sum(total['x1']) if total['x1'] else 0
    total['x2'] = sum(total['x2']) if total['x2'] else 0
    terms = []
    
    if total['x2'] != 0:
        terms.append(f"{total['x2']} * {power2}")
    if total['x1'] != 0:
        terms.append(f"{total['x1']} * {power1}")
    if total['x0'] != 0:
        terms.append(f"{total['x0']} * {power0}")
    if terms:
        final = terms[0]
        for term in terms[1:]:
            if term[0] == '-':
                final = final + " " + term
            else:
                final = final + " + " + term
    else:
        final = "0"

    a = total['x2']
    b = total['x1']
    c = total['x0']
    
    if a != 0:
        delta = b**2 - 4 * a * c
        if delta > 0:
            res1 = (-b + delta**0.5) / (2 * a)
            res2 = (-b - delta**0.5) / (2 * a)
            result.append(res1)
            result.append(res2)
        elif delta == 0:
            res = -b / (2*a)
            result.append(res)
        else:
            real = -b / (2*a)
            imag = (abs(delta)**0.5) / (2*a)
            imagination = 1
            result.append(real)
            result.append(imag)
    elif b != 0:
        nondelta = 0
        res1 = -(c/b)
        result.append(res1)
    elif c != 0:
        if a + b + c != 0:
            impossible = 1
        else:
            res = a + b + c
            result.append(res)
    
    return final, result, imagination, nondelta, impossible

def ft_analyse(equation):
    x = good(equation)
    degree1 = deg(equation)
    if x:
        reduced, result, imaginery, delta, impossible = redu(equation)
        degree = deg(reduced)
        print("Polynomial degree:", degree)
        if int(degree1) > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve.")
            return
        print("Reduced form:",reduced + " = 0")
        if len(result) == 2 and imaginery == 0 and delta:
            print("Discriminant is strictly positive, the two solutions are:")
            print(f"{result[0]:.4f}")
            print(f"{result[1]:.4f}")
        elif len(result) == 2 and imaginery == 1 and delta:
            print("Discriminant is strictly negative, the two complex solutions are:")
            print(f"{result[0]} + {result[1]:.4f}i")
            print(f"{result[0]} - {result[1]:.4f}i")
        elif len(result) == 1 and delta:
            print("The solution is:")
            print(f"{result[0]:.4f}")
        elif delta == 0:
            print(f"{result[0]:.4f}")
        elif impossible == 1:
            print("No solution!")
        elif impossible == 0:
            print("Any real number is a solution.")
    else:
        print("Bad Format")

    return
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ft_analyse(sys.argv[1])
    else:
        print("Please enter the equation with a good format")