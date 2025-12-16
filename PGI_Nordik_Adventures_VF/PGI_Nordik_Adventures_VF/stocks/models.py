from django.db import models
from django.core.exceptions import ValidationError
from common.models import TimeStampedModel


class ProductCategory(models.Model):
    """Catégorie de produit."""

    name = models.CharField("Nom de la catégorie", max_length=100, unique=True)
    description = models.TextField("Description", blank=True)

    class Meta:
        verbose_name = "Catégorie de produit"
        verbose_name_plural = "Catégories de produits"

    def __str__(self) -> str:
        return self.name


class Supplier(models.Model):
    """Fournisseur de produits."""

    name = models.CharField("Fournisseur", max_length=150)
    code = models.CharField("Code fournisseur", max_length=50, unique=True)
    default_discount = models.DecimalField(
        "Remise fournisseur (%)", max_digits=5, decimal_places=2, default=0
    )
    delivery_delay_days = models.PositiveIntegerField(
        "Délai de livraison (jours)", default=0
    )

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Product(TimeStampedModel):
    """Produit en stock."""

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Actif"),
        (STATUS_INACTIVE, "Inactif"),
    ]

    sku = models.CharField("SKU", max_length=20, unique=True)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="Catégorie",
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField("Nom du produit", max_length=255)
    description = models.TextField("Description", blank=True)
    image = models.ImageField("Photo", upload_to="products/", blank=True, null=True)
    purchase_cost = models.DecimalField(
        "Coût d'achat ($)", max_digits=10, decimal_places=2
    )
    sale_price = models.DecimalField(
        "Prix de vente ($)", max_digits=10, decimal_places=2
    )
    gross_margin_percent = models.DecimalField(
        "Marge brute (%)", max_digits=5, decimal_places=2
    )

    quantity_in_stock = models.PositiveIntegerField("Quantité en stock", default=0)
    reorder_threshold = models.PositiveIntegerField(
        "Seuil de réapprovisionnement", default=0
    )
    safety_stock = models.PositiveIntegerField("Stock minimum de sécurité", default=0)

    supplier = models.ForeignKey(
        Supplier,
        verbose_name="Fournisseur",
        on_delete=models.PROTECT,
        related_name="products",
    )
    supplier_discount = models.DecimalField(
        "Remise fournisseur (%)", max_digits=5, decimal_places=2, default=0
    )
    weight_kg = models.DecimalField("Poids (kg)", max_digits=6, decimal_places=2)
    stock_entry_date = models.DateField("Date d'entrée en stock")
    warehouse_location = models.CharField("Emplacement entrepôt", max_length=20)

    status = models.CharField(
        "Statut produit",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["sku"]

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"

    @property
    def total_stock_value(self):
        """Valeur totale du stock pour ce produit."""
        return self.purchase_cost * self.quantity_in_stock

    @property
    def is_below_reorder(self) -> bool:
        """Vérifie si le stock est en dessous du seuil de réapprovisionnement."""
        return self.quantity_in_stock <= self.reorder_threshold
    
    def clean(self):
        """Validation des données du produit."""
        if self.sale_price <= self.purchase_cost:
            raise ValidationError({
                "sale_price": "Le prix de vente doit être supérieur au coût d'achat"
            })
        if self.quantity_in_stock < 0:
            raise ValidationError({
                "quantity_in_stock": "La quantité en stock ne peut pas être négative"
            })
        if self.reorder_threshold < 0:
            raise ValidationError({
                "reorder_threshold": "Le seuil de réapprovisionnement ne peut pas être négatif"
            })
        if self.safety_stock < 0:
            raise ValidationError({
                "safety_stock": "Le stock minimum de sécurité ne peut pas être négatif"
            })
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class StockMovement(TimeStampedModel):
    """Mouvement de stock (entrée/sortie)."""

    MOVEMENT_IN = "in"
    MOVEMENT_OUT = "out"
    MOVEMENT_CHOICES = [
        (MOVEMENT_IN, "Entrée"),
        (MOVEMENT_OUT, "Sortie"),
    ]

    product = models.ForeignKey(
        Product,
        verbose_name="Produit",
        on_delete=models.PROTECT,
        related_name="movements",
    )
    movement_type = models.CharField(
        "Type de mouvement",
        max_length=10,
        choices=MOVEMENT_CHOICES,
    )
    quantity = models.PositiveIntegerField("Quantité")
    reason = models.CharField("Raison", max_length=255, blank=True)
    reference = models.CharField("Référence", max_length=100, blank=True)

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.movement_type} - {self.product.sku} - {self.quantity}"
    
    def clean(self):
        """Validation des données de mouvement de stock."""
        if self.quantity <= 0:
            raise ValidationError({
                "quantity": "La quantité doit être supérieure à 0"
            })
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)
