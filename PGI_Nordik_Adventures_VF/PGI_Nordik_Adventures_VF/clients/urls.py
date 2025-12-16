from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path("", views.clients, name="clients"),
    # Gestion des clients & interactions
    path("nouveau/", views.client_create, name="client_create"),
    path("interaction/nouvelle/", views.client_interaction_create, name="interaction_create"),
    path("interaction/nouvelle/<int:client_id>/", views.client_interaction_create, name="interaction_create_for_client"),
    # Panier et commandes
    path("panier/", views.cart_view, name="cart"),
    path("panier/ajouter/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("panier/retirer/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("panier/modifier/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("checkout/", views.checkout, name="checkout"),
    path("mes-commandes/", views.my_orders, name="my_orders"),
    path("commande/<int:order_id>/evaluer/", views.rate_order, name="rate_order"),
    path("client/<int:client_id>/historique/", views.client_activity_history, name="client_activity_history"),
]
