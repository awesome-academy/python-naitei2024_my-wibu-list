from django.test import TestCase
from django.urls import reverse
from ..models import Product, Content


class ProductViewTests(TestCase):
    def setUp(self):
        self.content1 = Content.objects.create(
            cid=1,
            name="Content A",
            category="anime",
            scoreAvg=8.5
        )
        self.content2 = Content.objects.create(
            cid=2,
            name="Content B",
            category="manga",
            scoreAvg=7.0
        )
        self.content3 = Content.objects.create(
            cid=3,
            name="Content C",
            category="anime",
            scoreAvg=9.0
        )
        # Tạo các sản phẩm mẫu
        self.product1 = Product.objects.create(
            pid=1,
            name="Product A",
            price=10.0,
            ravg=4.5,
            cid=self.content1
        )
        self.product2 = Product.objects.create(
            pid=2,
            name="Product B",
            price=20.0,
            ravg=3.5,
            cid=self.content2
        )
        self.product3 = Product.objects.create(
            pid=3,
            name="Product C",
            price=15.0,
            ravg=4.0,
            cid=self.content3
        )

    def test_search_by_keyword(self):
        """Kiểm tra chức năng tìm kiếm sản phẩm theo từ khóa."""
        response = self.client.get(
            reverse('product'), {'q': 'Product A'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product A')
        self.assertNotContains(response, 'Product B')
        self.assertNotContains(response, 'Product C')

    def test_sort_by_rating(self):
        """Kiểm tra chức năng sắp xếp sản phẩm theo đánh giá (rating)."""
        response = self.client.get(
            reverse('product'), {'sort_by': 'highest_rate'}
        )
        self.assertEqual(response.status_code, 200)
        products = response.context['products']

        self.assertEqual(products[0], self.product1)
        self.assertEqual(products[1], self.product3)
        self.assertEqual(products[2], self.product2)

    def test_sort_by_price_low_to_high(self):
        """Kiểm tra chức năng sắp xếp sản phẩm theo giá từ thấp đến cao."""
        response = self.client.get(
            reverse('product'), {'sort_by': 'low_to_high'}
        )
        self.assertEqual(response.status_code, 200)
        products = response.context['products']

        self.assertEqual(products[0], self.product1)
        self.assertEqual(products[1], self.product3)
        self.assertEqual(products[2], self.product2)

    def test_sort_by_price_high_to_low(self):
        """Kiểm tra chức năng sắp xếp sản phẩm theo giá từ cao đến thấp."""
        response = self.client.get(
            reverse('product'), {'sort_by': 'high_to_low'}
        )
        self.assertEqual(response.status_code, 200)
        products = response.context['products']

        self.assertEqual(products[0], self.product2)
        self.assertEqual(products[1], self.product3)
        self.assertEqual(products[2], self.product1)
