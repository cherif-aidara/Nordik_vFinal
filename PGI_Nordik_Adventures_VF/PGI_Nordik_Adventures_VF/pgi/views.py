from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from clients.models import Client

# Import des fonctions utilitaires depuis les applications modulaires
from stocks.utils import get_stock_statistics
from finances.utils import get_finance_statistics
from clients.utils import get_client_statistics


def dashboard(request):
    """Vue du tableau de bord général.
    
    Cette vue agrège les données des trois modules :
    - stocks : statistiques de produits et inventaire
    - finances : statistiques financières
    - clients : statistiques clients
    """
    # Récupération des statistiques depuis chaque module
    stock_stats = get_stock_statistics()
    finance_stats = get_finance_statistics()
    client_stats = get_client_statistics()
    
    # Contexte combiné pour le tableau de bord
    context = {
        # Statistiques stocks
        **stock_stats,
        # Statistiques finances
        **finance_stats,
        # Statistiques clients
        "clients_count": client_stats["total_clients"],
        "active_clients": client_stats["active_clients"],
    }
    return render(request, "pgi/index.html", context)


# La vue stock_list a été déplacée dans stocks/views.py


# Les vues finances, finances_factures, finances_achats, finances_tresorerie 
# et clients ont été déplacées dans leurs applications respectives


def login_view(request):
    """Écran de connexion avec authentification Django."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Django Auth utilise username, pas email
        # On doit trouver l'utilisateur par email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.get_full_name() or user.username}!")
                return redirect("pgi:dashboard")
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
        except User.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect.")
    
    return render(request, "pgi/login.html")


def register(request):
    """Page d'inscription pour créer un compte client."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        
        # Validations
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "pgi/register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "pgi/register.html")
        
        # Créer l'utilisateur Django
        username = email.split("@")[0]  # Utiliser la partie avant @ comme username
        # S'assurer que le username est unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name.split()[0] if name else "",
            last_name=" ".join(name.split()[1:]) if len(name.split()) > 1 else "",
        )
        
        # Créer le client associé
        client = Client.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            status=Client.STATUS_ACTIVE,
        )
        
        # Connecter l'utilisateur
        login(request, user)
        messages.success(request, f"Compte créé avec succès! Bienvenue {name}!")
        return redirect("pgi:dashboard")
    
    return render(request, "pgi/register.html")


def settings(request):
    """Page Paramètres du PGI (taux fiscaux, options globales, etc.)."""
    # Pour l'instant, on envoie des valeurs statiques (maquette).
    contexte = {
        "tps": 5.0,
        "tvq": 9.975,
        "devise": "CAD",
        "seuil_stock_bas": 5,
        "delai_paiement_jours": 30,
    }
    return render(request, "pgi/settings.html", contexte)
