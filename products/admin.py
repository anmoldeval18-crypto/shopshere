from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "sku",
        "price",
        "discount_price",
        "stock",
        "is_featured",
        "is_trending",
        "preview_image",
    )
    list_filter = ("category", "is_active", "is_featured", "is_trending")
    search_fields = ("name", "sku")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    list_editable = ("stock", "is_featured", "is_trending")
    list_per_page = 20
    autocomplete_fields = ("category",)

    def preview_image(self, obj):
        image = obj.primary_image
        if image and image.image:
            return format_html('<img src="{}" width="40" height="40" />', image.image.url)
        return "No image"

    preview_image.short_description = "Preview"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_primary", "created_at")
    list_filter = ("is_primary",)
    autocomplete_fields = ("product",)
