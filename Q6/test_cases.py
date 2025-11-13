"""
Comprehensive Test Suite for Octal Calculator

Tests cover:
1. Octal conversion (octal to decimal and decimal to octal)
2. Basic arithmetic operations
3. PEMDAS order of operations
4. Variable binding (LET)
5. Function definitions and calls
6. Recursive functions
7. Conditional expressions (IF-THEN-ELSE)
8. Edge cases and error handling
9. Complex feature interactions
"""

import unittest
from octal_calculator import OctalCalculator, OctalConverter
from exceptions import (
    InvalidOctalError,
    ParseError,
    RecursionLimitError,
    UndefinedVariableError,
    UndefinedFunctionError,
    InvalidArgumentCountError,
    DivisionByZeroError
)


class TestOctalConverter(unittest.TestCase):
    """Test octal to decimal and decimal to octal conversions"""
    
    def setUp(self):
        self.converter = OctalConverter()
    
    def test_octal_to_decimal_basic(self):
        """Test basic octal to decimal conversions"""
        self.assertEqual(self.converter.octal_to_decimal("0"), 0)
        self.assertEqual(self.converter.octal_to_decimal("1"), 1)
        self.assertEqual(self.converter.octal_to_decimal("7"), 7)
        self.assertEqual(self.converter.octal_to_decimal("10"), 8)
        self.assertEqual(self.converter.octal_to_decimal("17"), 15)
        self.assertEqual(self.converter.octal_to_decimal("20"), 16)
        self.assertEqual(self.converter.octal_to_decimal("100"), 64)
    
    def test_octal_to_decimal_large(self):
        """Test larger octal numbers"""
        self.assertEqual(self.converter.octal_to_decimal("777"), 511)
        self.assertEqual(self.converter.octal_to_decimal("1234"), 668)
        self.assertEqual(self.converter.octal_to_decimal("7777"), 4095)
    
    def test_octal_to_decimal_negative(self):
        """Test negative octal numbers"""
        self.assertEqual(self.converter.octal_to_decimal("-10"), -8)
        self.assertEqual(self.converter.octal_to_decimal("-77"), -63)
    
    def test_octal_to_decimal_invalid(self):
        """Test invalid octal digits"""
        with self.assertRaises(InvalidOctalError):
            self.converter.octal_to_decimal("8")
        with self.assertRaises(InvalidOctalError):
            self.converter.octal_to_decimal("19")
        with self.assertRaises(InvalidOctalError):
            self.converter.octal_to_decimal("ABC")
    
    def test_decimal_to_octal_basic(self):
        """Test basic decimal to octal conversions"""
        self.assertEqual(self.converter.decimal_to_octal(0), "0")
        self.assertEqual(self.converter.decimal_to_octal(1), "1")
        self.assertEqual(self.converter.decimal_to_octal(7), "7")
        self.assertEqual(self.converter.decimal_to_octal(8), "10")
        self.assertEqual(self.converter.decimal_to_octal(15), "17")
        self.assertEqual(self.converter.decimal_to_octal(16), "20")
        self.assertEqual(self.converter.decimal_to_octal(64), "100")
    
    def test_decimal_to_octal_large(self):
        """Test larger decimal numbers"""
        self.assertEqual(self.converter.decimal_to_octal(511), "777")
        self.assertEqual(self.converter.decimal_to_octal(668), "1234")
    
    def test_decimal_to_octal_negative(self):
        """Test negative decimal numbers"""
        self.assertEqual(self.converter.decimal_to_octal(-8), "-10")
        self.assertEqual(self.converter.decimal_to_octal(-63), "-77")
    
    def test_conversion_roundtrip(self):
        """Test that conversions are reversible"""
        for decimal in [0, 1, 7, 8, 15, 64, 511, -8, -63]:
            octal = self.converter.decimal_to_octal(decimal)
            back = self.converter.octal_to_decimal(octal)
            self.assertEqual(back, decimal)


