from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import render

from orders.models import Order
from products.models import Category, Product


def home(request):
    product_queryset = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")
    featured_products = product_queryset.filter(is_featured=True)[:8]
    trending_products = product_queryset.filter(is_trending=True)[:8]
    new_arrivals = product_queryset.order_by("-created_at")[:8]
    categories = Category.objects.filter(is_active=True).annotate(product_count=Count("products"))[:6]

    context = {
        "featured_products": featured_products,
        "trending_products": trending_products,
        "new_arrivals": new_arrivals,
        "categories": categories,
    }
    return render(request, "core/home.html", context)


@staff_member_required
def dashboard(request):
    latest_orders = Order.objects.select_related("user").order_by("-placed_at")[:8]
    low_stock_products = Product.objects.filter(stock__lte=5, is_active=True).order_by("stock")[:8]

    dashboard_data = {
        "total_products": Product.objects.count(),
        "total_categories": Category.objects.count(),
        "total_orders": Order.objects.count(),
        "total_users": User.objects.count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "revenue": Order.objects.aggregate(total=Sum("total_amount"))["total"] or 0,
    }

    context = {
        "dashboard_data": dashboard_data,
        "latest_orders": latest_orders,
        "low_stock_products": low_stock_products,
    }
    return render(request, "core/dashboard.html", context)
