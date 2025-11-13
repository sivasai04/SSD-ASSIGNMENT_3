# Octal Calculator - README

## Overview
This is a complete implementation of a calculator that evaluates mathematical expressions using the octal (base-8) number system. All inputs are interpreted as octal numbers, and all outputs are returned in octal format.

## Features
1. **Arithmetic Operations**: +, -, *, /, %, ^ (exponentiation)
2. **PEMDAS Order of Operations**: Proper operator precedence with support for nested parentheses
3. **Variable Binding**: `LET <variable> = <value> IN <expression>` with local scoping
4. **User-Defined Functions**: `DEF <name>(<params>) = <expression>` with recursion support
5. **Conditional Expressions**: `IF <condition> THEN <expr1> ELSE <expr2>`
6. **Comparison Operators**: ==, !=, <, >, <=, >=

## Requirements
- Python 3.7 or higher
- No external libraries required (uses only standard library)

## Installation
No installation needed. Simply ensure all files are in the same directory:
- `octal_calculator.py` (main implementation)
- `exceptions.py` (custom exception classes)
- `test_cases.py` (comprehensive test suite)

## Usage

### Interactive Mode
Run the calculator in interactive mode:
```bash
python octal_calculator.py
```

This opens an interactive prompt where you can enter expressions:
```
>>> 10 + 7
Result: 17

>>> DEF square(x) = x * x
Result: 0

>>> square(5)
Result: 31
```

### Programmatic Usage
```python
from octal_calculator import OctalCalculator

calc = OctalCalculator()
result = calc.calculate("10 + 7")  # Returns "17"
```

### Running Tests
Execute the comprehensive test suite:
```bash
python test_cases.py
```

This runs over 60 test cases covering all features and edge cases.

## Examples

### Basic Arithmetic
```
10 + 7          → 17    (8 + 7 = 15 in decimal)
5 * 2           → 12    (5 * 2 = 10 in decimal)
20 / 3          → 5     (16 / 3 = 5 in decimal, integer division)
2 ^ 3           → 10    (2³ = 8 in decimal)
```

### Variables
```
LET x = 10 IN x + 7                     → 17
LET x = 5 IN LET y = 3 IN x * y         → 17
```

### Functions
```
DEF square(x) = x * x
square(5)                                → 31  (25 in decimal)

DEF add(x, y) = x + y
add(10, 7)                               → 17
```

### Recursive Functions
```
DEF fact(n) = IF n <= 1 THEN 1 ELSE n * fact(n - 1)
fact(5)                                  → 170  (120 in decimal)

DEF sum_squares(n) = IF n <= 0 THEN 0 ELSE n * n + sum_squares(n - 1)
sum_squares(5)                           → 67   (55 in decimal)
```

### Conditionals
```
IF 10 > 7 THEN 5 ELSE 3                 → 5
IF 5 == 5 THEN 10 + 1 ELSE 0            → 11
```


### Octal Conversion Strategy

#### Octal to Decimal
```python
def octal_to_decimal(octal_str):
    decimal = 0
    for i, digit in enumerate(reversed(octal_str)):
        decimal += int(digit) * (8 ** i)
    return decimal
```

#### Decimal to Octal
```python
def decimal_to_octal(decimal):
    if decimal == 0:
        return "0"
    digits = []
    while decimal > 0:
        digits.append(str(decimal % 8))
        decimal //= 8
    return ''.join(reversed(digits))
```

## Assertion Strategy

Assertions are used to validate:

### Pre-conditions
- Input types are correct (e.g., strings for octal, integers for decimal)
- Input values are valid (e.g., octal digits are 0-7)

### Invariants
- Token types are valid during parsing
- AST node types are recognized during evaluation
- Recursion depth stays within bounds

### Post-conditions
- Conversion functions return expected types
- Evaluation returns integer values
- Round-trip conversions preserve values

Example:
```python
def octal_to_decimal(octal_str: str) -> int:
    assert isinstance(octal_str, str), "Input must be string"
    assert octal_str, "Input cannot be empty"
    # ... conversion logic ...
    assert isinstance(result, int), "Result must be integer"
    return result
```

## Design Decisions

### 1. **Why Manual Octal Conversion?**
The assignment prohibits built-in functions like `oct()` and `int(x, 8)`. Manual implementation demonstrates understanding of number system conversion algorithms.

### 2. **Why Recursive Descent Parsing?**
- Simple to implement and understand
- Natural mapping to grammar rules
- Efficient for the expression language
- Easy to extend with new features

### 3. **Why Immutable Variable Scopes?**
Creating new dictionaries for each scope prevents side effects and makes debugging easier. While slightly less efficient, the clarity benefits outweigh performance costs for this use case.

### 4. **Why Global Function Storage?**
Functions are defined once and used multiple times. Storing them globally (rather than in the evaluation scope) matches how most programming languages work.

### 5. **Why AST Instead of Direct Evaluation?**
An AST provides:
- Clear separation of parsing and evaluation
- Better error reporting
- Easier to extend with new features
- Ability to optimize or transform expressions

## Assumptions

1. **Integer Arithmetic Only**: Division returns integer results (floor division). No floating-point support.

2. **Negative Numbers**: Supported via subtraction and negative literals (e.g., `0 - 5` or directly as operands).

3. **Exponentiation**: Only non-negative integer exponents are supported (negative exponents would require floating-point).

4. **Comparison Results**: Comparisons return 1 for true, 0 for false (in octal).

5. **Recursion Limit**: Hard limit of 1000 recursive calls to prevent stack overflow.

6. **Keywords**: All keywords (LET, IN, DEF, IF, THEN, ELSE) are case-sensitive and must be uppercase.

7. **Function Scope**: Functions can call other functions and themselves (recursion), but cannot be defined inside other functions.

8. **Variable Shadowing**: Inner LET bindings shadow outer variables with the same name.


## Performance Considerations

- **Lexing**: O(n) where n is input length
- **Parsing**: O(n) for most expressions, O(n²) for deeply nested structures
- **Evaluation**: O(n) for the AST size, but recursion can be expensive
- **Conversion**: O(log n) for number size

The calculator is optimized for correctness and clarity rather than raw performance.
