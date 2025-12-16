from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Modules spécialisés en priorité pour éviter les boucles de redirection
    # (les anciennes routes `pgi:stocks`, `pgi:finances`, `pgi:clients`
    # continuent de pointer vers /stocks/, /finances/, /clients/ sans rediriger en boucle)
    path("stocks/", include("stocks.urls")),  # Module - Gestion des produits et des stocks
    path("finances/", include("finances.urls")),  # Module - Gestion financière et facturation
    path("clients/", include("clients.urls")),  # Module - Gestion de la relation client
    # Application principale (tableau de bord, login, settings)
    path("", include("pgi.urls")),
]


