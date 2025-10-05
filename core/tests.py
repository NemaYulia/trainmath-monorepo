from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import ProblemType, ProblemInstance, Attempt, ShareResult
from exercises.arithmetic import ArithmeticProblem
import json

User = get_user_model()

class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a problem type
        self.problem_type = ProblemType.objects.create(
            slug='arithmetic',
            name='Mental Arithmetic',
            description='Basic arithmetic operations',
            impl_path='exercises.arithmetic.ArithmeticProblem'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to TrainMath')

    def test_start_session_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('start_session', args=['arithmetic']), {'difficulty': 1})
        self.assertEqual(response.status_code, 302)  # Redirect to question

    def test_start_session_guest(self):
        response = self.client.get(reverse('start_session', args=['arithmetic']), {'difficulty': 1})
        self.assertEqual(response.status_code, 302)  # Redirect to question

    def test_show_question(self):
        # Create a problem instance
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )
        
        response = self.client.get(reverse('show_question', args=[problem.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2 + 3')

    def test_submit_answer_correct(self):
        # Create a problem instance
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )
        
        # Set session data
        session = self.client.session
        session['current_problem_id'] = problem.id
        session['start_time'] = 1000
        session.save()
        
        response = self.client.post(reverse('submit_answer', args=[problem.id]), {
            'answer': '5'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to result
        
        # Check that attempt was created
        attempt = Attempt.objects.get(problem=problem)
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.user_answer, '5')

    def test_submit_answer_incorrect(self):
        # Create a problem instance
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )
        
        # Set session data
        session = self.client.session
        session['current_problem_id'] = problem.id
        session['start_time'] = 1000
        session.save()
        
        response = self.client.post(reverse('submit_answer', args=[problem.id]), {
            'answer': '6'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to result
        
        # Check that attempt was created
        attempt = Attempt.objects.get(problem=problem)
        self.assertFalse(attempt.is_correct)
        self.assertEqual(attempt.user_answer, '6')

    def test_result_view(self):
        # Create a problem instance and attempt
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )
        
        attempt = Attempt.objects.create(
            user=self.user,
            problem=problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1000
        )
        
        response = self.client.get(reverse('result', args=[attempt.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Correct!')

    def test_share_attempt(self):
        # Create a problem instance and attempt
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )
        
        attempt = Attempt.objects.create(
            user=self.user,
            problem=problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1000
        )
        
        response = self.client.get(reverse('share_attempt', args=[attempt.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to share public
        
        # Check that ShareResult was created
        share_result = ShareResult.objects.get(attempt=attempt)
        self.assertIsNotNone(share_result.uuid)

    def test_share_public(self):
        # Create a problem instance and attempt
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )
        
        attempt = Attempt.objects.create(
            user=self.user,
            problem=problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1000
        )
        
        share_result = ShareResult.objects.create(attempt=attempt)
        
        response = self.client.get(reverse('share_public', args=[share_result.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shared Result')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Trainmath')

class ProblemTypeModelTest(TestCase):
    def test_problem_type_creation(self):
        problem_type = ProblemType.objects.create(
            slug='test',
            name='Test Problem',
            description='A test problem type',
            impl_path='test.module.TestClass'
        )
        self.assertEqual(str(problem_type), 'Test Problem')
        self.assertEqual(problem_type.slug, 'test')

class ProblemInstanceModelTest(TestCase):
    def setUp(self):
        self.problem_type = ProblemType.objects.create(
            slug='test',
            name='Test Problem',
            description='A test problem type',
            impl_path='test.module.TestClass'
        )

    def test_problem_instance_creation(self):
        problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'test': 'data'},
            question_text='What is 2+2?',
            canonical_answer='4'
        )
        self.assertEqual(problem.difficulty, 1)
        self.assertEqual(problem.question_text, 'What is 2+2?')
        self.assertEqual(problem.canonical_answer, '4')

class AttemptModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.problem_type = ProblemType.objects.create(
            slug='test',
            name='Test Problem',
            description='A test problem type',
            impl_path='test.module.TestClass'
        )
        self.problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'test': 'data'},
            question_text='What is 2+2?',
            canonical_answer='4'
        )

    def test_attempt_creation(self):
        attempt = Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='4',
            is_correct=True,
            time_taken_ms=1000
        )
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.problem, self.problem)
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.time_taken_ms, 1000)

    def test_attempt_guest_session(self):
        attempt = Attempt.objects.create(
            user=None,
            session_id='test_session_123',
            problem=self.problem,
            user_answer='4',
            is_correct=True,
            time_taken_ms=1000
        )
        self.assertIsNone(attempt.user)
        self.assertEqual(attempt.session_id, 'test_session_123')

class ShareResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.problem_type = ProblemType.objects.create(
            slug='test',
            name='Test Problem',
            description='A test problem type',
            impl_path='test.module.TestClass'
        )
        self.problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'test': 'data'},
            question_text='What is 2+2?',
            canonical_answer='4'
        )
        self.attempt = Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='4',
            is_correct=True,
            time_taken_ms=1000
        )

    def test_share_result_creation(self):
        share_result = ShareResult.objects.create(attempt=self.attempt)
        self.assertEqual(share_result.attempt, self.attempt)
        self.assertTrue(share_result.public)
        self.assertIsNotNone(share_result.uuid)