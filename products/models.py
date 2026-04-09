from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:category_products", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    sku = models.CharField(max_length=30, unique=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    specifications = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.slug])

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def average_rating(self):
        result = self.reviews.filter(is_approved=True).aggregate(avg=Avg("rating"))
        return round(result["avg"] or 0, 1)

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def discount_percentage(self):
        if self.discount_price and self.price:
            difference = self.price - self.discount_price
            return int((difference / self.price) * Decimal("100"))
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "id"]

    def __str__(self):
        return f"Image for {self.product.name}"

    def clean(self):
        super().clean()
        if (
            self.is_primary
            and self.product_id
            and ProductImage.objects.filter(product_id=self.product_id, is_primary=True)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {"is_primary": "Only one image per product can be marked as primary."}
            )
