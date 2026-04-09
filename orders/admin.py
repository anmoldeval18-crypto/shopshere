from django.contrib import admin

from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    max_num = 0
    fields = ("product", "product_name", "price", "quantity", "total_price")
    readonly_fields = fields

    def total_price(self, obj):
        if not obj or obj.price is None:
            return "-"
        return obj.total_price

    total_price.short_description = "Total"


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    can_delete = False
    max_num = 0
    fields = ("payment_method", "status", "transaction_id", "paid_at", "created_at")
    readonly_fields = fields


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "payment_method",
        "total_amount",
        "placed_at",
    )
    list_filter = ("status", "payment_method", "placed_at")
    search_fields = ("order_number", "user__username", "full_name", "email")
    list_editable = ("status",)
    readonly_fields = (
        "order_number",
        "user",
        "payment_method",
        "subtotal",
        "shipping_cost",
        "total_amount",
        "full_name",
        "email",
        "phone_number",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "postal_code",
        "country",
        "placed_at",
        "updated_at",
    )
    autocomplete_fields = ("user",)
    list_per_page = 20
    inlines = [OrderItemInline, PaymentInline]

    def has_add_permission(self, request):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "price", "quantity", "total_price")
    readonly_fields = ("order", "product", "product_name", "price", "quantity", "total_price")
    search_fields = ("order__order_number", "product_name")

    def total_price(self, obj):
        if not obj or obj.price is None:
            return "-"
        return obj.total_price

    total_price.short_description = "Total"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "payment_method", "status", "transaction_id", "paid_at")
    list_filter = ("status", "payment_method")
    readonly_fields = ("order", "payment_method", "created_at")
    autocomplete_fields = ("order",)

    def has_add_permission(self, request):
        return False
