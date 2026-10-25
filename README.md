# computorV1

A command-line solver for polynomial equations of degree 2 or lower, written in Python 3.

Given an equation in the form `a * X^p + ... = b * X^q + ...`, it prints the reduced form, the polynomial degree, and the solution(s).

## Features

- Reduces the equation to the form `... = 0` (moves every term to the left side and merges like terms)
- Detects the polynomial degree
- Solves degree 0, 1 and 2 equations
- Reports the sign of the discriminant for degree 2:
  - strictly positive: two real solutions
  - zero: one real solution
  - strictly negative: two complex solutions
- Handles special cases: `Any real number is a solution`, `No solution`
- Refuses degree > 2: `The polynomial degree is strictly greater than 2, I can't solve.`
- Supports zero, negative and non-integer (decimal) coefficients
- Validates input characters and format (`Bad Format` on error)

## Requirements

- Python 3

## Usage

```bash
chmod +x computor.py
./computor.py "<equation>"
# or
python3 computor.py "<equation>"
```

The equation must be passed as **one quoted argument**. Each term follows the form `a * X^p`, with exponents explicit and ordered.

## Examples

```
$> ./computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
Polynomial degree: 2
Reduced form: 4.0 * X^0 + 4.0 * X^1 - 9.3 * X^2 = 0
Discriminant is strictly positive, the two solutions are:
-0.4751
0.9052

$> ./computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
Polynomial degree: 1
Reduced form: 1.0 * X^0 + 4.0 * X^1 = 0
The solution is:
-0.2500

$> ./computor.py "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
Polynomial degree: 3
The polynomial degree is strictly greater than 2, I can't solve.

$> ./computor.py "6 * X^0 = 6 * X^0"
Any real number is a solution.

$> ./computor.py "10 * X^0 = 15 * X^0"
No solution!

$> ./computor.py "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
Discriminant is strictly negative, the two complex solutions are:
-0.2 + 0.2000i
-0.2 - 0.2000i
```

> Exact output formatting (decimals, ordering) follows the current implementation; see [Known limitations](#known-limitations).

## How it works

| Function | Role |
|---|---|
| `good(equation)` | Validates allowed characters (`X^+-=*/. 0-9`), requires an `X` and exactly one `=` |
| `deg(equation)` | Finds the highest exponent following a `^` |
| `check_part(part)` | Normalizes each term to the `± a * X^p` form (e.g. `X` → `+ 1 * X^1`) |
| `redu(str)` | Moves the right side to the left, splits into terms, sums coefficients per power (`X^0`, `X^1`, `X^2`), builds the reduced form, and computes the solutions |
| `ft_analyse(equation)` | Main flow: validate, reduce, print degree, reduced form and solutions |

### Solving logic

- `a != 0`: discriminant `Δ = b² - 4ac`
  - `Δ > 0`: `x = (-b ± √Δ) / 2a`
  - `Δ = 0`: `x = -b / 2a`
  - `Δ < 0`: `x = -b / 2a ± i·√|Δ| / 2a`
- `a == 0, b != 0`: `x = -c / b`
- `a == 0, b == 0, c != 0`: no solution
- `a == b == c == 0`: every real number is a solution

## Known limitations

- Exponents are read as a single character after `^` (`X^10` is not supported).
- Output order and number formatting differ slightly from the subject's examples (degree is printed before the reduced form; `No solution!` vs `No solution.`; complex real part is not rounded).
- Coefficients are parsed with a simple regex; malformed terms may not be rejected.
- `eval()` is used on pure-numeric terms; input is restricted by `good()` but this is worth replacing with a safe parser.

## Project

Part of the 42 curriculum (`computor`).
