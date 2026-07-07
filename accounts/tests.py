import bcrypt

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from portfolios.models import Profile


class OnboardingRedirectTests(TestCase):
    def test_login_redirects_to_dashboard_when_onboarding_completed(self):
        user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password=bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode(),
        )
        Profile.objects.create(user=user, full_name='Test User', onboarding_completed=True)

        response = self.client.post(reverse('accounts:login'), {
            'email': 'test@example.com',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:main_dashboard'))

    def test_login_redirects_to_onboarding_when_onboarding_incomplete(self):
        user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test2@example.com',
            password=bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode(),
        )
        Profile.objects.create(user=user, full_name='Test User')

        response = self.client.post(reverse('accounts:login'), {
            'email': 'test2@example.com',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('portfolios:onboarding_one'))

    def test_authenticated_user_with_completed_onboarding_cannot_access_onboarding(self):
        user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test3@example.com',
            password=bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode(),
        )
        Profile.objects.create(user=user, full_name='Test User', onboarding_completed=True)

        session = self.client.session
        session['user_id'] = user.id
        session.save()

        response = self.client.get(reverse('portfolios:onboarding_one'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:main_dashboard'))
