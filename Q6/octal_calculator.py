"""
Octal Calculator - Main Implementation
Evaluates mathematical expressions using octal number system (base-8)
Supports: arithmetic operations, variables, user-defined recursive functions, conditionals
"""

import re
from typing import Dict, List, Any, Tuple
from exceptions import (
    OctalCalculatorError,
    InvalidOctalError,
    ParseError,
    RecursionLimitError,
    UndefinedVariableError,
    UndefinedFunctionError,
    InvalidArgumentCountError,
    DivisionByZeroError
)


class OctalConverter:
    """Handles conversion between octal and decimal without using built-in functions"""
    
    @staticmethod
    def octal_to_decimal(octal_str: str) -> int:
        """
        Convert octal string to decimal integer
        Pre-condition: octal_str contains only valid octal digits (0-7)
        Post-condition: Returns equivalent decimal integer
        """
        assert isinstance(octal_str, str), "Input must be string"
        assert octal_str, "Input cannot be empty"
        
        # Handle negative numbers
        is_negative = octal_str.startswith('-')
        if is_negative:
            octal_str = octal_str[1:]
        
        # Validate octal digits
        for char in octal_str:
            if char not in '01234567':
                raise InvalidOctalError(f"Invalid octal digit '{char}' in '{octal_str}'")
        
        decimal = 0
        power = 0
        
        # Process from right to left
        for digit in reversed(octal_str):
            digit_value = int(digit)
            assert 0 <= digit_value <= 7, f"Invalid octal digit: {digit_value}"
            decimal += digit_value * (8 ** power)
            power += 1
        
        result = -decimal if is_negative else decimal
        assert isinstance(result, int), "Result must be integer"
        return result
    
    @staticmethod
    def decimal_to_octal(decimal: int) -> str:
        """
        Convert decimal integer to octal string
        Pre-condition: decimal is an integer
        Post-condition: Returns valid octal string representation
        """
        assert isinstance(decimal, int), "Input must be integer"
        
        if decimal == 0:
            return "0"
        
        is_negative = decimal < 0
        decimal = abs(decimal)
        
        octal_digits = []
        while decimal > 0:
            remainder = decimal % 8
            assert 0 <= remainder <= 7, f"Invalid remainder: {remainder}"
            octal_digits.append(str(remainder))
            decimal //= 8
        
        octal_str = ''.join(reversed(octal_digits))
        result = '-' + octal_str if is_negative else octal_str
        
        # Verify the conversion
        assert OctalConverter.octal_to_decimal(result) == (
            -int(''.join(reversed(octal_digits)), 8) if is_negative 
            else int(''.join(reversed(octal_digits)), 8)
        ), "Conversion verification failed"
        
        return result