class TestBasicArithmetic(unittest.TestCase):
    """Test basic arithmetic operations"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_addition(self):
        """Test addition in octal"""
        self.assertEqual(self.calc.calculate("10 + 7"), "17")  # 8 + 7 = 15 (octal 17)
        self.assertEqual(self.calc.calculate("5 + 3"), "10")   # 5 + 3 = 8 (octal 10)
        self.assertEqual(self.calc.calculate("77 + 1"), "100") # 63 + 1 = 64 (octal 100)
    
    def test_subtraction(self):
        """Test subtraction in octal"""
        self.assertEqual(self.calc.calculate("10 - 7"), "1")   # 8 - 7 = 1
        self.assertEqual(self.calc.calculate("20 - 10"), "10") # 16 - 8 = 8 (octal 10)
    
    def test_multiplication(self):
        """Test multiplication in octal"""
        self.assertEqual(self.calc.calculate("5 * 2"), "12")   # 5 * 2 = 10 (octal 12)
        self.assertEqual(self.calc.calculate("10 * 10"), "100") # 8 * 8 = 64 (octal 100)
    
    def test_division(self):
        """Test integer division in octal"""
        self.assertEqual(self.calc.calculate("10 / 2"), "4")   # 8 / 2 = 4
        self.assertEqual(self.calc.calculate("17 / 2"), "7")   # 15 / 2 = 7
        self.assertEqual(self.calc.calculate("20 / 3"), "5")   # 16 / 3 = 5
    
    def test_modulo(self):
        """Test modulo operation in octal"""
        self.assertEqual(self.calc.calculate("10 % 3"), "2")   # 8 % 3 = 2
        self.assertEqual(self.calc.calculate("17 % 10"), "7")  # 15 % 8 = 7
    
    def test_exponentiation(self):
        """Test exponentiation in octal"""
        self.assertEqual(self.calc.calculate("2 ^ 3"), "10")   # 2^3 = 8 (octal 10)
        self.assertEqual(self.calc.calculate("5 ^ 2"), "31")   # 5^2 = 25 (octal 31)
        self.assertEqual(self.calc.calculate("10 ^ 2"), "100") # 8^2 = 64 (octal 100)
    
    def test_division_by_zero(self):
        """Test division by zero error"""
        with self.assertRaises(DivisionByZeroError):
            self.calc.calculate("5 / 0")
        with self.assertRaises(DivisionByZeroError):
            self.calc.calculate("10 % 0")


class TestPEMDAS(unittest.TestCase):
    """Test order of operations (PEMDAS)"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_multiplication_before_addition(self):
        """Test that multiplication happens before addition"""
        self.assertEqual(self.calc.calculate("2 + 3 * 4"), "16")  # 2 + 12 = 14 (octal 16)
    
    def test_parentheses_override(self):
        """Test that parentheses override order"""
        self.assertEqual(self.calc.calculate("(2 + 3) * 4"), "24")  # 5 * 4 = 20 (octal 24)
    
    def test_nested_parentheses(self):
        """Test nested parentheses"""
        self.assertEqual(self.calc.calculate("((2 + 3) * 4) + 1"), "25")  # 20 + 1 = 21 (octal 25)
    
    def test_exponentiation_right_associative(self):
        """Test that exponentiation is right associative"""
        # 2^2^3 = 2^(2^3) = 2^8 = 256 = octal 400
        self.assertEqual(self.calc.calculate("2 ^ 2 ^ 3"), "400")
    
    def test_complex_expression(self):
        """Test complex expression with multiple operators"""
        # 3 + 4 * 2 - 1 = 3 + 8 - 1 = 10 (octal 12)
        self.assertEqual(self.calc.calculate("3 + 4 * 2 - 1"), "12")


class TestVariables(unittest.TestCase):
    """Test LET variable binding"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_simple_let(self):
        """Test simple LET binding"""
        self.assertEqual(self.calc.calculate("LET x = 10 IN x + 7"), "17")
    
    def test_let_with_expression(self):
        """Test LET with expression as value"""
        self.assertEqual(self.calc.calculate("LET x = 5 + 3 IN x * 2"), "20")
    
    def test_nested_let(self):
        """Test nested LET bindings"""
        self.assertEqual(
            self.calc.calculate("LET x = 5 IN LET y = 3 IN x + y"),
            "10"
        )
    
    def test_let_scoping(self):
        """Test that LET creates local scope"""
        self.assertEqual(
            self.calc.calculate("LET x = 5 IN LET x = 10 IN x"),
            "10"
        )
    
    def test_undefined_variable(self):
        """Test undefined variable error"""
        with self.assertRaises(UndefinedVariableError):
            self.calc.calculate("x + 5")
        with self.assertRaises(UndefinedVariableError):
            self.calc.calculate("LET x = 5 IN y + x")


class TestFunctions(unittest.TestCase):
    """Test function definition and calls"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_simple_function(self):
        """Test simple function definition and call"""
        self.calc.calculate("DEF square(x) = x * x")
        self.assertEqual(self.calc.calculate("square(5)"), "31")  # 25 in octal
    
    def test_function_with_multiple_params(self):
        """Test function with multiple parameters"""
        self.calc.calculate("DEF add(x, y) = x + y")
        self.assertEqual(self.calc.calculate("add(5, 3)"), "10")
    
    def test_function_with_expression(self):
        """Test function with complex expression"""
        self.calc.calculate("DEF compute(x, y) = x * x + y * y")
        self.assertEqual(self.calc.calculate("compute(3, 4)"), "31")  # 9 + 16 = 25 (octal 31)
    
    def test_undefined_function(self):
        """Test undefined function error"""
        with self.assertRaises(UndefinedFunctionError):
            self.calc.calculate("unknown(5)")
    
    def test_invalid_argument_count(self):
        """Test invalid argument count error"""
        self.calc.calculate("DEF f(x, y) = x + y")
        with self.assertRaises(InvalidArgumentCountError):
            self.calc.calculate("f(5)")
        with self.assertRaises(InvalidArgumentCountError):
            self.calc.calculate("f(5, 3, 2)")


