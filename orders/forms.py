from django import forms

from accounts.models import Address
from core.forms import BootstrapFormMixin


class CheckoutForm(BootstrapFormMixin, forms.Form):
    existing_address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=False,
        empty_label="Select a saved address",
    )
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    address_line_1 = forms.CharField(required=False)
    address_line_2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    country = forms.CharField(required=False, initial="India")
    save_address = forms.BooleanField(required=False)
    payment_method = forms.ChoiceField(
        choices=[
            ("cod", "Cash on Delivery"),
            ("dummy_online", "Online Payment (Dummy)"),
        ],
        widget=forms.RadioSelect,
        initial="cod",
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["existing_address"].queryset = user.addresses.all()
            self.fields["email"].initial = user.email
            self.fields["full_name"].initial = user.get_full_name()
            profile = getattr(user, "profile", None)
            if profile:
                self.fields["phone_number"].initial = profile.phone_number

    def clean(self):
        cleaned_data = super().clean()
        existing_address = cleaned_data.get("existing_address")
        email = cleaned_data.get("email")
        required_new_address_fields = [
            "full_name",
            "phone_number",
            "address_line_1",
            "city",
            "state",
            "postal_code",
            "country",
        ]

        if not email:
            raise forms.ValidationError("Please provide an email address for order updates.")

        if not existing_address:
            missing_fields = [
                field for field in required_new_address_fields if not cleaned_data.get(field)
            ]
            if missing_fields:
                raise forms.ValidationError(
                    "Please select a saved address or fill in all shipping details."
                )

        return cleaned_data