class Token:
    """Represents a token in the expression"""
    def __init__(self, type_: str, value: Any):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    """Tokenizes input expressions"""
    
    KEYWORDS = {'LET', 'IN', 'DEF', 'IF', 'THEN', 'ELSE'}
    OPERATORS = {'+', '-', '*', '/', '%', '^'}
    COMPARATORS = {'==', '!=', '<=', '>=', '<', '>'}
    
    def __init__(self, text: str):
        assert isinstance(text, str), "Input must be string"
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if self.text else None
    
    def advance(self):
        """Move to next character"""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_number(self) -> str:
        """Read an octal number"""
        num_str = ''
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        assert num_str, "Number string cannot be empty"
        return num_str
    
    def read_identifier(self) -> str:
        """Read an identifier or keyword"""
        id_str = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        assert id_str, "Identifier cannot be empty"
        return id_str
    
    def tokenize(self) -> List[Token]:
        """
        Convert input text to list of tokens
        Pre-condition: text is valid expression string
        Post-condition: Returns list of valid tokens
        """
        tokens = []
        
        while self.current_char:
            self.skip_whitespace()
            
            if not self.current_char:
                break
            
            # Numbers
            if self.current_char.isdigit():
                num = self.read_number()
                tokens.append(Token('NUMBER', num))
            
            # Identifiers and keywords
            elif self.current_char.isalpha() or self.current_char == '_':
                id_str = self.read_identifier()
                if id_str in self.KEYWORDS:
                    tokens.append(Token('KEYWORD', id_str))
                else:
                    tokens.append(Token('IDENTIFIER', id_str))
            
            # Comparators (must check two-char operators first)
            elif self.pos + 1 < len(self.text) and self.text[self.pos:self.pos+2] in self.COMPARATORS:
                tokens.append(Token('COMPARATOR', self.text[self.pos:self.pos+2]))
                self.advance()
                self.advance()
            
            # Single character operators and comparators
            elif self.current_char in self.OPERATORS:
                tokens.append(Token('OPERATOR', self.current_char))
                self.advance()
            
            elif self.current_char in '<>':
                tokens.append(Token('COMPARATOR', self.current_char))
                self.advance()
            
            # Parentheses
            elif self.current_char == '(':
                tokens.append(Token('LPAREN', '('))
                self.advance()
            
            elif self.current_char == ')':
                tokens.append(Token('RPAREN', ')'))
                self.advance()
            
            # Comma
            elif self.current_char == ',':
                tokens.append(Token('COMMA', ','))
                self.advance()
            
            # Assignment
            elif self.current_char == '=':
                tokens.append(Token('EQUALS', '='))
                self.advance()
            
            else:
                raise ParseError(f"Unexpected character: '{self.current_char}'")
        
        assert all(isinstance(t, Token) for t in tokens), "All items must be tokens"
        return tokens


