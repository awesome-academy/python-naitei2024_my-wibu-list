from django.test import TestCase, RequestFactory
from django.urls import reverse
from wibu_catalog.models import Content
from wibu_catalog.views import search_content

class SearchContentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.content1 = Content.objects.create(cid=1, name='Content 1')
        self.content2 = Content.objects.create(cid=2, name='Content 2')

    def test_search_content_with_query(self):
        request = self.factory.get(reverse('search_content'), {'q': 'Content 1'})
        request.session = {}  # Add session
        response = search_content(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content 1')
        self.assertNotContains(response, 'Content 2')

    def test_search_content_without_query(self):
        request = self.factory.get(reverse('search_content'))
        request.session = {}  # Add session
        response = search_content(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content 1')
        self.assertContains(response, 'Content 2')

    def test_search_content_with_no_matches(self):
        request = self.factory.get(reverse('search_content'), {'q': 'No matches'})
        request.session = {}  # Add session
        response = search_content(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Content 1')
        self.assertNotContains(response, 'Content 2')

    def test_search_content_with_partial_match(self):
        request = self.factory.get(reverse('search_content'), {'q': 'Content'})
        request.session = {}  # Add session
        response = search_content(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content 1')
        self.assertContains(response, 'Content 2')
