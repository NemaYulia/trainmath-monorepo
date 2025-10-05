# exercises/calculus.py
import random
import sympy as sp
from .base import BaseProblem

class DerivativesProblem(BaseProblem):
    slug = 'derivatives'
    name = 'Derivatives'

    def generate(self, difficulty):
        if difficulty == 1:
            # Easy: Basic derivatives
            return self._generate_basic_derivative()
        elif difficulty == 2:
            # Medium: More complex derivatives
            return self._generate_complex_derivative()
        else:
            # Hard: More complex derivatives
            return self._generate_complex_derivative()

    def _generate_basic_derivative(self):
        x = sp.Symbol('x')
        
        # Basic functions
        functions = [
            # Power functions
            lambda: x**random.randint(2, 5),
            # Polynomials
            lambda: x**random.randint(2, 4) + random.randint(1, 5) * x + random.randint(1, 10),
            # Simple trigonometric
            lambda: sp.sin(x) if random.choice([True, False]) else sp.cos(x),
        ]
        
        func_generator = random.choice(functions)
        func = func_generator()
        
        # Calculate derivative
        derivative = sp.diff(func, x)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(derivative, func)
        
        return {
            'question': sp.latex(func),
            'canonical_answer': str(derivative),
            'multiple_choice': options,
            'params': {
                'function': str(func),
                'type': 'basic_derivative'
            }
        }

    def _generate_complex_derivative(self):
        x = sp.Symbol('x')
        
        # More complex functions
        functions = [
            # Product rule: f(x) * g(x)
            lambda: x**random.randint(2, 3) * sp.sin(x),
            lambda: x**random.randint(2, 3) * sp.cos(x),
            # Chain rule: f(g(x))
            lambda: sp.sin(x**random.randint(2, 3)),
            lambda: sp.cos(x**random.randint(2, 3)),
            # Quotient rule: f(x) / g(x)
            lambda: x**random.randint(2, 4) / (x + random.randint(1, 3)),
        ]
        
        func_generator = random.choice(functions)
        func = func_generator()
        
        # Calculate derivative
        derivative = sp.diff(func, x)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(derivative, func)
        
        return {
            'question': sp.latex(func),
            'canonical_answer': str(derivative),
            'multiple_choice': options,
            'params': {
                'function': str(func),
                'type': 'complex_derivative'
            }
        }

    def _generate_multiple_choice_options(self, correct_answer, original_function):
        """Generate multiple choice options for calculus problems"""
        import random
        
        # Parse the correct answer
        correct_expr = sp.sympify(correct_answer)
        x = sp.Symbol('x')
        
        options = []
        
        # Option 1: Correct answer
        options.append({
            'text': sp.latex(correct_expr),
            'value': str(correct_expr),
            'is_correct': True
        })
        
        # Generate wrong options
        try:
            # Option 2: Wrong power rule (for derivatives)
            if '**' in str(correct_answer):
                wrong_expr = correct_expr + x  # Add extra term
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
        except:
            pass
        
        try:
            # Option 3: Missing constant of integration (for integrals)
            if 'C' in str(correct_answer) or 'constant' in str(correct_answer).lower():
                # Remove the constant
                wrong_expr = correct_expr - sp.Symbol('C')
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
        except:
            pass
        
        try:
            # Option 4: Wrong trigonometric derivative
            if 'sin' in str(correct_answer) or 'cos' in str(correct_answer):
                # Swap sin and cos
                wrong_expr = correct_expr.subs(sp.sin(x), sp.cos(x)).subs(sp.cos(x), sp.sin(x))
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
        except:
            pass
        
        # If we don't have enough options, generate some simple wrong ones
        while len(options) < 4:
            try:
                wrong_expr = correct_expr + random.randint(1, 5) * x
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
            except:
                break
        
        # Shuffle options and ensure we have exactly 4
        random.shuffle(options)
        return options[:4]

    def check(self, user_input, canonical_answer, params):
        try:
            # Parse user input and canonical answer
            user_expr = sp.sympify(user_input)
            correct_expr = sp.sympify(canonical_answer)
            
            # For derivatives, check if they are equivalent
            diff = sp.simplify(user_expr - correct_expr)
            is_correct = (diff == 0)
            
            return bool(is_correct), None
            
        except Exception as e:
            return False, f"Invalid input format. Please check your syntax. Error: {str(e)}"


class IntegralsProblem(BaseProblem):
    slug = 'integrals'
    name = 'Integrals'

    def generate(self, difficulty):
        x = sp.Symbol('x')
        # Use increasingly complex functions with difficulty
        if difficulty == 1:
            functions = [
                lambda: x**random.randint(1, 4),
                lambda: x + random.randint(1, 5),
            ]
        elif difficulty == 2:
            functions = [
                lambda: x**random.randint(2, 4) + random.randint(1, 3) * x,
                lambda: sp.sin(x),
                lambda: sp.cos(x),
            ]
        else:
            functions = [
                lambda: x**random.randint(2, 5) + random.randint(1, 5) * x + random.randint(1, 5),
                lambda: sp.exp(x),
                lambda: sp.sin(x) + sp.cos(x),
            ]

        func = random.choice(functions)()
        integral = sp.integrate(func, x)
        options = self._generate_multiple_choice_options(integral, func)
        return {
            'question': sp.latex(func),
            'canonical_answer': str(integral),
            'multiple_choice': options,
            'params': {
                'function': str(func),
                'type': 'integral'
            }
        }

    def _generate_multiple_choice_options(self, correct_answer, original_function):
        # reuse same logic as above class
        correct_expr = sp.sympify(correct_answer)
        x = sp.Symbol('x')
        options = [{
            'text': sp.latex(correct_expr),
            'value': str(correct_expr),
            'is_correct': True
        }]
        # Add plausible wrong ones
        options.append({
            'text': sp.latex(correct_expr + x),
            'value': str(correct_expr + x),
            'is_correct': False
        })
        options.append({
            'text': sp.latex(correct_expr - x),
            'value': str(correct_expr - x),
            'is_correct': False
        })
        options.append({
            'text': sp.latex(correct_expr + 1),
            'value': str(correct_expr + 1),
            'is_correct': False
        })
        random.shuffle(options)
        return options[:4]

    def check(self, user_input, canonical_answer, params):
        try:
            user_expr = sp.sympify(user_input)
            correct_expr = sp.sympify(canonical_answer)
            # Integrals equal up to constant
            diff = sp.simplify(user_expr - correct_expr)
            return bool(diff.is_constant() or diff == 0), None
        except Exception as e:
            return False, f"Invalid input format. Please check your syntax. Error: {str(e)}"
