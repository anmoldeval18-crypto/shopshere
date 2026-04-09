from django.db.utils import OperationalError, ProgrammingError


def global_context(request):
    context = {
        "nav_categories": [],
        "cart_items_count": 0,
        "wishlist_items_count": 0,
    }

    try:
        from cart.models import CartItem
        from products.models import Category
        from wishlist.models import WishlistItem

        context["nav_categories"] = Category.objects.filter(is_active=True)[:8]
        if request.user.is_authenticated:
            context["cart_items_count"] = (
                CartItem.objects.filter(cart__user=request.user).count()
            )
            context["wishlist_items_count"] = (
                WishlistItem.objects.filter(wishlist__user=request.user).count()
            )
    except (OperationalError, ProgrammingError):
        # This keeps templates safe before the first migration is run.
        pass

    return context
