from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from orders.models import Order

from .forms import AddressForm, ProfileUpdateForm, UserRegistrationForm, UserUpdateForm
from .models import Address


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("core:home")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    address_form = AddressForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "profile":
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=request.user.profile,
            )
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile was updated successfully.")
                return redirect("accounts:profile")

        elif form_type == "address":
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
                messages.success(request, "Address saved successfully.")
                return redirect("accounts:profile")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "address_form": address_form,
        "addresses": request.user.addresses.all(),
        "recent_orders": Order.objects.filter(user=request.user)[:5],
    }
    return render(request, "accounts/profile.html", context)


@require_POST
@login_required
def set_default_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, "Default address updated.")
    return redirect("accounts:profile")


@require_POST
@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, "Address removed successfully.")
    return redirect("accounts:profile")
