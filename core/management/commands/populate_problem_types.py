from django.core.management.base import BaseCommand
from core.models import ProblemType

class Command(BaseCommand):
    help = 'Populate the database with problem types'

    def handle(self, *args, **options):
        problem_types = [
            {
                'slug': 'arithmetic',
                'name': 'Mental Arithmetic',
                'description': 'Practice basic arithmetic operations: addition, subtraction, multiplication, and division',
                'impl_path': 'exercises.arithmetic.ArithmeticProblem'
            },
            {
                'slug': 'algebraic',
                'name': 'Algebraic Identities',
                'description': 'Expand and factor algebraic expressions using identities',
                'impl_path': 'exercises.algebraic.AlgebraicIdentitiesProblem'
            },
            {
                'slug': 'exponential',
                'name': 'Exponential & Logarithmic',
                'description': 'Work with exponential expressions, logarithms, and their properties',
                'impl_path': 'exercises.exponential.ExponentialLogarithmProblem'
            },
            {
                'slug': 'equations',
                'name': 'Linear & Quadratic Equations',
                'description': 'Solve linear and quadratic equations',
                'impl_path': 'exercises.equations.EquationsProblem'
            },
            {
                'slug': 'calculus',
                'name': 'Derivatives & Integrals',
                'description': 'Find derivatives and integrals of various functions',
                'impl_path': 'exercises.calculus.CalculusProblem'
            },
        ]

        for pt_data in problem_types:
            pt, created = ProblemType.objects.get_or_create(
                slug=pt_data['slug'],
                defaults={
                    'name': pt_data['name'],
                    'description': pt_data['description'],
                    'impl_path': pt_data['impl_path']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created problem type: {pt.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Problem type already exists: {pt.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated problem types')
        )
