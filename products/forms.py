from django import forms

from core.forms import BootstrapFormMixin


class ProductFilterForm(BootstrapFormMixin, forms.Form):
    query = forms.CharField(required=False, label="Search")
    category = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ("latest", "Latest"),
            ("price_asc", "Price: Low to High"),
            ("price_desc", "Price: High to Low"),
        ],
    )
