from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    path("", views.stock_list, name="stock_list"),
    path("catalogue/", views.catalogue, name="catalogue"),
    path("produit/<int:product_id>/", views.product_detail, name="product_detail"),
    path("ajouter/", views.product_create, name="product_create"),
]
