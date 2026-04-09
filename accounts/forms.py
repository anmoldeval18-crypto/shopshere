from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from core.forms import BootstrapFormMixin

from .models import Address, Profile


class UserRegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class UserLoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already used by another account.")
        return email


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "bio", "profile_image"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}


class AddressForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "label",
            "full_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]
