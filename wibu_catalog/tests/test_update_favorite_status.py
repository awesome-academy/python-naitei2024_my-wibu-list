from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseForbidden
from unittest.mock import patch
from wibu_catalog.models import Users, Content, FavoriteList
from wibu_catalog.views import update_favorite_status, _get_user_from_session

class UpdateFavoriteStatusViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_update_favorite_status_valid(self):
        user = Users.objects.create(uid=1, username='test_user')
        content = Content.objects.create(cid=1, name='Test Anime')

        request = self.factory.post(reverse('update_favorite_status', args=[content.cid]), {'status': '1'})
        request.session = {'user_id': user.uid}

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = update_favorite_status(request, content.cid)
        favorite = FavoriteList.objects.get(uid=user, cid=content)

        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertEqual(favorite.status, '1')  # Check if status updated correctly

    @patch('wibu_catalog.views._get_user_from_session', return_value=None)
    def test_update_favorite_status_not_logged_in(self, mock_get_user):
        content = Content.objects.create(cid=1, name='Test Anime')

        request = self.factory.post(reverse('update_favorite_status', args=[content.cid]), {'status': '1'})

        response = update_favorite_status(request, content.cid)

        self.assertIsInstance(response, HttpResponseForbidden)  # Check if forbidden when not logged in

    def test_update_favorite_status_invalid_status(self):
        user = Users.objects.create(uid=1, username='test_user')
        content = Content.objects.create(cid=1, name='Test Anime')

        request = self.factory.post(reverse('update_favorite_status', args=[content.cid]), {'status': '4'})
        request.session = {'user_id': user.uid}

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = update_favorite_status(request, content.cid)
        favorite_exists = FavoriteList.objects.filter(uid=user, cid=content).exists()

        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertFalse(favorite_exists)  # Check if favorite not created for invalid status
