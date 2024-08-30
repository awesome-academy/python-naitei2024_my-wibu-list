from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from wibu_catalog.models import Product, Content
import json


class AddToCartViewTest(TestCase):
    def setUp(self):
        self.content1 = Content.objects.create(
            cid=1,
            name="Content A",
            category="anime",
            scoreAvg=8.5
        )

        self.client = Client()

        self.product = Product.objects.create(
            pid=1,
            name="Product 1",
            price=100.0,
            cid=self.content1
        )
        self.url = reverse("add_to_cart")

    def test_add_new_product_to_cart(self):
        """Thêm sản phẩm mới vào giỏ hàng."""
        data = {
            "product_id": self.product.pid,
            "quantity": 2
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["cart_total"], 200.0)
        self.assertEqual(
            self.client.session["cart"][0]["product_id"], self.product.pid
        )
        self.assertEqual(self.client.session["cart"][0]["quantity"], 2)
        self.assertEqual(self.client.session["cart"][0]["subtotal"], 200.0)

    def test_product_not_found(self):
        """Kiểm tra trường hợp sản phẩm không tồn tại."""
        data = {
            "product_id": 999,  # ID không tồn tại
            "quantity": 1
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "Product not found.")

    def test_invalid_request_method(self):
        """Kiểm tra trường hợp yêu cầu không hợp lệ (GET thay vì POST)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "Invalid request method.")
