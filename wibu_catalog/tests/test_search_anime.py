from django.test import TestCase
from django.urls import reverse
from wibu_catalog.models import Content, Users


class SearchContentViewTest(TestCase):
    def setUp(self):

        self.content1 = Content.objects.create(
            cid=1,
            name="Naruto",
            genres="Action"

        )
        self.content2 = Content.objects.create(
            cid=2,
            name="One Piece",
            genres="Adventure"
        )

        self.content3 = Content.objects.create(
            cid=3,
            name="Bleach",
            genres="Action"
        )

        # URL cho trang tìm kiếm
        self.url = reverse("search_content")

    def test_search_content_with_query(self):
        response = self.client.get(self.url, {'q': 'Naruto'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "html/search_content_results.html")

        search_results = response.context["search_results"]
        self.assertIn(self.content1, search_results)
        self.assertNotIn(self.content2, search_results)
        self.assertNotIn(self.content3, search_results)

    def test_search_content_without_query(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "html/search_content_results.html")

        search_results = response.context["search_results"]
        self.assertIn(self.content1, search_results)
        self.assertIn(self.content2, search_results)
        self.assertIn(self.content3, search_results)
