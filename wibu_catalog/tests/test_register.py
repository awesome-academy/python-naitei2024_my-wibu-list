from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import date

from wibu_catalog.models import Users
from wibu_catalog.forms import UserRegistrationForm


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.registration_url = reverse('register')

    def test_get_registration_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/registerform.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_post_valid_data_creates_user(self):
        response = self.client.post(self.registration_url, {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'password_confirmation': 'securepassword',
            'dateOfBirth': '1990-01-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Users.objects.filter(email='testuser@example.com').exists()
        )
        user = Users.objects.get(email='testuser@example.com')
        self.assertEqual(user.username, 'Test User')
        self.assertEqual(user.role, 'new_user')
        self.assertTrue(user.password.startswith('pbkdf2_'))
        self.assertEqual(user.dateOfBirth, date(1990, 1, 1))

    def test_post_invalid_email(self):
        Users.objects.create(
            uid=1,
            username='Existing User',
            role='new_user',
            email='testuser@example.com',
            password=make_password('password123'),
            dateOfBirth=date(1990, 1, 1),
            registrationDate=timezone.now()
        )
        response = self.client.post(self.registration_url, {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'password_confirmation': 'securepassword',
            'dateOfBirth': '1990-01-01',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email address already exists.')

    def test_post_password_mismatch(self):
        response = self.client.post(self.registration_url, {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'password_confirmation': 'differentpassword',
            'dateOfBirth': '1990-01-01',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match.')
