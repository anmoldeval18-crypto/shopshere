from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Address
from cart.models import Cart

from .forms import CheckoutForm
from .models import Order, OrderItem, Payment


def calculate_shipping(subtotal):
    return Decimal("0.00") if subtotal >= Decimal("1000.00") else Decimal("49.00")


def get_shipping_data(form, user):
    existing_address = form.cleaned_data["existing_address"]
    if existing_address:
        return {
            "full_name": existing_address.full_name,
            "email": form.cleaned_data["email"] or user.email,
            "phone_number": existing_address.phone_number,
            "address_line_1": existing_address.address_line_1,
            "address_line_2": existing_address.address_line_2,
            "city": existing_address.city,
            "state": existing_address.state,
            "postal_code": existing_address.postal_code,
            "country": existing_address.country,
        }

    shipping_data = {
        "full_name": form.cleaned_data["full_name"],
        "email": form.cleaned_data["email"] or user.email,
        "phone_number": form.cleaned_data["phone_number"],
        "address_line_1": form.cleaned_data["address_line_1"],
        "address_line_2": form.cleaned_data["address_line_2"],
        "city": form.cleaned_data["city"],
        "state": form.cleaned_data["state"],
        "postal_code": form.cleaned_data["postal_code"],
        "country": form.cleaned_data["country"],
    }

    if form.cleaned_data["save_address"]:
        Address.objects.create(
            user=user,
            label="Checkout Address",
            full_name=shipping_data["full_name"],
            phone_number=shipping_data["phone_number"],
            address_line_1=shipping_data["address_line_1"],
            address_line_2=shipping_data["address_line_2"],
            city=shipping_data["city"],
            state=shipping_data["state"],
            postal_code=shipping_data["postal_code"],
            country=shipping_data["country"],
            is_default=True,
        )

    return shipping_data


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty. Add products before checkout.")
        return redirect("products:product_list")

    form = CheckoutForm(request.POST or None, user=request.user)
    subtotal = cart.subtotal
    shipping_cost = calculate_shipping(subtotal)
    grand_total = subtotal + shipping_cost

    if request.method == "POST" and form.is_valid():
        cart_items = list(cart.items.select_related("product"))
        out_of_stock_products = [
            item.product.name for item in cart_items if item.quantity > item.product.stock
        ]
        if out_of_stock_products:
            messages.error(
                request,
                "Some items are no longer available in the requested quantity: "
                + ", ".join(out_of_stock_products),
            )
            return redirect("cart:cart_detail")

        with transaction.atomic():
            shipping_data = get_shipping_data(form, request.user)

            order = Order.objects.create(
                user=request.user,
                payment_method=form.cleaned_data["payment_method"],
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                total_amount=grand_total,
                notes=form.cleaned_data["notes"],
                **shipping_data,
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    price=cart_item.product.effective_price,
                    quantity=cart_item.quantity,
                )
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

            payment_status = "pending"
            paid_at = None
            transaction_id = ""
            if order.payment_method == "dummy_online":
                payment_status = "completed"
                paid_at = timezone.now()
                transaction_id = f"DUMMY-{order.order_number}"

            Payment.objects.create(
                order=order,
                payment_method=order.payment_method,
                status=payment_status,
                transaction_id=transaction_id,
                paid_at=paid_at,
            )

            cart.items.all().delete()
            messages.success(request, "Your order has been placed successfully.")
            return redirect("orders:order_confirmation", order_number=order.order_number)

    context = {
        "cart": cart,
        "form": form,
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "grand_total": grand_total,
    }
    return render(request, "orders/checkout.html", context)


@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        order_number=order_number,
        user=request.user,
    )
    return render(request, "orders/order_detail.html", {"order": order})
