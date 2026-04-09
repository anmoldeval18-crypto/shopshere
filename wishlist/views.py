from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from cart.models import CartItem
from cart.views import get_user_cart
from products.models import Product

from .models import Wishlist, WishlistItem


def get_user_wishlist(user):
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


@login_required
def wishlist_detail(request):
    wishlist = get_user_wishlist(request.user)
    return render(request, "wishlist/wishlist_detail.html", {"wishlist": wishlist})


@require_POST
@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    wishlist = get_user_wishlist(request.user)
    item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()

    if item:
        item.delete()
        messages.success(request, f"{product.name} removed from wishlist.")
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f"{product.name} added to wishlist.")

    referer = request.META.get("HTTP_REFERER")
    if referer and url_has_allowed_host_and_scheme(
        url=referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(referer)
    return redirect(reverse("products:product_list"))


@require_POST
@login_required
def remove_wishlist_item(request, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist__user=request.user)
    item.delete()
    messages.success(request, "Item removed from wishlist.")
    return redirect("wishlist:wishlist_detail")


@require_POST
@login_required
def move_to_cart(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, pk=item_id, wishlist__user=request.user)
    if wishlist_item.product.stock < 1:
        messages.error(request, "This product is currently out of stock.")
        return redirect("wishlist:wishlist_detail")

    cart = get_user_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=wishlist_item.product)

    if not created:
        if cart_item.quantity + 1 > wishlist_item.product.stock:
            messages.error(request, "Not enough stock to move this item to cart.")
            return redirect("wishlist:wishlist_detail")
        cart_item.quantity += 1
        cart_item.save()

    wishlist_item.delete()
    messages.success(request, "Item moved from wishlist to cart.")
    return redirect("cart:cart_detail")
