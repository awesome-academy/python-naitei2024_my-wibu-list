from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.auth.models import User
from wibu_catalog.models import Product, Content
from wibu_catalog.views import _calculate_cart_total, cart, get_product_price
from django.core.exceptions import ObjectDoesNotExist
from unittest.mock import Mock
# Helper function to set up session for tests
def setup_session(client):
    session = client.session
    session.save()
    return session

class RemoveFromCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create content and products
        self.content = Content.objects.create(cid=1, name="Test Content", scoreAvg=8.5)
        self.product1 = Product.objects.create(pid=1, name="Product 1", price=100, cid=self.content)
        self.product2 = Product.objects.create(pid=2, name="Product 2", price=200, cid=self.content)
        self.product3 = Product.objects.create(pid=3, name="Product 3", price=300, cid=self.content)

        # Set up session data
        session = setup_session(self.client)
        session["cart"] = [
            {"product_id": self.product1.pid, "quantity": 2},
            {"product_id": self.product2.pid, "quantity": 1}
        ]
        session.save()

    def test_remove_existing_item(self):
        response = self.client.post(reverse("remove_from_cart"), {"item_id": self.product1.pid})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))
        self.assertEqual(len(self.client.session["cart"]), 1)

    def test_remove_existing_item_by_id(self):

        # Check if product_id is None
        self.assertIsNotNone(self.product3.pid, "product_id is None")

        # Call the API to remove the item
        response = self.client.post(reverse("remove_from_cart"), {"product_id": self.product3.pid})

        # Print the response data
        print("Response data: ", response.json())

        # Print the status code
        print("Status code: ", response.status_code)

        # Check if the API call was successful
        self.assertEqual(response.status_code, 200)

class GetProductPriceTestCase(TestCase):
    def setUp(self):
        self.content = Content.objects.create(cid=1, name="Test Content", scoreAvg=8.5)
        self.product1 = Product.objects.create(pid=1, name="Product 1", price=100, cid=self.content)
        self.product2 = Product.objects.create(pid=2, name="Product 2", price=200, cid=self.content)

    def test_get_price_existing_product(self):
        self.assertEqual(get_product_price(self.product1.pid), 100)
        self.assertEqual(get_product_price(self.product2.pid), 200)

    def test_get_price_non_existent_product(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_product_price(999)
class UpdateQuantityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.content = Content.objects.create(cid=1, name="Test Content", scoreAvg=8.5)
        self.product1 = Product.objects.create(pid=1, name="Product 1", price=100, inventory=10, cid=self.content)
        self.product2 = Product.objects.create(pid=2, name="Product 2", price=200, inventory=5, cid=self.content)

        session = setup_session(self.client)
        session["cart"] = [{"product_id": self.product1.pid, "quantity": 2}]
        session.save()

    def test_update_existing_product_quantity(self):
        response = self.client.post(reverse("update_quantity"), {"product_id": self.product1.pid, "quantity": 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["cart"][0]["quantity"], 3)

    def test_update_invalid_quantity(self):
        response = self.client.post(reverse("update_quantity"), {"product_id": self.product1.pid, "quantity": 0})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json().get("success"))

        response = self.client.post(reverse("update_quantity"), {"product_id": self.product2.pid, "quantity": 6})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json().get("success"))

class UpdateCartItemTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.content = Content.objects.create(cid=1, name="Test Content", scoreAvg=8.5)
        self.product1 = Product.objects.create(pid=1, name="Product 1", price=100, cid=self.content)
        self.product2 = Product.objects.create(pid=2, name="Product 2", price=200, cid=self.content)

        session = setup_session(self.client)
        session["cart"] = [{"product_id": self.product1.pid, "quantity": 2, "id": "1"}]
        session.save()

    def test_update_existing_cart_item(self):
        response = self.client.post(reverse("update_cart_item"), {"item_id": "1", "new_quantity": 5})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))
        self.assertEqual(self.client.session["cart"][0]["quantity"], 5)

    def test_update_non_existent_cart_item(self):
        response = self.client.post(reverse("update_cart_item"), {"item_id": 999, "new_quantity": 3})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json().get("success"))
        self.assertEqual(response.json().get("error"), "Product not found")

class CalculateCartTotalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.content = Content.objects.create(cid=1, name="Test Content", scoreAvg=8.5)
        self.product1 = Product.objects.create(pid=1, name="Product 1", price=100, cid=self.content)
        self.product2 = Product.objects.create(pid=2, name="Product 2", price=200, cid=self.content)
        # Create a mock request object
        mock_request = Mock()
        mock_request.session = {"user_id": 1}
        # Call the cart function with the mock request
        self.cart = cart(mock_request)

    def test_calculate_total(self):
        cart_items = [
            {"product_id": self.product1.pid, "quantity": 2, "subtotal": self.product1.price * 2},
            {"product_id": self.product2.pid, "quantity": 1, "subtotal": self.product2.price}
            ]

        self.cart.add_item(self.product1, 5)  # Ensure the correct quantity and price
        total = _calculate_cart_total(self.cart.items)
        self.assertEqual(total, 500)

    def test_calculate_empty_cart(self):
        cart_items = []
        total = _calculate_cart_total(cart_items)
        self.assertEqual(total, 0)

class CartViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.content = Content.objects.create(cid=1, name="Test Content", scoreAvg=8.5)
        self.product1 = Product.objects.create(pid=1, name="Product 1", price=100, cid=self.content)
        self.product2 = Product.objects.create(pid=2, name="Product 2", price=200, cid=self.content)

        session = setup_session(self.client)
        session["cart"] = [{"product_id": self.product1.pid, "quantity": 2}]
        session.save()

    def test_cart_view(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("cart_items", response.context)
        self.assertIn("cart_total", response.context)
        self.assertEqual(response.context["cart_total"], 200)

    def test_cart_view_with_non_existent_product(self):
        session = setup_session(self.client)
        session["cart"].append({"product_id": 999, "quantity": 1})
        session.save()

        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cart_items"]), 1)
        self.assertEqual(response.context["cart_total"], 200)
