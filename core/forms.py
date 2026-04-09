from django import forms


class BootstrapFormMixin:
    """Adds Bootstrap-friendly classes to forms for a consistent UI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

            if field.required:
                field.widget.attrs.setdefault("placeholder", field.label)
