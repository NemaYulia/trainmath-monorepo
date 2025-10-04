# exercises/arithmetic.py
import random
from fractions import Fraction
from .base import BaseProblem
import sympy as sp

class ArithmeticProblem(BaseProblem):
    slug = 'arithmetic'
    name = 'Усна лічба'

    def generate(self, difficulty):
        if difficulty == 1:
            rng = (1, 20); ops = ['+','-','*']; n = 2
        elif difficulty == 2:
            rng = (-50,50); ops = ['+','-','*','/']; n = 2
        else:
            rng = (-200,200); ops = ['+','-','*','/']; n = random.choice([3,4])

        operands = [random.randint(rng[0], rng[1]) for _ in range(n)]
        operators = [random.choice(ops) for _ in range(n-1)]

        # будувати вираз без eval для безпеки - через sympy
        x = sp.Symbol('x')
        expr = sp.Integer(operands[0])
        for op, val in zip(operators, operands[1:]):
            val_expr = sp.Integer(val)
            if op == '+':
                expr = expr + val_expr
            elif op == '-':
                expr = expr - val_expr
            elif op == '*':
                expr = expr * val_expr
            elif op == '/':
                # робимо дроби, уникаємо ділення на 0
                if val == 0:
                    val = 1
                    val_expr = sp.Integer(1)
                expr = expr / val_expr

        # canonical_answer як строка (в раціональному вигляді або float)
        try:
            ans = sp.nsimplify(expr)  # зведе до дробу, якщо це можливо
            canonical = str(ans)
        except Exception:
            canonical = str(float(expr))

        question_text = str(expr)
        return {
            'question': question_text,
            'canonical_answer': canonical,
            'params': {'operands':operands, 'operators':operators}
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
