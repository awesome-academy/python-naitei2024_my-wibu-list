from django.test import TestCase, Client
from django.urls import reverse
from ..models import Content, Users
from django.contrib.auth.hashers import make_password


class FilterByGenreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.genre = "Action"  # thể loại muốn tìm
        self.user = Users.objects.create(
            uid=1,
            username="testuser",
            email="testuser@example.com",
            password=make_password("password123"),
            dateOfBirth="1990-01-01",
            role="new_user"
        )
        self.client.session["user_id"] = self.user.uid
        self.client.session.save()

        # sản phẩm giả lập 1 chứa genre muốn tìm
        self.content1 = Content.objects.create(
            cid=1,
            name="Action Anime 1",
            genres="Action,Adventure",
            scoreAvg=8.5
        )
        # sản phẩm giả lập 2 chứa genre muốn tìm
        self.content2 = Content.objects.create(
            cid=2,
            name="Action Anime 2",
            genres="Action,Fantasy",
            scoreAvg=9.0
        )
        # sản phẩm giả lập 3 không chứa genre muốn tìm
        self.content3 = Content.objects.create(
            cid=3,
            name="Adventure Anime 1",
            genres="Adventure",
            scoreAvg=7.0
        )

        self.url = reverse("filter_by_genre", args=[self.genre])

    def test_filter_by_genre(self):
        response = self.client.get(self.url)
        # check xem yêu cầu có được xử lý thành công không
        self.assertEqual(response.status_code, 200)
        # check xem template có phải là filtered_content.html hay không
        self.assertTemplateUsed(response, "html/filtered_content.html")

        filtered_content = response.context["filtered_content"]
        # kiểm tra xem số lượng nội dung đã lọc được có phải là 2 hay không
        self.assertEqual(len(filtered_content), 2)
        # kiểm tra xem trong các sản phẩm lọc được có chứa sản phẩm 1
        self.assertIn(self.content1, filtered_content)
        # kiểm tra xem trong các sản phẩm lọc được có chứa sản phẩm 2
        self.assertIn(self.content2, filtered_content)
        # kiểm tra xxem trong các sản phẩm lọc được không chứa sản phẩm 3
        self.assertNotIn(self.content3, filtered_content)