class Parser:
    """Parses tokens into an abstract syntax tree"""
    
    def __init__(self, tokens: List[Token]):
        assert isinstance(tokens, list), "Tokens must be a list"
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def expect(self, token_type: str, value: Any = None):
        """
        Expect a specific token type and optionally value
        Pre-condition: current_token exists
        Post-condition: advances if match, raises error otherwise
        """
        if not self.current_token:
            raise ParseError(f"Expected {token_type} but reached end of input")
        
        if self.current_token.type != token_type:
            raise ParseError(f"Expected {token_type} but got {self.current_token.type}")
        
        if value is not None and self.current_token.value != value:
            raise ParseError(f"Expected {value} but got {self.current_token.value}")
        
        token = self.current_token
        self.advance()
        return token
    
    def parse(self):
        """
        Parse the token stream
        Returns AST node representing the expression
        """
        if not self.tokens:
            raise ParseError("Empty expression")
        
        result = self.parse_expression()
        
        # Ensure all tokens are consumed
        if self.current_token:
            raise ParseError(f"Unexpected token after expression: {self.current_token}")
        
        return result
    
    def parse_expression(self):
        """Parse a complete expression (handles LET, DEF, IF)"""
        if self.current_token and self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'LET':
                return self.parse_let()
            elif self.current_token.value == 'DEF':
                return self.parse_def()
            elif self.current_token.value == 'IF':
                return self.parse_if()
        
        return self.parse_comparison()
    
    def parse_let(self):
        """Parse LET binding"""
        self.expect('KEYWORD', 'LET')
        var_name = self.expect('IDENTIFIER').value
        self.expect('EQUALS')
        value_expr = self.parse_comparison()
        self.expect('KEYWORD', 'IN')
        body_expr = self.parse_expression()
        
        return {
            'type': 'LET',
            'variable': var_name,
            'value': value_expr,
            'body': body_expr
        }
    
    def parse_def(self):
        """Parse function definition"""
        self.expect('KEYWORD', 'DEF')
        func_name = self.expect('IDENTIFIER').value
        self.expect('LPAREN')
        
        params = []
        if self.current_token and self.current_token.type != 'RPAREN':
            params.append(self.expect('IDENTIFIER').value)
            while self.current_token and self.current_token.type == 'COMMA':
                self.advance()
                params.append(self.expect('IDENTIFIER').value)
        
        self.expect('RPAREN')
        self.expect('EQUALS')
        body = self.parse_expression()
        
        return {
            'type': 'DEF',
            'name': func_name,
            'params': params,
            'body': body
        }
    
    def parse_if(self):
        """Parse conditional expression"""
        self.expect('KEYWORD', 'IF')
        condition = self.parse_comparison()
        self.expect('KEYWORD', 'THEN')
        then_expr = self.parse_expression()
        self.expect('KEYWORD', 'ELSE')
        else_expr = self.parse_expression()
        
        return {
            'type': 'IF',
            'condition': condition,
            'then': then_expr,
            'else': else_expr
        }
    
    def parse_comparison(self):
        """Parse comparison expressions"""
        left = self.parse_additive()
        
        while self.current_token and self.current_token.type == 'COMPARATOR':
            op = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = {
                'type': 'COMPARISON',
                'operator': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_additive(self):
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and \
              self.current_token.value in ['+', '-']:
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = {
                'type': 'BINARY_OP',
                'operator': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_multiplicative(self):
        """Parse multiplication, division, and modulo"""
        left = self.parse_exponentiation()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and \
              self.current_token.value in ['*', '/', '%']:
            op = self.current_token.value
            self.advance()
            right = self.parse_exponentiation()
            left = {
                'type': 'BINARY_OP',
                'operator': op,
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_exponentiation(self):
        """Parse exponentiation (right associative)"""
        left = self.parse_primary()
        
        if self.current_token and self.current_token.type == 'OPERATOR' and \
           self.current_token.value == '^':
            self.advance()
            right = self.parse_exponentiation()  # Right associative
            return {
                'type': 'BINARY_OP',
                'operator': '^',
                'left': left,
                'right': right
            }
        
        return left
    
    def parse_primary(self):
        """Parse primary expressions (numbers, variables, function calls, parentheses)"""
        # Parentheses
        if self.current_token and self.current_token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        
        # Numbers
        if self.current_token and self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return {'type': 'NUMBER', 'value': value}
        
        # Variables or function calls
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.advance()
            
            # Function call
            if self.current_token and self.current_token.type == 'LPAREN':
                self.advance()
                args = []
                
                if self.current_token and self.current_token.type != 'RPAREN':
                    args.append(self.parse_comparison())
                    while self.current_token and self.current_token.type == 'COMMA':
                        self.advance()
                        args.append(self.parse_comparison())
                
                self.expect('RPAREN')
                return {
                    'type': 'FUNCTION_CALL',
                    'name': name,
                    'args': args
                }
            
            # Variable
            return {'type': 'VARIABLE', 'name': name}
        
        raise ParseError(f"Unexpected token: {self.current_token}")


class Evaluator:
    """Evaluates the AST"""
    
    MAX_RECURSION_DEPTH = 1000
    
    def __init__(self):
        self.functions: Dict[str, Dict] = {}
        self.recursion_depth = 0
        self.converter = OctalConverter()
    
    def evaluate(self, node, variables: Dict[str, int] = None):
        """
        Evaluate an AST node
        Pre-condition: node is valid AST structure
        Post-condition: returns decimal integer result
        """
        if variables is None:
            variables = {}
        
        assert isinstance(variables, dict), "Variables must be dictionary"
        
        # Check recursion depth for ALL recursive calls, not just function calls
        if self.recursion_depth > self.MAX_RECURSION_DEPTH:
            raise RecursionLimitError(
                f"Recursion depth exceeded maximum of {self.MAX_RECURSION_DEPTH}"
            )
        
        node_type = node['type']
        
        if node_type == 'NUMBER':
            octal_value = node['value']
            result = self.converter.octal_to_decimal(octal_value)
            assert isinstance(result, int), "Number evaluation must return integer"
            return result
        
        elif node_type == 'VARIABLE':
            var_name = node['name']
            if var_name not in variables:
                raise UndefinedVariableError(f"Variable '{var_name}' is not defined")
            result = variables[var_name]
            assert isinstance(result, int), "Variable value must be integer"
            return result
        
        elif node_type == 'BINARY_OP':
            left = self.evaluate(node['left'], variables)
            right = self.evaluate(node['right'], variables)
            op = node['operator']
            
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise DivisionByZeroError("Division by zero")
                return left // right
            elif op == '%':
                if right == 0:
                    raise DivisionByZeroError("Modulo by zero")
                return left % right
            elif op == '^':
                assert right >= 0, "Negative exponents not supported"
                return left ** right
        
        elif node_type == 'COMPARISON':
            left = self.evaluate(node['left'], variables)
            right = self.evaluate(node['right'], variables)
            op = node['operator']
            
            if op == '==':
                return 1 if left == right else 0
            elif op == '!=':
                return 1 if left != right else 0
            elif op == '<':
                return 1 if left < right else 0
            elif op == '>':
                return 1 if left > right else 0
            elif op == '<=':
                return 1 if left <= right else 0
            elif op == '>=':
                return 1 if left >= right else 0
        
        elif node_type == 'LET':
            value = self.evaluate(node['value'], variables)
            new_vars = variables.copy()
            new_vars[node['variable']] = value
            return self.evaluate(node['body'], new_vars)
        
        elif node_type == 'DEF':
            self.functions[node['name']] = {
                'params': node['params'],
                'body': node['body']
            }
            return 0  # DEF returns 0
        
        elif node_type == 'IF':
            condition_result = self.evaluate(node['condition'], variables)
            if condition_result != 0:  # Non-zero is true
                return self.evaluate(node['then'], variables)
            else:
                return self.evaluate(node['else'], variables)
        
        elif node_type == 'FUNCTION_CALL':
            func_name = node['name']
            
            if func_name not in self.functions:
                raise UndefinedFunctionError(f"Function '{func_name}' is not defined")
            
            # Increment recursion depth
            self.recursion_depth += 1
            
            try:
                func_def = self.functions[func_name]
                params = func_def['params']
                body = func_def['body']
                args = node['args']
                
                if len(args) != len(params):
                    raise InvalidArgumentCountError(
                        f"Function '{func_name}' expects {len(params)} arguments, "
                        f"got {len(args)}"
                    )
                
                # Evaluate arguments
                arg_values = [self.evaluate(arg, variables) for arg in args]
                
                # Create new variable scope
                new_vars = variables.copy()
                for param, value in zip(params, arg_values):
                    new_vars[param] = value
                
                result = self.evaluate(body, new_vars)
                assert isinstance(result, int), "Function must return integer"
                return result
            
            finally:
                self.recursion_depth -= 1
        
        raise ParseError(f"Unknown node type: {node_type}")


class OctalCalculator:
    """Main calculator interface"""
    
    def __init__(self):
        self.evaluator = Evaluator()
        self.converter = OctalConverter()
    
    def calculate(self, expression: str) -> str:
        """
        Calculate expression in octal
        Pre-condition: expression is valid octal expression string
        Post-condition: returns result as octal string
        """
        assert isinstance(expression, str), "Expression must be string"
        assert expression.strip(), "Expression cannot be empty"
        
        try:
            # Tokenize
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Evaluate
            result_decimal = self.evaluator.evaluate(ast)
            
            # Convert back to octal
            result_octal = self.converter.decimal_to_octal(result_decimal)
            
            assert isinstance(result_octal, str), "Result must be octal string"
            return result_octal
        
        except OctalCalculatorError:
            raise
        except RecursionError as e:
            raise RecursionLimitError(f"Python recursion limit exceeded: {str(e)}")
        except Exception as e:
            raise OctalCalculatorError(f"Unexpected error: {str(e)}")


def main():
    """Main entry point for interactive calculator"""
    calculator = OctalCalculator()
    
    print("Octal Calculator")
    print("=" * 50)
    print("All inputs and outputs are in octal (base-8)")
    print("Commands: DEF, LET, IF-THEN-ELSE")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            expr = input(">>> ").strip()
            
            if expr.lower() == 'quit':
                break
            
            if not expr:
                continue
            
            result = calculator.calculate(expr)
            print(f"Result: {result}\n")
        
        except OctalCalculatorError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()