class TestRecursion(unittest.TestCase):
    """Test recursive functions"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_factorial(self):
        """Test recursive factorial function"""
        self.calc.calculate("DEF fact(n) = IF n <= 1 THEN 1 ELSE n * fact(n - 1)")
        self.assertEqual(self.calc.calculate("fact(5)"), "170")  # 120 in octal
    
    def test_fibonacci(self):
        """Test recursive fibonacci function"""
        self.calc.calculate("DEF fib(n) = IF n <= 1 THEN n ELSE fib(n - 1) + fib(n - 2)")
        # fib(10) where 10 is octal (8 in decimal)
        # fib(8) = 21 in decimal = 25 in octal
        self.assertEqual(self.calc.calculate("fib(10)"), "25")
    
    def test_sum_squares(self):
        """Test the example from assignment"""
        self.calc.calculate("DEF sum_squares(n) = IF n <= 0 THEN 0 ELSE n * n + sum_squares(n - 1)")
        # sum_squares(5) where 5 is octal (5 in decimal)
        # sum = 5^2 + 4^2 + 3^2 + 2^2 + 1^2 = 25+16+9+4+1 = 55 = octal 67
        self.assertEqual(self.calc.calculate("sum_squares(5)"), "67")
    
    def test_recursion_limit(self):
        """Test recursion limit is enforced"""
        self.calc.calculate("DEF infinite(n) = infinite(n + 1)")
        with self.assertRaises(RecursionLimitError):
            self.calc.calculate("infinite(0)")


class TestConditionals(unittest.TestCase):
    """Test IF-THEN-ELSE conditionals"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_simple_if_true(self):
        """Test simple IF with true condition"""
        self.assertEqual(self.calc.calculate("IF 10 > 7 THEN 5 ELSE 3"), "5")
    
    def test_simple_if_false(self):
        """Test simple IF with false condition"""
        self.assertEqual(self.calc.calculate("IF 5 > 10 THEN 5 ELSE 3"), "3")
    
    def test_equality_comparison(self):
        """Test equality comparisons"""
        self.assertEqual(self.calc.calculate("IF 5 == 5 THEN 1 ELSE 0"), "1")
        self.assertEqual(self.calc.calculate("IF 5 == 3 THEN 1 ELSE 0"), "0")
    
    def test_inequality_comparison(self):
        """Test inequality comparisons"""
        self.assertEqual(self.calc.calculate("IF 5 != 3 THEN 1 ELSE 0"), "1")
        self.assertEqual(self.calc.calculate("IF 5 != 5 THEN 1 ELSE 0"), "0")
    
    def test_less_than_or_equal(self):
        """Test <= comparison"""
        self.assertEqual(self.calc.calculate("IF 5 <= 10 THEN 1 ELSE 0"), "1")
        self.assertEqual(self.calc.calculate("IF 5 <= 5 THEN 1 ELSE 0"), "1")
        self.assertEqual(self.calc.calculate("IF 10 <= 5 THEN 1 ELSE 0"), "0")
    
    def test_greater_than_or_equal(self):
        """Test >= comparison"""
        self.assertEqual(self.calc.calculate("IF 10 >= 5 THEN 1 ELSE 0"), "1")
        self.assertEqual(self.calc.calculate("IF 5 >= 5 THEN 1 ELSE 0"), "1")
        self.assertEqual(self.calc.calculate("IF 5 >= 10 THEN 1 ELSE 0"), "0")
    
    def test_nested_conditionals(self):
        """Test nested IF expressions"""
        self.assertEqual(
            self.calc.calculate("IF 5 > 3 THEN IF 10 > 7 THEN 1 ELSE 2 ELSE 3"),
            "1"
        )
    
    def test_conditional_with_variables(self):
        """Test conditionals with LET variables"""
        self.assertEqual(
            self.calc.calculate("LET x = 10 IN IF x > 5 THEN x + 1 ELSE x - 1"),
            "11"
        )


