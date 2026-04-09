from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class CorePagesTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic products",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Bluetooth Speaker",
            slug="bluetooth-speaker",
            sku="SPK-001",
            short_description="Portable speaker",
            description="A compact wireless speaker.",
            specifications="10W output",
            price="1999.00",
            discount_price="1499.00",
            stock=10,
            is_active=True,
            is_featured=True,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ShopSphere")

    def test_product_pages_load(self):
        list_response = self.client.get(reverse("products:product_list"))
        detail_response = self.client.get(self.product.get_absolute_url())
        category_response = self.client.get(self.category.get_absolute_url())

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(category_response.status_code, 200)

    def test_dashboard_requires_staff_login(self):
        user = User.objects.create_user(username="student", password="Password123!")
        self.client.login(username="student", password="Password123!")
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 302)
