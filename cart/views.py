from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .models import Cart, CartItem


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = get_user_cart(request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_user_cart(request.user)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        quantity += item.quantity

    if quantity > product.stock:
        messages.error(request, "Requested quantity exceeds available stock.")
        return redirect(product.get_absolute_url())

    item.quantity = quantity
    item.save()
    messages.success(request, f"{product.name} added to your cart.")
    return redirect("cart:cart_detail")


@require_POST
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        item.delete()
        messages.success(request, "Item removed from cart.")
    elif quantity > item.product.stock:
        messages.error(request, "Requested quantity exceeds available stock.")
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, "Cart updated successfully.")

    return redirect("cart:cart_detail")


@require_POST
@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect("cart:cart_detail")
