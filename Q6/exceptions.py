"""
Custom Exception Hierarchy for Octal Calculator

This module defines a hierarchical exception structure that provides
clear, informative error messages for all error scenarios in the calculator.

Exception Hierarchy:
    OctalCalculatorError (base)
    ├── InvalidOctalError
    ├── ParseError
    ├── RecursionLimitError
    ├── UndefinedVariableError
    ├── UndefinedFunctionError
    ├── InvalidArgumentCountError
    └── DivisionByZeroError

Design Rationale:
- All calculator exceptions inherit from OctalCalculatorError for easy catching
- Each exception type represents a specific error category
- Error messages provide context about what went wrong and where
"""


class OctalCalculatorError(Exception):
    """
    Base exception class for all octal calculator errors.
    
    This allows users to catch all calculator-specific errors with a single
    except clause while still providing detailed error information.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class InvalidOctalError(OctalCalculatorError):
    """
    Raised when an invalid octal digit is encountered.
    
    Octal numbers can only contain digits 0-7. This exception is raised
    when any other digit (8, 9) or non-digit character is found in a
    position where an octal number is expected.
    
    Example:
        "18 + 5" -> InvalidOctalError (8 is not valid in octal)
        "12.5 + 3" -> InvalidOctalError (decimal point not allowed)
    """
    def __init__(self, message: str):
        super().__init__(f"Invalid octal number: {message}")


class ParseError(OctalCalculatorError):
    """
    Raised when the expression cannot be parsed.
    
    This exception is raised for syntax errors such as:
    - Mismatched parentheses
    - Missing operators or operands
    - Unexpected tokens
    - Invalid expression structure
    
    Example:
        "5 + + 3" -> ParseError (double operator)
        "(5 + 3" -> ParseError (missing closing parenthesis)
        "5 3" -> ParseError (missing operator)
    """
    def __init__(self, message: str):
        super().__init__(f"Parse error: {message}")


class RecursionLimitError(OctalCalculatorError):
    """
    Raised when recursion depth exceeds the maximum limit.
    
    To prevent stack overflow and infinite recursion, the calculator
    limits recursive function calls to 1000 levels. This exception
    is raised when that limit is exceeded.
    
    Example:
        DEF infinite(n) = infinite(n + 1)
        infinite(0) -> RecursionLimitError
    """
    def __init__(self, message: str):
        super().__init__(f"Recursion limit exceeded: {message}")


class UndefinedVariableError(OctalCalculatorError):
    """
    Raised when attempting to use a variable that hasn't been defined.
    
    Variables must be defined using LET before they can be used.
    This exception is raised when a variable is referenced but not
    in the current scope.
    
    Example:
        "x + 5" -> UndefinedVariableError (x not defined)
        "LET x = 5 IN y + x" -> UndefinedVariableError (y not defined)
    """
    def __init__(self, message: str):
        super().__init__(f"Undefined variable: {message}")


class UndefinedFunctionError(OctalCalculatorError):
    """
    Raised when attempting to call a function that hasn't been defined.
    
    Functions must be defined using DEF before they can be called.
    This exception is raised when a function is called but not
    in the function registry.
    
    Example:
        "square(5)" -> UndefinedFunctionError (square not defined)
        "DEF f(x) = g(x)" and "f(5)" -> UndefinedFunctionError (g not defined)
    """
    def __init__(self, message: str):
        super().__init__(f"Undefined function: {message}")


class InvalidArgumentCountError(OctalCalculatorError):
    """
    Raised when a function is called with wrong number of arguments.
    
    Functions must be called with exactly the number of arguments
    they were defined with. This exception is raised when there's
    a mismatch.
    
    Example:
        DEF add(x, y) = x + y
        add(5) -> InvalidArgumentCountError (expects 2, got 1)
        add(5, 3, 2) -> InvalidArgumentCountError (expects 2, got 3)
    """
    def __init__(self, message: str):
        super().__init__(f"Invalid argument count: {message}")


class DivisionByZeroError(OctalCalculatorError):
    """
    Raised when attempting to divide or modulo by zero.
    
    Division and modulo operations require a non-zero divisor.
    This exception is raised when the divisor evaluates to zero.
    
    Example:
        "5 / 0" -> DivisionByZeroError
        "10 % 0" -> DivisionByZeroError
        "LET x = 0 IN 5 / x" -> DivisionByZeroError
    """
    def __init__(self, message: str):
        super().__init__(f"Division error: {message}")


# Additional utility function for exception handling
def format_error_context(expression: str, position: int, length: int = 1) -> str:
    """
    Format an error message with context showing where the error occurred.
    
    Args:
        expression: The full expression string
        position: Character position where error occurred
        length: Number of characters to highlight (default 1)
    
    Returns:
        Formatted string showing the error location
    
    Example:
        >>> format_error_context("5 + 8 + 3", 4, 1)
        '5 + 8 + 3
             ^
        Error at position 4'
    """
    lines = [
        expression,
        ' ' * position + '^' * length,
        f"Error at position {position}"
    ]
    return '\n'.join(lines)