from django import forms

from core.forms import BootstrapFormMixin

from .models import Review


class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }
