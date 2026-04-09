from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from orders.models import OrderItem
from reviews.forms import ReviewForm
from reviews.models import Review

from .models import Category, Product


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")
    categories = Category.objects.filter(is_active=True)

    query = request.GET.get("q")
    category_slug = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort", "latest")

    if query:
        products = products.filter(Q(name__icontains=query) | Q(short_description__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    else:
        products = products.order_by("-created_at")

    context = {
        "products": products,
        "categories": categories,
        "current_query": query or "",
        "current_category": category_slug or "",
        "current_min_price": min_price or "",
        "current_max_price": max_price or "",
        "current_sort": sort,
    }
    return render(request, "products/product_list.html", context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True).select_related("category").prefetch_related("images")
    return render(
        request,
        "products/category_products.html",
        {"category": category, "products": products},
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images"),
        slug=slug,
        is_active=True,
    )
    related_products = (
        Product.objects.filter(category=product.category, is_active=True)
        .select_related("category")
        .prefetch_related("images")
        .exclude(pk=product.pk)[:4]
    )
    reviews = Review.objects.filter(product=product, is_approved=True).select_related("user")

    can_review = False
    user_review_exists = False
    if request.user.is_authenticated:
        user_review_exists = reviews.filter(user=request.user).exists()
        can_review = OrderItem.objects.filter(order__user=request.user, product=product).exists()

    context = {
        "product": product,
        "related_products": related_products,
        "reviews": reviews,
        "review_form": ReviewForm(),
        "can_review": can_review,
        "user_review_exists": user_review_exists,
    }
    return render(request, "products/product_detail.html", context)
