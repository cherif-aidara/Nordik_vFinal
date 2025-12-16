from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from . import views

app_name = "pgi"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Redirections vers les nouvelles applications
    # Ces routes conservent les anciens noms pour compatibilité avec les templates
    path("stocks/", lambda request: redirect("stocks:stock_list"), name="stocks"),
    path("finances/", lambda request: redirect("finances:finances"), name="finances"),
    path("clients/", lambda request: redirect("clients:clients"), name="clients"),
    # Pages principales de l'application pgi
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="pgi:login"), name="logout"),
    path("parametres/", views.settings, name="settings"),
]


