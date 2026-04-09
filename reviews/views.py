from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from orders.models import OrderItem
from products.models import Product

from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if not OrderItem.objects.filter(order__user=request.user, product=product).exists():
        messages.error(request, "You can review only products that you have purchased.")
        return redirect(product.get_absolute_url())

    if Review.objects.filter(user=request.user, product=product).exists():
        messages.error(request, "You have already reviewed this product.")
        return redirect(product.get_absolute_url())

    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        messages.success(request, "Thank you for reviewing this product.")
        return redirect(product.get_absolute_url())

    messages.error(request, "Please submit a valid review.")
    return redirect(product.get_absolute_url())
