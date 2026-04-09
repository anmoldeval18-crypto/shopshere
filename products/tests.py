from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Category, Product, ProductImage


class ProductImageModelTests(TestCase):
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
        )

    def test_only_one_primary_image_per_product(self):
        ProductImage.objects.create(
            product=self.product,
            image="products/primary-one.jpg",
            is_primary=True,
        )
        duplicate_primary = ProductImage(
            product=self.product,
            image="products/primary-two.jpg",
            is_primary=True,
        )

        with self.assertRaises(ValidationError):
            duplicate_primary.full_clean()
