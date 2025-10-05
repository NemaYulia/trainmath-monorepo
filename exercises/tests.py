from django.test import TestCase
from exercises.arithmetic import ArithmeticProblem
from exercises.algebraic import AlgebraicIdentitiesProblem
from exercises.exponential import ExponentialLogarithmProblem
from exercises.equations import EquationsProblem
from exercises.calculus import CalculusProblem
import sympy as sp

class ArithmeticProblemTest(TestCase):
    def setUp(self):
        self.problem = ArithmeticProblem()

    def test_generate_easy(self):
        result = self.problem.generate(1)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)
        self.assertIsInstance(result['question'], str)
        self.assertIsInstance(result['canonical_answer'], str)

    def test_generate_medium(self):
        result = self.problem.generate(2)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_hard(self):
        result = self.problem.generate(3)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_check_correct_answer(self):
        # Test with a simple arithmetic problem
        result = self.problem.generate(1)
        canonical = result['canonical_answer']
        params = result['params']
        
        is_correct, feedback = self.problem.check(canonical, canonical, params)
        self.assertTrue(is_correct)
        self.assertIsNone(feedback)

    def test_check_incorrect_answer(self):
        result = self.problem.generate(1)
        canonical = result['canonical_answer']
        params = result['params']
        
        is_correct, feedback = self.problem.check("wrong_answer", canonical, params)
        self.assertFalse(is_correct)

class AlgebraicIdentitiesProblemTest(TestCase):
    def setUp(self):
        self.problem = AlgebraicIdentitiesProblem()

    def test_generate_easy(self):
        result = self.problem.generate(1)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_medium(self):
        result = self.problem.generate(2)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_hard(self):
        result = self.problem.generate(3)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_check_correct_answer(self):
        result = self.problem.generate(1)
        canonical = result['canonical_answer']
        params = result['params']
        
        is_correct, feedback = self.problem.check(canonical, canonical, params)
        self.assertTrue(is_correct)

class ExponentialLogarithmProblemTest(TestCase):
    def setUp(self):
        self.problem = ExponentialLogarithmProblem()

    def test_generate_easy(self):
        result = self.problem.generate(1)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_medium(self):
        result = self.problem.generate(2)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_hard(self):
        result = self.problem.generate(3)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_check_correct_answer(self):
        result = self.problem.generate(1)
        canonical = result['canonical_answer']
        params = result['params']
        
        is_correct, feedback = self.problem.check(canonical, canonical, params)
        self.assertTrue(is_correct)

class EquationsProblemTest(TestCase):
    def setUp(self):
        self.problem = EquationsProblem()

    def test_generate_linear(self):
        result = self.problem.generate(1)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_complex_linear(self):
        result = self.problem.generate(2)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_quadratic(self):
        result = self.problem.generate(3)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_check_correct_answer(self):
        result = self.problem.generate(1)
        canonical = result['canonical_answer']
        params = result['params']
        
        is_correct, feedback = self.problem.check(canonical, canonical, params)
        self.assertTrue(is_correct)

class CalculusProblemTest(TestCase):
    def setUp(self):
        self.problem = CalculusProblem()

    def test_generate_basic_derivative(self):
        result = self.problem.generate(1)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_complex_derivative(self):
        result = self.problem.generate(2)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_generate_integral(self):
        result = self.problem.generate(3)
        self.assertIn('question', result)
        self.assertIn('canonical_answer', result)
        self.assertIn('params', result)

    def test_check_correct_answer(self):
        result = self.problem.generate(1)
        canonical = result['canonical_answer']
        params = result['params']
        
        is_correct, feedback = self.problem.check(canonical, canonical, params)
        self.assertTrue(is_correct)