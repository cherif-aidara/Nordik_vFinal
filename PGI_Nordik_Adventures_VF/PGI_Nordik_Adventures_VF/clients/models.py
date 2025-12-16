from django.db import models
from django.core.exceptions import ValidationError
from common.models import TimeStampedModel


class Client(TimeStampedModel):
    """Client de l'entreprise."""

    CLIENT_TYPE_INDIVIDUAL = "individual"
    CLIENT_TYPE_COMPANY = "company"
    CLIENT_TYPE_PARTNER = "partner"
    CLIENT_TYPE_CHOICES = [
        (CLIENT_TYPE_INDIVIDUAL, "Individuel"),
        (CLIENT_TYPE_COMPANY, "Entreprise"),
        (CLIENT_TYPE_PARTNER, "Partenaire"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Actif"),
        (STATUS_INACTIVE, "Inactif"),
    ]

    name = models.CharField("Nom", max_length=255)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    address = models.TextField("Adresse", blank=True)
    client_type = models.CharField(
        "Type de client",
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        default=CLIENT_TYPE_INDIVIDUAL,
    )
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    loyalty_score = models.PositiveIntegerField(
        "Score de fidélité (1-5)", default=3, help_text="Note de 1 à 5"
    )
    satisfaction_score = models.PositiveIntegerField(
        "Score de satisfaction (%)", default=0, help_text="Pourcentage de satisfaction"
    )
    total_orders = models.PositiveIntegerField("Nombre total de commandes", default=0)
    total_spent = models.DecimalField(
        "Montant total dépensé ($)", max_digits=10, decimal_places=2, default=0
    )
    last_activity_date = models.DateField("Dernière activité", blank=True, null=True)
    notes = models.TextField("Notes", blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"
    
    def clean(self):
        """Validation des données du client."""
        if self.loyalty_score < 1 or self.loyalty_score > 5:
            raise ValidationError({
                "loyalty_score": "Le score de fidélité doit être entre 1 et 5"
            })
        if self.satisfaction_score < 0 or self.satisfaction_score > 100:
            raise ValidationError({
                "satisfaction_score": "Le score de satisfaction doit être entre 0 et 100"
            })
        if self.total_orders < 0:
            raise ValidationError({
                "total_orders": "Le nombre de commandes ne peut pas être négatif"
            })
        if self.total_spent < 0:
            raise ValidationError({
                "total_spent": "Le montant total dépensé ne peut pas être négatif"
            })
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class ClientInteraction(TimeStampedModel):
    """Interaction avec un client (appel, email, message, etc.)."""

    INTERACTION_TYPE_CALL = "call"
    INTERACTION_TYPE_EMAIL = "email"
    INTERACTION_TYPE_MESSAGE = "message"
    INTERACTION_TYPE_MEETING = "meeting"
    INTERACTION_TYPE_OTHER = "other"
    INTERACTION_TYPE_CHOICES = [
        (INTERACTION_TYPE_CALL, "Appel téléphonique"),
        (INTERACTION_TYPE_EMAIL, "Email"),
        (INTERACTION_TYPE_MESSAGE, "Message"),
        (INTERACTION_TYPE_MEETING, "Réunion"),
        (INTERACTION_TYPE_OTHER, "Autre"),
    ]

    client = models.ForeignKey(
        Client,
        verbose_name="Client",
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    interaction_type = models.CharField(
        "Type d'interaction",
        max_length=20,
        choices=INTERACTION_TYPE_CHOICES,
    )
    subject = models.CharField("Sujet", max_length=255)
    description = models.TextField("Description")
    interaction_date = models.DateTimeField("Date de l'interaction")
    user_name = models.CharField("Utilisateur", max_length=100, blank=True)

    class Meta:
        verbose_name = "Interaction client"
        verbose_name_plural = "Interactions clients"
        ordering = ["-interaction_date"]

    def __str__(self) -> str:
        return f"{self.client.name} - {self.get_interaction_type_display()} - {self.subject}"


class ClientOrder(TimeStampedModel):
    """Commande d'un client."""

    STATUS_PENDING = "pending"
    STATUS_RECEIVED = "received"  # Réception
    STATUS_PREPARING = "preparing"  # Préparation
    STATUS_SHIPPED = "shipped"  # Expédiée
    STATUS_INVOICED = "invoiced"  # Facturée
    STATUS_PAID = "paid"  # Payée/fermée
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_RECEIVED, "Réception"),
        (STATUS_PREPARING, "Préparation"),
        (STATUS_SHIPPED, "Expédiée"),
        (STATUS_INVOICED, "Facturée"),
        (STATUS_PAID, "Payée/fermée"),
        (STATUS_CANCELLED, "Annulée"),
    ]

    client = models.ForeignKey(
        Client,
        verbose_name="Client",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    order_number = models.CharField("Numéro de commande", max_length=50, unique=True)
    order_date = models.DateField("Date de commande")
    total_amount = models.DecimalField("Montant total ($)", max_digits=10, decimal_places=2)
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    notes = models.TextField("Notes", blank=True)

    class Meta:
        verbose_name = "Commande client"
        verbose_name_plural = "Commandes clients"
        ordering = ["-order_date"]

    def __str__(self) -> str:
        return f"{self.order_number} - {self.client.name}"
    
    def clean(self):
        """Validation des données de commande."""
        if self.total_amount < 0:
            raise ValidationError({
                "total_amount": "Le montant total ne peut pas être négatif"
            })
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class OrderLineItem(TimeStampedModel):
    """Ligne de commande - Détail des produits dans une commande."""
    
    order = models.ForeignKey(
        ClientOrder,
        verbose_name="Commande",
        on_delete=models.CASCADE,
        related_name="line_items",
    )
    product = models.ForeignKey(
        "stocks.Product",
        verbose_name="Produit",
        on_delete=models.PROTECT,
        related_name="order_line_items",
    )
    quantity = models.PositiveIntegerField("Quantité")
    unit_price = models.DecimalField("Prix unitaire ($)", max_digits=10, decimal_places=2)
    line_total = models.DecimalField("Montant total ligne ($)", max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
        ordering = ["order", "id"]
    
    def __str__(self) -> str:
        return f"{self.order.order_number} - {self.product.name} x{self.quantity}"
    
    def clean(self):
        """Validation des données de ligne de commande."""
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


class ClientActivityLog(TimeStampedModel):
    """Historique horodaté des actions des clients."""
    
    ACTIVITY_TYPE_VISIT = "visit"
    ACTIVITY_TYPE_PAGE_VIEW = "page_view"
    ACTIVITY_TYPE_ORDER = "order"
    ACTIVITY_TYPE_EMAIL = "email"
    ACTIVITY_TYPE_CALL = "call"
    ACTIVITY_TYPE_DOCUMENT = "document"
    ACTIVITY_TYPE_OTHER = "other"
    ACTIVITY_TYPE_CHOICES = [
        (ACTIVITY_TYPE_VISIT, "Visite du site"),
        (ACTIVITY_TYPE_PAGE_VIEW, "Consultation de page"),
        (ACTIVITY_TYPE_ORDER, "Commande"),
        (ACTIVITY_TYPE_EMAIL, "Courriel"),
        (ACTIVITY_TYPE_CALL, "Appel téléphonique"),
        (ACTIVITY_TYPE_DOCUMENT, "Document (PDF, soumission)"),
        (ACTIVITY_TYPE_OTHER, "Autre"),
    ]
    
    client = models.ForeignKey(
        Client,
        verbose_name="Client",
        on_delete=models.CASCADE,
        related_name="activity_logs",
    )
    activity_type = models.CharField(
        "Type d'activité",
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
    )
    description = models.TextField("Description")
    page_url = models.URLField("URL de la page", blank=True)
    document = models.FileField("Document", upload_to="client_documents/", blank=True, null=True)
    user = models.ForeignKey(
        "auth.User",
        verbose_name="Employé",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="client_activity_logs",
    )
    
    class Meta:
        verbose_name = "Journal d'activité client"
        verbose_name_plural = "Journaux d'activité clients"
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.client.name} - {self.get_activity_type_display()} - {self.created_at}"


class OrderRating(TimeStampedModel):
    """Évaluation de satisfaction client (1 à 5 étoiles) après un achat."""
    
    order = models.OneToOneField(
        ClientOrder,
        verbose_name="Commande",
        on_delete=models.CASCADE,
        related_name="rating",
    )
    rating = models.PositiveIntegerField(
        "Note (1-5 étoiles)",
        help_text="Note de satisfaction de 1 à 5 étoiles"
    )
    comment = models.TextField("Commentaire", blank=True)
    
    class Meta:
        verbose_name = "Évaluation de commande"
        verbose_name_plural = "Évaluations de commandes"
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.order.order_number} - {self.rating} étoiles"
    
    def clean(self):
        """Validation de l'évaluation."""
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({
                "rating": "La note doit être entre 1 et 5 étoiles"
            })
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class Cart(TimeStampedModel):
    """Panier d'achats d'un client."""
    
    client = models.OneToOneField(
        Client,
        verbose_name="Client",
        on_delete=models.CASCADE,
        related_name="cart",
    )
    
    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
        ordering = ["-updated_at"]
    
    def __str__(self) -> str:
        return f"Panier de {self.client.name}"
    
    @property
    def total_items(self):
        """Nombre total d'articles dans le panier."""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        """Sous-total HT du panier."""
        from decimal import Decimal
        total = Decimal("0")
        for item in self.items.all():
            total += item.line_total
        return total
    
    @property
    def tps(self):
        """TPS (5%) calculée sur le sous-total."""
        from decimal import Decimal
        return self.subtotal * Decimal("0.05")
    
    @property
    def tvq(self):
        """TVQ (9.975%) calculée sur le sous-total."""
        from decimal import Decimal
        return self.subtotal * Decimal("0.09975")
    
    @property
    def total(self):
        """Total TTC du panier."""
        return self.subtotal + self.tps + self.tvq


class CartItem(TimeStampedModel):
    """Article dans un panier d'achats."""
    
    cart = models.ForeignKey(
        Cart,
        verbose_name="Panier",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "stocks.Product",
        verbose_name="Produit",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField("Quantité", default=1)
    unit_price = models.DecimalField("Prix unitaire ($)", max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Article de panier"
        verbose_name_plural = "Articles de panier"
        ordering = ["cart", "id"]
        unique_together = [["cart", "product"]]
    
    def __str__(self) -> str:
        return f"{self.cart.client.name} - {self.product.name} x{self.quantity}"
    
    @property
    def line_total(self):
        """Montant total pour cette ligne."""
        return self.unit_price * self.quantity
    
    def clean(self):
        """Validation des données de l'article de panier."""
        if self.quantity <= 0:
            raise ValidationError({
                "quantity": "La quantité doit être supérieure à 0"
            })
        if self.quantity > self.product.quantity_in_stock:
            raise ValidationError({
                "quantity": f"Stock insuffisant. Disponible: {self.product.quantity_in_stock}"
            })
        # Utiliser le prix de vente du produit si le prix unitaire n'est pas défini
        if not self.unit_price or self.unit_price == 0:
            self.unit_price = self.product.sale_price
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation."""
        self.full_clean()
        super().save(*args, **kwargs)
