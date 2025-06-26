import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):  
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.evaluate("2 + 3"), 5.0)

    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate("5 - 2"), 3.0)

    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate("4 * 3"), 12.0)

    def test_division(self):
        self.assertEqual(self.calculator.evaluate("8 / 2"), 4.0)

    def test_precedence_multiplication_addition(self):
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4"), 14.0)

    def test_precedence_division_subtraction(self):
        self.assertEqual(self.calculator.evaluate("10 - 8 / 2"), 6.0)

    def test_multiple_operators(self):
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4 - 1"), 13.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("5 / 0")

if __name__ == '__main__':
    unittest.main()