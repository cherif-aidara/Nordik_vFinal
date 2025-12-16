"""Signaux Django pour automatiser les règles d'affaires."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClientOrder, OrderLineItem, ClientActivityLog
from stocks.models import StockMovement, Product


@receiver(post_save, sender=OrderLineItem)
def update_stock_on_sale(sender, instance, created, **kwargs):
    """Mise à jour automatique du stock après une vente (règle d'affaires TP#2)."""
    if created:  # Seulement lors de la création
        product = instance.product
        quantity = instance.quantity
        
        # Créer un mouvement de stock (sortie)
        StockMovement.objects.create(
            product=product,
            movement_type=StockMovement.MOVEMENT_OUT,
            quantity=quantity,
            reason=f"Vente - Commande {instance.order.order_number}",
            reference=instance.order.order_number,
        )
        
        # Diminuer la quantité en stock
        if product.quantity_in_stock >= quantity:
            product.quantity_in_stock -= quantity
            product.save(update_fields=["quantity_in_stock"])
        else:
            # Ne devrait pas arriver car validation dans clean()
            pass


@receiver(post_save, sender=ClientOrder)
def create_welcome_message(sender, instance, created, **kwargs):
    """Message de bienvenue automatisé lors de la première commande."""
    if created:
        client = instance.client
        
        # Vérifier si c'est la première commande
        if client.total_orders == 1:
            ClientActivityLog.objects.create(
                client=client,
                activity_type=ClientActivityLog.ACTIVITY_TYPE_EMAIL,
                description=f"Message de bienvenue automatisé - Première commande #{instance.order_number}",
            )


@receiver(post_save, sender=ClientOrder)
def create_sale_interaction(sender, instance, created, **kwargs):
    """Créer automatiquement une interaction client lors d'une vente."""
    if created:
        ClientActivityLog.objects.create(
            client=instance.client,
            activity_type=ClientActivityLog.ACTIVITY_TYPE_ORDER,
            description=f"Commande créée - {instance.order_number} - Montant: {instance.total_amount} $",
        )

