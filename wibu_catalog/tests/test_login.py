from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from wibu_catalog.models import Users
from wibu_catalog.forms import LoginForm


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.user = Users.objects.create(
            uid=1,
            email="testuser@example.com",
            password=make_password("correct_password"),
            username="testuser",
            dateOfBirth="1990-01-01",
            role="new_user"
        )

    def test_login_with_nonexistent_email(self):
        response = self.client.post(self.login_url, {
            "email": "nonexistent@example.com",
            "password": "any_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "email", "Email does not exist."
        )

    def test_login_with_incorrect_password(self):
        response = self.client.post(self.login_url, {
            "email": self.user.email,
            "password": "incorrect_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "password", "Incorrect password."
        )

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            "email": self.user.email,
            "password": "correct_password"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("user_id"), self.user.uid)

    def test_get_login_form(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], LoginForm)
