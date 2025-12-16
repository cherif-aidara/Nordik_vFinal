from django.contrib import admin
from .models import (
    Client, ClientInteraction, ClientOrder,
    OrderLineItem, ClientActivityLog, OrderRating,
    Cart, CartItem
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "client_type",
        "status",
        "loyalty_score",
        "satisfaction_score",
        "total_orders",
        "total_spent",
    )
    list_filter = ("client_type", "status", "loyalty_score")
    search_fields = ("name", "email", "phone")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ClientInteraction)
class ClientInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "interaction_type",
        "subject",
        "interaction_date",
        "user_name",
    )
    list_filter = ("interaction_type", "interaction_date")
    search_fields = ("client__name", "subject", "description")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "interaction_date"


@admin.register(ClientOrder)
class ClientOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "client",
        "total_amount",
        "order_date",
        "status",
    )
    list_filter = ("status", "order_date")
    search_fields = ("order_number", "client__name", "client__email")
    readonly_fields = ("created_at", "updated_at", "order_number")
    date_hierarchy = "order_date"
    list_editable = ("status",)  # Permet de changer le statut directement dans la liste
    actions = ["mark_as_received", "mark_as_preparing", "mark_as_shipped", "mark_as_invoiced", "mark_as_paid"]
    
    def mark_as_received(self, request, queryset):
        """Action pour marquer les commandes comme reçues."""
        queryset.update(status=ClientOrder.STATUS_RECEIVED)
        self.message_user(request, f"{queryset.count()} commande(s) marquée(s) comme reçue(s).")
    mark_as_received.short_description = "Marquer comme reçue"
    
    def mark_as_preparing(self, request, queryset):
        """Action pour marquer les commandes comme en préparation."""
        queryset.update(status=ClientOrder.STATUS_PREPARING)
        self.message_user(request, f"{queryset.count()} commande(s) marquée(s) comme en préparation.")
    mark_as_preparing.short_description = "Marquer comme en préparation"
    
    def mark_as_shipped(self, request, queryset):
        """Action pour marquer les commandes comme expédiées."""
        queryset.update(status=ClientOrder.STATUS_SHIPPED)
        self.message_user(request, f"{queryset.count()} commande(s) marquée(s) comme expédiée(s).")
    mark_as_shipped.short_description = "Marquer comme expédiée"
    
    def mark_as_invoiced(self, request, queryset):
        """Action pour marquer les commandes comme facturées."""
        queryset.update(status=ClientOrder.STATUS_INVOICED)
        self.message_user(request, f"{queryset.count()} commande(s) marquée(s) comme facturée(s).")
    mark_as_invoiced.short_description = "Marquer comme facturée"
    
    def mark_as_paid(self, request, queryset):
        """Action pour marquer les commandes comme payées."""
        queryset.update(status=ClientOrder.STATUS_PAID)
        self.message_user(request, f"{queryset.count()} commande(s) marquée(s) comme payée(s).")
    mark_as_paid.short_description = "Marquer comme payée"


@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price", "line_total")
    list_filter = ("order__status", "order__order_date")
    search_fields = ("order__order_number", "product__name", "product__sku")
    readonly_fields = ("created_at", "updated_at", "line_total")


@admin.register(ClientActivityLog)
class ClientActivityLogAdmin(admin.ModelAdmin):
    list_display = ("client", "activity_type", "description", "created_at", "user")
    list_filter = ("activity_type", "created_at")
    search_fields = ("client__name", "description", "page_url")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(OrderRating)
class OrderRatingAdmin(admin.ModelAdmin):
    list_display = ("order", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("order__order_number", "order__client__name", "comment")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("client", "total_items", "subtotal", "total", "updated_at")
    search_fields = ("client__name", "client__email")
    readonly_fields = ("created_at", "updated_at", "total_items", "subtotal", "tps", "tvq", "total")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "unit_price", "line_total")
    list_filter = ("cart__client",)
    search_fields = ("cart__client__name", "product__name", "product__sku")
    readonly_fields = ("created_at", "updated_at", "line_total")
