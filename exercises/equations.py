# exercises/equations.py
import random
import sympy as sp
from .base import BaseProblem

class EquationsProblem(BaseProblem):
    slug = 'equations'
    name = 'Linear Equations'

    def generate(self, difficulty):
        if difficulty == 1:
            # Easy: Simple linear equations
            return self._generate_linear_equation()
        elif difficulty == 2:
            # Medium: More complex linear equations
            return self._generate_complex_linear()
        else:
            # Hard: Still linear, more steps
            return self._generate_complex_linear()

    def _generate_linear_equation(self):
        x = sp.Symbol('x')
        
        # Generate ax + b = c
        a = random.randint(1, 10)
        b = random.randint(-10, 10)
        c = random.randint(-20, 20)
        
        # Calculate solution
        solution = (c - b) / a
        
        # Create equation
        left_side = a * x + b
        equation = sp.Eq(left_side, c)
        
        question = f"Solve for x: {sp.latex(equation)}"
        canonical_answer = str(solution)
        
        return {
            'question': question,
            'canonical_answer': canonical_answer,
            'params': {
                'a': a,
                'b': b,
                'c': c,
                'type': 'linear_simple'
            }
        }

    def _generate_complex_linear(self):
        x = sp.Symbol('x')
        
        # Generate equations like: ax + b = cx + d
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = random.randint(1, 5)
        d = random.randint(-10, 10)
        
        # Ensure a != c to have a unique solution
        while a == c:
            c = random.randint(1, 5)
        
        # Calculate solution
        solution = (d - b) / (a - c)
        
        # Create equation
        left_side = a * x + b
        right_side = c * x + d
        equation = sp.Eq(left_side, right_side)
        
        question = f"Solve for x: {sp.latex(equation)}"
        canonical_answer = str(solution)
        
        return {
            'question': question,
            'canonical_answer': canonical_answer,
            'params': {
                'a': a,
                'b': b,
                'c': c,
                'd': d,
                'type': 'linear_complex'
            }
        }

    # Quadratic removed per spec

    def check(self, user_input, canonical_answer, params):
        try:
            # Parse user input and canonical answer
            user_answer = sp.sympify(user_input)
            correct_answer = sp.sympify(canonical_answer)
            
            # Check if answers are equal
            is_correct = (user_answer == correct_answer)
            
            if not is_correct:
                # For quadratic equations, check if it's the other solution
                if params.get('type') == 'quadratic':
                    sol1 = params.get('sol1')
                    sol2 = params.get('sol2')
                    if user_answer in [sol1, sol2]:
                        is_correct = True
            
            return bool(is_correct), None
            
        except Exception as e:
            return False, f"Invalid input format. Please check your syntax. Error: {str(e)}"
