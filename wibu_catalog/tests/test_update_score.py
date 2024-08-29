from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseForbidden
from wibu_catalog.models import Content, Users, ScoreList
from wibu_catalog.views import score_to_str
from django.core.exceptions import ObjectDoesNotExist

class UpdateScoreTests(TestCase):

    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = Users.objects.create(
            uid=1,
            username="UserOne",
            email="userone@example.com",
            password="password123",
            registrationDate=timezone.now(),
        )

        # Create another test user
        self.user2 = Users.objects.create(
            uid=2,
            username="UserTwo",
            email="usertwo@example.com",
            password="password456",
            registrationDate=timezone.now(),
        )

        # Create test content
        self.content = Content.objects.create(
            cid=1,
            category="anime",
            name="One Punch Man",
            scoreAvg=9.0,
        )

    def test_update_score_logged_in(self):
        # Simulate user login by setting session
        session = self.client.session
        session['user_id'] = self.user.uid
        session.save()

        # Data to post
        data = {'score': '10'}

        # Send POST request to update score
        response = self.client.post(reverse('update_score', args=[self.content.cid]), data)

        # Check if score was created or updated
        score_instance = ScoreList.objects.get(uid=self.user, cid=self.content)
        self.assertEqual(score_instance.score, 10)

        # Ensure the user is redirected to the anime detail page
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_update_score_not_logged_in(self):
        # Send POST request without logging in
        data = {'score': '8'}
        response = self.client.post(reverse('update_score', args=[self.content.cid]), data)

        # Check if the response is forbidden
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code)

        # Ensure that no score was created
        with self.assertRaises(ScoreList.DoesNotExist):
            ScoreList.objects.get(uid=self.user, cid=self.content)

    def test_score_to_str(self):
        # Create a score for testing
        ScoreList.objects.create(
            uid=self.user,
            cid=self.content,
            score=9,
        )

        # Convert score to string
        score_sentence = score_to_str(self.content, self.user)

        # Check if the returned sentence matches the expected value
        self.assertEqual(score_sentence, "Excellent")

    def test_score_to_str_no_score(self):
        # Test when no score exists for the given content and user
        score_sentence = score_to_str(self.content, self.user)

        # Ensure that None is returned
        self.assertIsNone(score_sentence)
