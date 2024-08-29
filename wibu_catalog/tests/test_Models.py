from django.test import TestCase
from wibu_catalog.models import (
    Content,
    Score,
    Users,
    FavoriteList,
    ScoreList,
    Comments,
    Notifications,
    Product,
    Order,
    OrderItems,
    Feedback
)
from django.utils import timezone

class WibuCatalogTests(TestCase):

    def setUp(self):
        # Create Users
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
            dateOfCmt=timezone.now(),
            likes=10,
        )
        self.comment2 = Comments.objects.create(
            uid=self.user2,
            cid=self.content2,
            content="Exciting manga!",
            dateOfCmt=timezone.now(),
            likes=5,
        )

        # Create Notifications
        self.notification1 = Notifications.objects.create(
            uid=self.user1,
            message="You have a new message.",
            date=timezone.now(),
            nType="message",
            isRead=False,
        )
        self.notification2 = Notifications.objects.create(
            uid=self.user2,
            message="Your order has been shipped.",
            date=timezone.now(),
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

        # Create Orders
        self.order1 = Order.objects.create(
            oid=1,
            orderDate=timezone.now(),
            status="Shipped",
            uid=self.user1,
        )
        self.order2 = Order.objects.create(
            oid=2,
            orderDate=timezone.now(),
            status="Processing",
            uid=self.user2,
        )

        # Create OrderItems
        self.order_item1 = OrderItems.objects.create(
            oid=self.order1,
            pid=self.product1,
            quantity=1,
            buyPrice=25.99,
        )
        self.order_item2 = OrderItems.objects.create(
            oid=self.order2,
            pid=self.product2,
            quantity=2,
            buyPrice=21.98,
        )

        # Create Feedback
        self.feedback1 = Feedback.objects.create(
            uid=self.user1,
            pid=self.product1,
            cmt="Excellent product!",
            rate=5,
        )
        self.feedback2 = Feedback.objects.create(
            uid=self.user2,
            pid=self.product2,
            cmt="Very good manga.",
            rate=4,
        )

    def test_content_str(self):
        self.assertEqual(str(self.content1), "One Punch Man")
        self.assertEqual(str(self.content2), "Attack on Titan")

    def test_user_str(self):
        self.assertEqual(str(self.user1), "UserOne")
        self.assertEqual(str(self.user2), "UserTwo")

    def test_score_str(self):
        self.assertEqual(str(self.score1), f"Scores for Content CID: {self.content1.cid}")
        self.assertEqual(str(self.score2), f"Scores for Content CID: {self.content2.cid}")

    def test_favoritelist_str(self):
        self.assertEqual(str(self.favorite1), "1")
        self.assertEqual(str(self.favorite2), "2")

    def test_scorelist_str(self):
        self.assertEqual(str(self.score_list1), "10")
        self.assertEqual(str(self.score_list2), "8")

    def test_comments_str(self):
        self.assertEqual(str(self.comment1), f"{str(self.user1)},{str(self.content1)},{self.comment1.content}")
        self.assertEqual(str(self.comment2), f"{str(self.user2)},{str(self.content2)},{self.comment2.content}")

    def test_notifications_str(self):
        self.assertEqual(str(self.notification1), str(self.notification1.notificationId))
        self.assertEqual(str(self.notification2), str(self.notification2.notificationId))

    def test_product_str(self):
        self.assertEqual(str(self.product1), str(self.product1.pid))
        self.assertEqual(str(self.product2), str(self.product2.pid))

    def test_order_str(self):
        self.assertEqual(str(self.order1), f"Order {str(self.order1.oid)} by User {str(self.order1.uid)}")
        self.assertEqual(str(self.order2), f"Order {str(self.order2.oid)} by User {str(self.order2.uid)}")

    def test_orderitems_str(self):
        self.assertEqual(str(self.order_item1), f"{str(self.order_item1.oid)} - {str(self.order_item1.pid)}")
        self.assertEqual(str(self.order_item2), f"{str(self.order_item2.oid)} - {str(self.order_item2.pid)}")

    def test_feedback_str(self):
        self.assertEqual(str(self.feedback1), f"Feedback by User {str(self.feedback1.uid)} on Product {str(self.feedback1.pid)}")
        self.assertEqual(str(self.feedback2), f"Feedback by User {str(self.feedback2.uid)} on Product {str(self.feedback2.pid)}")

