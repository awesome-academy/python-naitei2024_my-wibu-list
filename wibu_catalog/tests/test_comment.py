from django.test import TestCase, Client
from django.urls import reverse
from wibu_catalog.models import Content, Users, Comments
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class CommentFunctionTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create test users
        self.user1 = Users.objects.create(
            uid=1,
            username="UserOne",
            email="userone@example.com",
            password="password123",
            registrationDate=timezone.now(),
        )
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

        # Create a comment by user1
        self.comment = Comments.objects.create(
            id=1,
            uid=self.user1,
            cid=self.content,
            content="Great anime!",
            dateOfCmt=timezone.now().date(),
        )

    def test_post_comment(self):
        # Simulate user1 login
        session = self.client.session
        session['user_id'] = self.user1.uid
        session.save()

        data = {'content': 'Amazing series!'}
        response = self.client.post(reverse('post_comment', args=[self.content.cid]), data)

        # Check if the comment was created
        self.assertTrue(Comments.objects.filter(content='Amazing series!').exists())

        # Check if the user is redirected to the anime detail page
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_edit_comment(self):
        # Simulate user1 login
        session = self.client.session
        session['user_id'] = self.user1.uid
        session.save()

        data = {'content': 'Edited comment'}
        response = self.client.post(reverse('edit_comment', args=[self.comment.id]), data)

        # Refresh the comment from the database
        self.comment.refresh_from_db()

        # Check if the comment was updated
        self.assertEqual(self.comment.content, 'Edited comment')

        # Check if the user is redirected to the anime detail page
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_delete_comment(self):
        # Simulate user1 login
        session = self.client.session
        session['user_id'] = self.user1.uid
        session.save()

        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))

        # Check if the comment was deleted
        with self.assertRaises(Comments.DoesNotExist):
            Comments.objects.get(id=self.comment.id)

        # Check if the user is redirected to the anime detail page
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_toggle_like_comment(self):
        # Simulate user2 login
        session = self.client.session
        session['user_id'] = self.user2.uid
        session.save()

        response = self.client.post(reverse('toggle_like_comment', args=[self.comment.id]))

        # Refresh the comment from the database
        self.comment.refresh_from_db()

        # Check if the like was added
        self.assertTrue(self.user2 in self.comment.userLikes.all())
        self.assertEqual(self.comment.likes, 1)

        # Check if the user is redirected to the anime detail page
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

        # Send the request again to remove the like
        response = self.client.post(reverse('toggle_like_comment', args=[self.comment.id]))
        self.comment.refresh_from_db()

        # Check if the like was removed
        self.assertFalse(self.user2 in self.comment.userLikes.all())
        self.assertEqual(self.comment.likes, 0)

    def test_reply_comment(self):
        # Simulate user2 login
        session = self.client.session
        session['user_id'] = self.user2.uid
        session.save()

        data = {'content': 'This is a reply.'}
        response = self.client.post(reverse('reply_comment', args=[self.comment.id]), data)

        # Check if the reply was created
        reply = Comments.objects.get(content='This is a reply.')
        self.assertEqual(reply.parent, self.comment)

        # Check if the user is redirected to the anime detail page
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_post_comment_not_logged_in(self):
        # Try to post a comment without being logged in
        data = {'content': 'Amazing series!'}
        response = self.client.post(reverse('post_comment', args=[self.content.cid]), data)

        # Check that no comment was created
        self.assertFalse(Comments.objects.filter(content='Amazing series!').exists())

        # Check that the user is redirected (since they're not logged in)
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_edit_comment_not_logged_in(self):
        # Try to edit a comment without being logged in
        data = {'content': 'Edited comment'}
        response = self.client.post(reverse('edit_comment', args=[self.comment.id]), data)

        # Refresh the comment from the database
        self.comment.refresh_from_db()

        # Check that the comment was not edited
        self.assertNotEqual(self.comment.content, 'Edited comment')

        # Check that the user is redirected (since they're not logged in)
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))

    def test_delete_comment_not_logged_in(self):
        # Try to delete a comment without being logged in
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))

        # Check that the comment was not deleted
        self.assertTrue(Comments.objects.filter(id=self.comment.id).exists())

        # Check that the user is redirected (since they're not logged in)
        self.assertRedirects(response, reverse('anime_detail', args=[self.content.cid]))
