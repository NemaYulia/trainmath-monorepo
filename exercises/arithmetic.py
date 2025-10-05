# exercises/arithmetic.py
import random
from fractions import Fraction
from .base import BaseProblem
import sympy as sp

class ArithmeticProblem(BaseProblem):
    slug = 'arithmetic'
    name = 'Усна лічба'

    def generate(self, difficulty):
        op = random.choice(['+', '-', '*', '/'])
        return self._generate_op(op, difficulty)

    def generate_division(self, difficulty):
        return self._generate_op('/', difficulty)

    def _generate_op(self, op: str, difficulty: int) -> dict:
        # Select ranges per difficulty and operation
        if difficulty == 1:
            if op in ['+', '-', '/']:
                rng_a = (0, 50)
                rng_b = (0, 50)
            else:  # '*'
                rng_a = (-20, 20)
                rng_b = (-20, 20)
        elif difficulty == 2:
            rng_a = (-20, 20)
            rng_b = (-20, 20)
        else:
            rng_a = (-100, 100)
            rng_b = (-100, 100)

        if op == '+':
            a = random.randint(*rng_a)
            b = random.randint(*rng_b)
            expr = sp.Integer(a) + sp.Integer(b)
        elif op == '-':
            a = random.randint(*rng_a)
            b = random.randint(*rng_b)
            expr = sp.Integer(a) - sp.Integer(b)
        elif op == '*':
            a = random.randint(*rng_a)
            b = random.randint(*rng_b)
            expr = sp.Integer(a) * sp.Integer(b)
        else:  # '/'
            # Build dividend as divisor * quotient to guarantee integer result
            # Choose non-zero divisor in range_b
            possible_divisors = [d for d in range(rng_b[0], rng_b[1] + 1) if d != 0]
            b = random.choice(possible_divisors)
            # Choose quotient in range_a
            q = random.randint(rng_a[0], rng_a[1])
            a = b * q
            expr = sp.Integer(a) / sp.Integer(b)

        ans = sp.simplify(expr)
        canonical = str(int(ans)) if getattr(ans, 'is_integer', False) else str(ans)

        if op == '+':
            qtext = f"{a} + {b}"
        elif op == '-':
            qtext = f"{a} - {b}"
        elif op == '*':
            qtext = f"{a} * {b}"
        else:
            qtext = f"{a} / {b}"

        return {
            'question': qtext,
            'canonical_answer': canonical,
            'params': {'operands': [a, b], 'operators': [op], 'difficulty': difficulty}
        }

    def check(self, user_input, canonical_answer, params):
        # намагаємось розпізнати як дріб або символьний вираз через sympy
        try:
            user_expr = sp.sympify(user_input)
            correct_expr = sp.sympify(canonical_answer)
        except Exception:
            return False, "Не вдалося розпізнати ваш запис — спробуйте інший формат."

        diff = sp.simplify(user_expr - correct_expr)
        # diff може бути числом 0 або sympy.Zero
        is_correct = (diff == 0)
        return bool(is_correct), None
