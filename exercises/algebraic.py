# exercises/algebraic.py
import random
import sympy as sp
from .base import BaseProblem

class AlgebraicIdentitiesProblem(BaseProblem):
    slug = 'algebraic'
    name = 'Algebraic Identities'

    def generate(self, difficulty):
        if difficulty == 1:
            # Easy: Simple expansion (a+b)^2, (a-b)^2
            return self._generate_simple_expansion()
        elif difficulty == 2:
            # Medium: More complex expansions (a+b)^3, (a-b)^3, (a+b)(a-b)
            return self._generate_medium_expansion()
        else:
            # Hard: Complex expressions with multiple terms
            return self._generate_complex_expansion()

    def _generate_simple_expansion(self):
        a, b = sp.symbols('a b')
        patterns = [
            (a + b)**2,
            (a - b)**2,
        ]
        
        pattern = random.choice(patterns)
        
        # Random coefficients
        coeff_a = random.randint(1, 5)
        coeff_b = random.randint(1, 5)
        
        # Substitute with coefficients
        pattern_with_coeffs = pattern.subs({a: coeff_a * a, b: coeff_b * b})
        expanded_with_coeffs = sp.expand(pattern_with_coeffs)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(expanded_with_coeffs, pattern_with_coeffs)
        
        return {
            'question': sp.latex(pattern_with_coeffs),
            'canonical_answer': str(expanded_with_coeffs),
            'multiple_choice': options,
            'params': {
                'pattern': str(pattern),
                'coeff_a': coeff_a,
                'coeff_b': coeff_b,
                'type': 'simple_expansion'
            }
        }

    def _generate_medium_expansion(self):
        a, b = sp.symbols('a b')
        patterns = [
            (a + b)**3,
            (a - b)**3,
            (a + b) * (a - b),
            (a + b) * (a**2 - a*b + b**2),
        ]
        
        pattern = random.choice(patterns)
        
        # Random coefficients
        coeff_a = random.randint(1, 3)
        coeff_b = random.randint(1, 3)
        
        pattern_with_coeffs = pattern.subs({a: coeff_a * a, b: coeff_b * b})
        expanded_with_coeffs = sp.expand(pattern_with_coeffs)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(expanded_with_coeffs, pattern_with_coeffs)
        
        return {
            'question': sp.latex(pattern_with_coeffs),
            'canonical_answer': str(expanded_with_coeffs),
            'multiple_choice': options,
            'params': {
                'pattern': str(pattern),
                'coeff_a': coeff_a,
                'coeff_b': coeff_b,
                'type': 'medium_expansion'
            }
        }

    def _generate_complex_expansion(self):
        a, b, c = sp.symbols('a b c')
        patterns = [
            (a + b + c)**2,
            (a + b) * (a + c) * (b + c),
            (a**2 + b**2) * (a + b),
            (a + b + c) * (a - b + c),
        ]
        
        pattern = random.choice(patterns)
        
        # Random coefficients
        coeff_a = random.randint(1, 2)
        coeff_b = random.randint(1, 2)
        coeff_c = random.randint(1, 2)
        
        pattern_with_coeffs = pattern.subs({
            a: coeff_a * a, 
            b: coeff_b * b, 
            c: coeff_c * c
        })
        expanded_with_coeffs = sp.expand(pattern_with_coeffs)
        
        # Generate multiple choice options
        options = self._generate_multiple_choice_options(expanded_with_coeffs, pattern_with_coeffs)
        
        return {
            'question': sp.latex(pattern_with_coeffs),
            'canonical_answer': str(expanded_with_coeffs),
            'multiple_choice': options,
            'params': {
                'pattern': str(pattern),
                'coeff_a': coeff_a,
                'coeff_b': coeff_b,
                'coeff_c': coeff_c,
                'type': 'complex_expansion'
            }
        }

    def _generate_multiple_choice_options(self, correct_answer, original_expression):
        """Generate multiple choice options for algebraic problems"""
        import random
        
        # Parse the correct answer
        correct_expr = sp.sympify(correct_answer)
        
        # Generate wrong options by modifying the correct answer
        options = []
        
        # Option 1: Correct answer
        options.append({
            'text': sp.latex(correct_expr),
            'value': str(correct_expr),
            'is_correct': True
        })
        
        # Option 2: Missing middle term (for (a+b)^2 = a^2 + 2ab + b^2, show a^2 + b^2)
        if '**2' in str(original_expression) or '^2' in str(original_expression):
            try:
                # Try to create a wrong answer by removing the middle term
                wrong_expr = correct_expr - 2 * sp.symbols('a') * sp.symbols('b')
                options.append({
                    'text': sp.latex(wrong_expr),
                    'value': str(wrong_expr),
                    'is_correct': False
                })
            except:
                pass
        
        # Option 3: Wrong sign on one term
        try:
            wrong_expr = correct_expr + 2 * sp.symbols('a') * sp.symbols('b')
            options.append({
                'text': sp.latex(wrong_expr),
                'value': str(wrong_expr),
                'is_correct': False
            })
        except:
            pass
        
        # Option 4: Completely different expression
        try:
            a, b = sp.symbols('a b')
            wrong_expr = a**2 + b**2 + a*b
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
                a, b = sp.symbols('a b')
                wrong_expr = a**2 + b**2 + random.randint(1, 5) * a * b
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
            
            # Simplify both expressions
            user_simplified = sp.simplify(user_expr)
            correct_simplified = sp.simplify(correct_expr)
            
            # Check if they are equivalent
            diff = sp.simplify(user_simplified - correct_simplified)
            is_correct = (diff == 0)
            
            if not is_correct:
                # Try alternative forms
                user_expanded = sp.expand(user_expr)
                correct_expanded = sp.expand(correct_expr)
                diff_expanded = sp.simplify(user_expanded - correct_expanded)
                is_correct = (diff_expanded == 0)
            
            return bool(is_correct), None
            
        except Exception as e:
            return False, f"Invalid input format. Please check your syntax. Error: {str(e)}"
