from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from common.models import TimeStampedModel


class Invoice(TimeStampedModel):
    """Facture client."""

    STATUS_PAID = "paid"
    STATUS_PENDING = "pending"
    STATUS_OVERDUE = "overdue"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PAID, "Payée"),
        (STATUS_PENDING, "En attente"),
        (STATUS_OVERDUE, "En retard"),
        (STATUS_CANCELLED, "Annulée"),
    ]

    invoice_number = models.CharField("Numéro de facture", max_length=50, unique=True)
    client = models.ForeignKey(
        "clients.Client",
        verbose_name="Client",
        on_delete=models.PROTECT,
        related_name="invoices",
        null=True,
        blank=True,
    )
    client_name = models.CharField("Nom du client", max_length=255, blank=True)
    client_email = models.EmailField("Email du client", blank=True)
    amount = models.DecimalField("Montant HT ($)", max_digits=10, decimal_places=2)
    tps = models.DecimalField("TPS (5%)", max_digits=10, decimal_places=2, default=0)
    tvq = models.DecimalField("TVQ (9.975%)", max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField("Montant TTC ($)", max_digits=10, decimal_places=2)
    invoice_date = models.DateField("Date de facturation")
    due_date = models.DateField("Date d'échéance")
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    notes = models.TextField("Notes", blank=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ["-invoice_date"]

    def __str__(self) -> str:
        return f"{self.invoice_number} - {self.client_name}"

    def clean(self):
        """Validation et calcul automatique des taxes."""
        if self.amount < 0:
            raise ValidationError({"amount": "Le montant ne peut pas être négatif"})
        
        # Remplir client_name et client_email depuis le client si disponible
        if self.client:
            if not self.client_name:
                self.client_name = self.client.name
            if not self.client_email:
                self.client_email = self.client.email
        
        # Calcul automatique des taxes si elles ne sont pas définies
        two_dec = Decimal("0.01")
        if self.tps == 0 and not hasattr(self, "_tps_manually_set"):
            self.tps = (self.amount * Decimal("0.05")).quantize(two_dec)
        if self.tvq == 0 and not hasattr(self, "_tvq_manually_set"):
            self.tvq = (self.amount * Decimal("0.09975")).quantize(two_dec)

        # Calcul du montant total
        self.total_amount = (self.amount + self.tps + self.tvq).quantize(two_dec)
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class Expense(TimeStampedModel):
    """Dépense/achat."""

    STATUS_PAID = "paid"
    STATUS_PENDING = "pending"
    STATUS_OVERDUE = "overdue"
    STATUS_CHOICES = [
        (STATUS_PAID, "Payée"),
        (STATUS_PENDING, "En attente"),
        (STATUS_OVERDUE, "En retard"),
    ]

    EXPENSE_TYPE_STOCK = "stock"
    EXPENSE_TYPE_ENERGY = "energy"
    EXPENSE_TYPE_RENT = "rent"
    EXPENSE_TYPE_SALARY = "salary"
    EXPENSE_TYPE_OTHER = "other"
    EXPENSE_TYPE_CHOICES = [
        (EXPENSE_TYPE_STOCK, "Stock"),
        (EXPENSE_TYPE_ENERGY, "Énergie"),
        (EXPENSE_TYPE_RENT, "Loyer"),
        (EXPENSE_TYPE_SALARY, "Salaire"),
        (EXPENSE_TYPE_OTHER, "Autre"),
    ]

    supplier_name = models.CharField("Nom du fournisseur", max_length=255)
    expense_type = models.CharField(
        "Type de dépense",
        max_length=20,
        choices=EXPENSE_TYPE_CHOICES,
        default=EXPENSE_TYPE_OTHER,
    )
    amount = models.DecimalField("Montant ($)", max_digits=10, decimal_places=2)
    expense_date = models.DateField("Date de dépense")
    due_date = models.DateField("Date d'échéance", blank=True, null=True)
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    reference = models.CharField("Référence", max_length=100, blank=True)
    notes = models.TextField("Notes", blank=True)

    class Meta:
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"
        ordering = ["-expense_date"]

    def __str__(self) -> str:
        return f"{self.supplier_name} - {self.amount} $ - {self.get_expense_type_display()}"
    
    def clean(self):
        """Validation des données de dépense."""
        if self.amount < 0:
            raise ValidationError({"amount": "Le montant ne peut pas être négatif"})
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class CashFlow(TimeStampedModel):
    """Flux de trésorerie."""

    FLOW_IN = "in"
    FLOW_OUT = "out"
    FLOW_CHOICES = [
        (FLOW_IN, "Entrée"),
        (FLOW_OUT, "Sortie"),
    ]

    flow_type = models.CharField(
        "Type de flux",
        max_length=10,
        choices=FLOW_CHOICES,
    )
    amount = models.DecimalField("Montant ($)", max_digits=10, decimal_places=2)
    description = models.CharField("Description", max_length=255)
    flow_date = models.DateField("Date du flux")
    related_invoice = models.ForeignKey(
        Invoice,
        verbose_name="Facture liée",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="cash_flows",
    )
    related_expense = models.ForeignKey(
        Expense,
        verbose_name="Dépense liée",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="cash_flows",
    )

    class Meta:
        verbose_name = "Flux de trésorerie"
        verbose_name_plural = "Flux de trésorerie"
        ordering = ["-flow_date"]

    def __str__(self) -> str:
        return f"{self.get_flow_type_display()} - {self.amount} $ - {self.description}"


class InvoiceLineItem(TimeStampedModel):
    """Ligne de facture - Détail des produits dans une facture."""
    
    invoice = models.ForeignKey(
        Invoice,
        verbose_name="Facture",
        on_delete=models.CASCADE,
        related_name="line_items",
    )
    product = models.ForeignKey(
        "stocks.Product",
        verbose_name="Produit",
        on_delete=models.PROTECT,
        related_name="invoice_line_items",
    )
    quantity = models.PositiveIntegerField("Quantité")
    unit_price = models.DecimalField("Prix unitaire ($)", max_digits=10, decimal_places=2)
    line_total = models.DecimalField("Montant total ligne ($)", max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
        ordering = ["invoice", "id"]
    
    def __str__(self) -> str:
        return f"{self.invoice.invoice_number} - {self.product.name} x{self.quantity}"
    
    def clean(self):
        """Validation des données de ligne de facture."""
        if self.quantity <= 0:
            raise ValidationError({
                "quantity": "La quantité doit être supérieure à 0"
            })
        if self.unit_price < 0:
            raise ValidationError({
                "unit_price": "Le prix unitaire ne peut pas être négatif"
            })
        # Calcul automatique du total ligne
        self.line_total = self.unit_price * self.quantity
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)
