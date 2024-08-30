from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone  # Add this import
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from ..views import AnimeDetailView

from wibu_catalog.models import (
    Content,
    Score,
    Users,
    FavoriteList,
    ScoreList,
    Comments,
    Product,
    Notifications,  # Add this import if it's used
)

class AnimeDetailViewTests(TestCase):
    def setUp(self):
        # Create Users
        self.user1 = Users.objects.create(
            uid=1,
            username="UserOne",
            email="userone@example.com",
            password="password123",
            registrationDate=timezone.now(),  # Fixed
        )
        self.user2 = Users.objects.create(
            uid=2,
            username="UserTwo",
            email="usertwo@example.com",
            password="password456",
            registrationDate=timezone.now(),  # Fixed
        )

        # Create Content
        self.content1 = Content.objects.create(
            cid=1,
            category="anime",
            name="One Punch Man",
            scoreAvg=9.0,
        )
        self.content2 = Content.objects.create(
            cid=2,
            category="manga",
            name="Attack on Titan",
            scoreAvg=8.5,
        )

        # Create Scores
        self.score1 = Score.objects.create(
            cid=self.content1,
            score10=5,
            score9=10,
        )
        self.score2 = Score.objects.create(
            cid=self.content2,
            score10=3,
            score9=7,
        )

        # Create FavoriteList
        self.favorite1 = FavoriteList.objects.create(
            uid=self.user1,
            cid=self.content1,
            status="1",
            progress=12,
        )
        self.favorite2 = FavoriteList.objects.create(
            uid=self.user2,
            cid=self.content2,
            status="2",
            progress=20,
        )

        # Create ScoreList
        self.score_list1 = ScoreList.objects.create(
            uid=self.user1,
            cid=self.content1,
            score=10,
        )
        self.score_list2 = ScoreList.objects.create(
            uid=self.user2,
            cid=self.content2,
            score=8,
        )

        # Create Comments
        self.comment1 = Comments.objects.create(
            uid=self.user1,
            cid=self.content1,
            content="Amazing anime!",
            dateOfCmt=timezone.now(),  # Fixed
            likes=10,
        )
        self.comment2 = Comments.objects.create(
            uid=self.user2,
            cid=self.content2,
            content="Exciting manga!",
            dateOfCmt=timezone.now(),  # Fixed
            likes=5,
        )

        # Create Notifications
        self.notification1 = Notifications.objects.create(
            uid=self.user1,
            message="You have a new message.",
            date=timezone.now(),  # Fixed
            nType="message",
            isRead=False,
        )
        self.notification2 = Notifications.objects.create(
            uid=self.user2,
            message="Your order has been shipped.",
            date=timezone.now(),  # Fixed
            nType="order",
            isRead=True,
        )

        # Create Products
        self.product1 = Product.objects.create(
            pid=1,
            name="One Punch Man Figurine",
            price=25.99,
            description="A high-quality figurine.",
            cid=self.content1,
        )
        self.product2 = Product.objects.create(
            pid=2,
            name="Attack on Titan Manga Volume 1",
            price=10.99,
            description="The first volume of Attack on Titan manga.",
            cid=self.content2,
        )

        self.factory = RequestFactory()

    def test_anime_detail_view_with_logged_in_user(self):
        # Simulate a session where the user is logged in
        session = self.client.session
        session['user_id'] = self.user1.uid
        session.save()

        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/anime_detail.html')
        self.assertContains(response, self.content1.name)
        self.assertContains(response, self.comment1.content)  # Fixed to comment1
        self.assertContains(response, self.favorite1.cid.name)  # Fixed to favorite1
        self.assertContains(response, '10')  # Fixed to match score_list1
        self.assertIsNotNone(response.context['userr'])  # Ensure user is in context

    def test_anime_detail_view_without_logged_in_user(self):
        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/anime_detail.html')
        self.assertContains(response, self.content1.name)
        self.assertContains(response, self.comment1.content)  # Fixed to comment1
        self.assertNotContains(response, '10')  # No score should be shown for anonymous user
        self.assertIsNone(response.context['userr'])  # No user in context

    def test_anime_detail_view_context_data(self):
        # Test if context data is correctly populated
        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}))

        context = response.context
        self.assertEqual(context["anime_detail"], self.content1)
        self.assertEqual(list(context["comments"]), list(Comments.objects.filter(cid=self.content1.cid)))
        self.assertEqual(context["favorite"], self.favorite1)  # Fixed to favorite1
        self.assertIsNotNone(context["what_to_watch"])
        self.assertEqual(list(context["products"]), list(Product.objects.filter(cid=self.content1.cid)))
        self.assertIn("score_", context)
        self.assertNotIn("score_str", context)  # Since no user is logged in

    def test_anime_detail_view_random_button_functionality(self):
        # Test if the random button returns a valid Content instance
        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}))
        self.assertIsNotNone(response.context['what_to_watch'])
        self.assertIsInstance(response.context['what_to_watch'], Content)

    def test_anime_detail_view_pagination(self):
        # Setup more comments to test pagination
        for i in range(1, 15):  # Assuming COMMENTS_PER_PAGE_DETAIL is less than 14
            Comments.objects.create(
                cid=self.content1,
                uid=self.user1,
                content=f"Comment {i}",
                dateOfCmt=timezone.now()  # Fixed
            )

        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}), {'comments_page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['comments'].number, 2)  # Check if second page is loaded

    def test_anime_detail_view_no_products(self):
        # Test when there are no products related to the content
        Product.objects.all().delete()  # Delete all products
        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}))
        self.assertIsNone(response.context['products'])  # Ensure products context is None

    def test_anime_detail_view_user_favorite_status(self):
        # Test favorite status when user is logged in
        session = self.client.session
        session['user_id'] = self.user1.uid
        session.save()

        response = self.client.get(reverse('anime_detail', kwargs={'pk': self.content1.cid}))
        self.assertEqual(response.context['favorite'], self.favorite1)  # Fixed to favorite1
