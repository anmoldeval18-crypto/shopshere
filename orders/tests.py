from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from cart.models import Cart, CartItem
from orders.admin import OrderAdmin
from orders.models import Order
from products.models import Category, Product
from reviews.models import Review


class ShoppingFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="Password123!",
            first_name="Test",
            last_name="User",
        )
        self.category = Category.objects.create(
            name="Books",
            slug="books",
            description="Books category",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Django Guide",
            slug="django-guide",
            sku="BOOK-001",
            short_description="Learn Django",
            description="A beginner friendly Django book.",
            specifications="Paperback",
            price="649.00",
            discount_price="599.00",
            stock=8,
            is_active=True,
        )

    def test_cart_to_checkout_to_review_flow(self):
        self.client.login(username="tester", password="Password123!")

        add_response = self.client.post(
            reverse("cart:add_to_cart", args=[self.product.id]),
            {"quantity": 2},
        )
        self.assertEqual(add_response.status_code, 302)

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(CartItem.objects.get(cart=cart, product=self.product).quantity, 2)

        checkout_response = self.client.post(
            reverse("orders:checkout"),
            {
                "full_name": "Test User",
                "email": "tester@example.com",
                "phone_number": "9999999999",
                "address_line_1": "123 Student Street",
                "address_line_2": "Near Campus",
                "city": "Pune",
                "state": "Maharashtra",
                "postal_code": "411001",
                "country": "India",
                "payment_method": "cod",
                "notes": "Handle carefully",
            },
        )
        self.assertEqual(checkout_response.status_code, 302)

        order = Order.objects.get(user=self.user)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_amount, order.subtotal + order.shipping_cost)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 6)
        self.assertFalse(cart.items.exists())

        review_response = self.client.post(
            reverse("reviews:add_review", args=[self.product.slug]),
            {
                "rating": 5,
                "title": "Very Helpful",
                "comment": "This product met expectations.",
            },
        )
        self.assertEqual(review_response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, product=self.product).exists())


class OrderAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="Password123!",
        )
        self.category = Category.objects.create(
            name="Admin Books",
            slug="admin-books",
            description="Books category",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Admin Django Guide",
            slug="admin-django-guide",
            sku="BOOK-ADMIN-001",
            short_description="Learn Django",
            description="A beginner friendly Django book.",
            specifications="Paperback",
            price="649.00",
            discount_price="599.00",
            stock=8,
            is_active=True,
        )
        self.order = Order.objects.create(
            user=self.superuser,
            payment_method="dummy_online",
            subtotal="599.00",
            shipping_cost="0.00",
            total_amount="599.00",
            notes="Handle carefully",
            full_name="Admin User",
            email="admin@example.com",
            phone_number="9999999999",
            address_line_1="123 Student Street",
            city="Pune",
            state="Maharashtra",
            postal_code="411001",
            country="India",
        )

    def test_order_admin_change_view_keeps_historical_fields_read_only(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("admin:orders_order_change", args=[self.order.pk]))

        self.assertEqual(response.status_code, 200)
        form_fields = response.context["adminform"].form.fields
        self.assertIn("status", form_fields)
        self.assertIn("notes", form_fields)
        self.assertNotIn("payment_method", form_fields)
        self.assertNotIn("user", form_fields)
        self.assertNotIn("total_amount", form_fields)
        self.assertNotIn("full_name", form_fields)

    def test_order_admin_disables_manual_adds(self):
        model_admin = OrderAdmin(Order, admin.site)
        request = self.factory.get("/admin/orders/order/add/")
        request.user = self.superuser

        self.assertFalse(model_admin.has_add_permission(request))
