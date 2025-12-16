from django import forms

from .models import Invoice, Expense


class InvoiceForm(forms.ModelForm):
    """Formulaire simple de création / édition de facture manuelle.

    - L'utilisateur saisit uniquement les infos visibles dans l'énoncé.
    - Les champs TPS, TVQ et Montant total sont calculés automatiquement
      dans le modèle `Invoice.clean()`.
    """

    invoice_date = forms.DateField(
        label="Date de facturation",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    due_date = forms.DateField(
        label="Date d'échéance",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "client_name",
            "client_email",
            "amount",
            "invoice_date",
            "due_date",
            "status",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer le style PGI sur tous les champs
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " pgi-input").strip()
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label


class ExpenseForm(forms.ModelForm):
    """Formulaire de création / édition d'un achat / dépense."""

    expense_date = forms.DateField(
        label="Date de dépense",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    due_date = forms.DateField(
        label="Date d'échéance",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Expense
        fields = [
            "supplier_name",
            "expense_type",
            "amount",
            "expense_date",
            "due_date",
            "status",
            "reference",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " pgi-input").strip()
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label


