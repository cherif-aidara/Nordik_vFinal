from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    stock_entry_date = forms.DateField(
        label="Date d'entrée en stock",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Product
        fields = [
            "sku",
            "name",
            "category",
            "supplier",
            "purchase_cost",
            "sale_price",
            "quantity_in_stock",
            "reorder_threshold",
            "safety_stock",
            "supplier_discount",
            "weight_kg",
            "stock_entry_date",
            "warehouse_location",
            "status",
            "description",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " pgi-input").strip()
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label

    def save(self, commit=True):
        instance: Product = super().save(commit=False)
        purchase_cost = instance.purchase_cost
        sale_price = instance.sale_price
        if purchase_cost is not None and sale_price not in (None, 0):
            instance.gross_margin_percent = (
                (sale_price - purchase_cost) / sale_price
            ) * 100
        if commit:
            instance.save()
        return instance