class TestComplexInteractions(unittest.TestCase):
    """Test complex interactions between features"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_function_with_let(self):
        """Test function that uses LET"""
        self.calc.calculate("DEF compute(x) = LET y = x * 2 IN y + x")
        self.assertEqual(self.calc.calculate("compute(5)"), "17")  # 5*2 + 5 = 15 (octal 17)
    
    def test_nested_function_calls(self):
        """Test nested function calls"""
        self.calc.calculate("DEF double(x) = x * 2")
        self.calc.calculate("DEF quadruple(x) = double(double(x))")
        self.assertEqual(self.calc.calculate("quadruple(3)"), "14")  # 3*4 = 12 (octal 14)
    
    def test_function_with_conditional(self):
        """Test function containing conditional"""
        self.calc.calculate("DEF abs(x) = IF x < 0 THEN 0 - x ELSE x")
        self.assertEqual(self.calc.calculate("abs(5)"), "5")
    
    def test_recursive_with_multiple_params(self):
        """Test recursive function with multiple parameters"""
        self.calc.calculate("DEF gcd(a, b) = IF b == 0 THEN a ELSE gcd(b, a % b)")
        # gcd(30, 14) where 30 octal = 24 decimal, 14 octal = 12 decimal
        # gcd(24, 12) = 12 decimal = 14 octal
        self.assertEqual(self.calc.calculate("gcd(30, 14)"), "14")
    
    def test_all_features_combined(self):
        """Test expression using all features"""
        # Define a complex recursive function with conditionals and variables
        self.calc.calculate(
            "DEF complex(n, m) = "
            "IF n <= 0 THEN m "
            "ELSE LET x = n * n IN x + complex(n - 1, m)"
        )
        result = self.calc.calculate("complex(3, 5)")
        # complex(3, 5) = 9 + complex(2, 5) = 9 + 4 + complex(1, 5) = 9 + 4 + 1 + 5 = 19 (octal 23)
        self.assertEqual(result, "23")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        self.calc = OctalCalculator()
    
    def test_zero_operations(self):
        """Test operations with zero"""
        self.assertEqual(self.calc.calculate("0 + 5"), "5")
        self.assertEqual(self.calc.calculate("5 - 5"), "0")
        self.assertEqual(self.calc.calculate("0 * 100"), "0")
        self.assertEqual(self.calc.calculate("0 ^ 10"), "0")
    
    def test_one_operations(self):
        """Test operations with one"""
        self.assertEqual(self.calc.calculate("1 * 5"), "5")
        self.assertEqual(self.calc.calculate("5 ^ 1"), "5")
    
    def test_large_numbers(self):
        """Test with larger octal numbers"""
        self.assertEqual(self.calc.calculate("777 + 1"), "1000")
        self.assertEqual(self.calc.calculate("1000 - 1"), "777")
    
    def test_empty_parentheses_error(self):
        """Test that empty parentheses cause error"""
        with self.assertRaises(ParseError):
            self.calc.calculate("()")
    
    def test_mismatched_parentheses(self):
        """Test mismatched parentheses"""
        with self.assertRaises(ParseError):
            self.calc.calculate("(5 + 3")
        with self.assertRaises(ParseError):
            self.calc.calculate("5 + 3)")
    
    def test_invalid_syntax(self):
        """Test various invalid syntax"""
        with self.assertRaises(ParseError):
            self.calc.calculate("5 + + 3")
        with self.assertRaises(ParseError):
            self.calc.calculate("* 5")
    
    def test_function_no_params(self):
        """Test function with no parameters"""
        self.calc.calculate("DEF get_five() = 5")
        self.assertEqual(self.calc.calculate("get_five()"), "5")


def run_tests():
    """Run all tests and print results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOctalConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicArithmetic))
    suite.addTests(loader.loadTestsFromTestCase(TestPEMDAS))
    suite.addTests(loader.loadTestsFromTestCase(TestVariables))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestRecursion))
    suite.addTests(loader.loadTestsFromTestCase(TestConditionals))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexInteractions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)