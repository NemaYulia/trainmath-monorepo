# exercises/exponential.py
import random
import sympy as sp
from .base import BaseProblem

class ExponentialLogarithmProblem(BaseProblem):
    slug = 'exponential'
    name = 'Exponential & Logarithmic Expressions'

    def generate(self, difficulty):
        if difficulty == 1:
            # Easy: Simple exponential rules
            return self._generate_simple_exponential()
        elif difficulty == 2:
            # Medium: Logarithmic properties
            return self._generate_logarithmic()
        else:
            # Hard: Complex expressions and simple equations
            return self._generate_complex_expressions()

    def _generate_simple_exponential(self):
        x = sp.Symbol('x')
        patterns = [
            # a^x * a^y = a^(x+y)
            lambda: (2**x * 2**random.randint(1, 5), 2**(x + random.randint(1, 5))),
            # a^x / a^y = a^(x-y)
            lambda: (3**x / 3**random.randint(1, 3), 3**(x - random.randint(1, 3))),
            # (a^x)^y = a^(x*y)
            lambda: ((2**x)**random.randint(2, 4), 2**(x * random.randint(2, 4))),
        ]
        
        pattern_func = random.choice(patterns)
        left_expr, right_expr = pattern_func()
        
        # Always show the left side and ask for simplification
        question_expr = left_expr
        canonical_answer = str(right_expr)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(right_expr, left_expr)
        
        return {
            'question': sp.latex(question_expr),
            'canonical_answer': canonical_answer,
            'multiple_choice': options,
            'params': {
                'left_expr': str(left_expr),
                'right_expr': str(right_expr),
                'type': 'simple_exponential'
            }
        }

    def _generate_logarithmic(self):
        x = sp.Symbol('x')
        base = random.choice([2, 3, 5, 10])
        
        patterns = [
            # log(a) + log(b) = log(a*b)
            lambda: (sp.log(base**random.randint(1, 3), base) + sp.log(base**random.randint(1, 3), base), 
                    sp.log(base**(random.randint(1, 3) + random.randint(1, 3)), base)),
            # log(a) - log(b) = log(a/b)
            lambda: (sp.log(base**random.randint(2, 4), base) - sp.log(base**random.randint(1, 2), base),
                    sp.log(base**(random.randint(2, 4) - random.randint(1, 2)), base)),
            # n*log(a) = log(a^n)
            lambda: (random.randint(2, 4) * sp.log(base**random.randint(1, 3), base),
                    sp.log((base**random.randint(1, 3))**random.randint(2, 4), base)),
        ]
        
        pattern_func = random.choice(patterns)
        left_expr, right_expr = pattern_func()
        
        # Always show the left side and ask for simplification
        question_expr = left_expr
        canonical_answer = str(right_expr)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(right_expr, left_expr)
        
        return {
            'question': sp.latex(question_expr),
            'canonical_answer': canonical_answer,
            'multiple_choice': options,
            'params': {
                'left_expr': str(left_expr),
                'right_expr': str(right_expr),
                'base': base,
                'type': 'logarithmic'
            }
        }

    def _generate_complex_expressions(self):
        x = sp.Symbol('x')
        
        # Generate simple exponential equations
        if random.choice([True, False]):
            # Exponential equation: a^x = b
            base = random.choice([2, 3, 5])
            exponent = random.randint(1, 5)
            result = base**exponent
            
            question = f"Solve for x: {base}^x = {result}"
            canonical_answer = str(exponent)
            
            return {
                'question': question,
                'canonical_answer': canonical_answer,
                'params': {
                    'base': base,
                    'result': result,
                    'type': 'exponential_equation'
                }
            }
        else:
            # Logarithmic equation: log_a(x) = b
            base = random.choice([2, 3, 5])
            result = random.randint(1, 4)
            x_value = base**result
            
            question = f"Solve for x: log_{base}(x) = {result}"
            canonical_answer = str(x_value)
            
            return {
                'question': question,
                'canonical_answer': canonical_answer,
                'params': {
                    'base': base,
                    'result': result,
                    'type': 'logarithmic_equation'
                }
            }

    def _generate_multiple_choice_options(self, correct_answer, original_expression):
        """Generate multiple choice options for exponential/logarithmic problems"""
        import random
        
        # Parse the correct answer
        correct_expr = sp.sympify(correct_answer)
        
        options = []
        
        # Option 1: Correct answer
        options.append({
            'text': sp.latex(correct_expr),
            'value': str(correct_expr),
            'is_correct': True
        })
        
        # Generate wrong options
        try:
            # Option 2: Wrong exponent (for exponential problems)
            if '**' in str(correct_answer) or '^' in str(correct_answer):
                x = sp.Symbol('x')
                wrong_expr = correct_expr + x  # Add extra term
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
        except:
            pass
        
        try:
            # Option 3: Different base
            if 'log' in str(correct_answer):
                # Try to create a wrong log expression
                wrong_expr = correct_expr + 1
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
        except:
            pass
        
        try:
            # Option 4: Simple wrong expression
            x = sp.Symbol('x')
            wrong_expr = x + 1
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
                x = sp.Symbol('x')
                wrong_expr = x + random.randint(1, 5)
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
            
            # For equations, check if the values are equal
            if params.get('type') in ['exponential_equation', 'logarithmic_equation']:
                is_correct = (user_expr == correct_expr)
            else:
                # For expressions, check if they are equivalent
                diff = sp.simplify(user_expr - correct_expr)
                is_correct = (diff == 0)
            
            return bool(is_correct), None
            
        except Exception as e:
            return False, f"Invalid input format. Please check your syntax. Error: {str(e)}"
