from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import ProblemType, ProblemInstance, Attempt
from django.db.models import Avg, Count, Q

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test data
        self.problem_type = ProblemType.objects.create(
            slug='arithmetic',
            name='Mental Arithmetic',
            description='Basic arithmetic operations',
            impl_path='exercises.arithmetic.ArithmeticProblem'
        )
        
        self.problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )

    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_view_post(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # Check that user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_view_post(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_view_with_attempts(self):
        # Create some attempts for the user
        Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1000
        )
        Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='6',
            is_correct=False,
            time_taken_ms=2000
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total Attempts')
        self.assertContains(response, 'Accuracy')

class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_admin_user)

    def test_superuser_creation(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')

class UserStatisticsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.problem_type = ProblemType.objects.create(
            slug='arithmetic',
            name='Mental Arithmetic',
            description='Basic arithmetic operations',
            impl_path='exercises.arithmetic.ArithmeticProblem'
        )
        
        self.problem = ProblemInstance.objects.create(
            problem_type=self.problem_type,
            difficulty=1,
            params={'operands': [2, 3], 'operators': ['+']},
            question_text='2 + 3',
            canonical_answer='5'
        )

    def test_user_statistics_calculation(self):
        # Create attempts with different results
        Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1000
        )
        Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='6',
            is_correct=False,
            time_taken_ms=2000
        )
        Attempt.objects.create(
            user=self.user,
            problem=self.problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1500
        )
        
        # Calculate statistics
        attempts = Attempt.objects.filter(user=self.user)
        total = attempts.count()
        correct = attempts.filter(is_correct=True).count()
        accuracy = (correct / total * 100) if total > 0 else 0
        avg_time = attempts.aggregate(Avg("time_taken_ms"))["time_taken_ms__avg"]
        
        self.assertEqual(total, 3)
        self.assertEqual(correct, 2)
        self.assertAlmostEqual(accuracy, 66.67, places=1)
        self.assertEqual(avg_time, 1500.0)

    def test_guest_user_statistics(self):
        # Create attempts for guest user (no user, but with session_id)
        Attempt.objects.create(
            user=None,
            session_id='guest_session_123',
            problem=self.problem,
            user_answer='5',
            is_correct=True,
            time_taken_ms=1000
        )
        
        # Guest attempts should not be counted in user statistics
        user_attempts = Attempt.objects.filter(user=self.user)
        self.assertEqual(user_attempts.count(), 0)
        
        # But should be counted in guest statistics
        guest_attempts = Attempt.objects.filter(session_id='guest_session_123')
        self.assertEqual(guest_attempts.count(), 1)