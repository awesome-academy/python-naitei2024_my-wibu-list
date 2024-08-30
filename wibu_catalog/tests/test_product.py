from django.test import TestCase, Client
from django.urls import reverse
from wibu_catalog.models import Product, Content
from rest_framework import status
from wibu_catalog.views import get_product_price
from django.core.exceptions import ObjectDoesNotExist
import json

class AddToCartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        content, created = Content.objects.get_or_create(
            cid='1',
            name='content1',
            category='anime',
        )
        cls.product = Product.objects.create(
            pid='1',
            price=100.0,
            cid=content
        )

    def setUp(self):
        self.client = Client()
        self.add_to_cart_url = reverse('add_to_cart')

    def test_add_to_cart_post(self):
        # Kiểm tra việc thêm sản phẩm vào giỏ hàng bằng phương thức POST
        response = self.client.post(self.add_to_cart_url,
                                    data=json.dumps({"product_id": "1", "quantity": 1}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"success": True, "cart_total": 100.0})

    def test_add_to_cart_product_not_found(self):
        # Kiểm tra việc thêm sản phẩm không tồn tại vào giỏ hàng
        response = self.client.post(self.add_to_cart_url,
                                    data=json.dumps({"product_id": "2", "quantity": 1}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"success": False, "error": "Product not found."})

    def test_add_to_cart_invalid_method(self):
        # Kiểm tra việc thêm sản phẩm vào giỏ hàng bằng phương thức yêu cầu không hợp lệ (GET)
        response = self.client.get(self.add_to_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"success": False, "error": "Invalid request method."})

    def test_invalid_request_method(self):
        # Kiểm tra việc yêu cầu phương thức không hợp lệ
        response = self.client.get(reverse('add_to_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": False, "error": "Invalid request method."})

    def test_product_not_found(self):
        # Kiểm tra việc thêm sản phẩm không tồn tại vào giỏ hàng
        response = self.client.post(reverse('add_to_cart'), {'product_id': '2', 'quantity': '1'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": False, "error": "Product not found."})

    def test_add_new_product_to_cart(self):
        # Kiểm tra việc thêm sản phẩm mới vào giỏ hàng
        response = self.client.post(reverse('add_to_cart'), {'product_id': '1', 'quantity': '1'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True, "cart_total": 100.0})

    def test_add_existing_product_to_cart(self):
        session = self.client.session
        session['cart'] = [{'product_id': '1', 'quantity': 1, 'subtotal': 100.0}]
        session.save()

        # Kiểm tra việc thêm sản phẩm đã tồn tại vào giỏ hàng
        response = self.client.post(reverse('add_to_cart'), {'product_id': '1', 'quantity': '1'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True, "cart_total": 200.0})



class GetProductPriceTest(TestCase):
    def setUp(self):
        self.content = Content.objects.create(
            cid='1',
            name='content1',
            category='anime'
        )
        self.product = Product.objects.create(
            pid='1',
            price=100.0,
            cid=self.content
        )

    def test_product_exists(self):
        price = get_product_price('1')
        self.assertEqual(price, 100.0)

    def test_product_does_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            price = get_product_price('2')
