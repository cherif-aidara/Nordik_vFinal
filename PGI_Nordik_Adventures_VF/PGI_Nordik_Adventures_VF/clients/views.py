from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from datetime import timedelta
from decimal import Decimal

from .models import Client, ClientInteraction, ClientOrder, OrderLineItem, Cart, CartItem, OrderRating, ClientActivityLog
from .forms import ClientForm, ClientInteractionForm
from stocks.models import Product


def clients(request):
    """Module Relations clients."""
    clients_list = Client.objects.all()

    total_clients = clients_list.count()
    active_clients = clients_list.filter(status=Client.STATUS_ACTIVE).count()

    # Calcul des statistiques
    avg_satisfaction = clients_list.aggregate(avg=Avg("satisfaction_score"))["avg"] or 0
    avg_loyalty = clients_list.aggregate(avg=Avg("loyalty_score"))["avg"] or 0
    total_interactions = ClientInteraction.objects.count()

    # Calcul réel de la croissance mensuelle
    now = timezone.now()
    last_month = now - timedelta(days=30)
    clients_last_month = Client.objects.filter(created_at__lt=last_month).count()
    clients_this_month = Client.objects.filter(created_at__gte=last_month).count()

    if clients_last_month > 0:
        monthly_growth = round(((clients_this_month - clients_last_month) / clients_last_month) * 100, 1)
    else:
        monthly_growth = clients_this_month * 100 if clients_this_month > 0 else 0

    # Répartition par type
    type_distribution = (
        clients_list.values("client_type")
        .annotate(count=Count("id"))
        .order_by("client_type")
    )

    # Calcul réel des interactions par mois (12 derniers mois)
    interactions_by_month = []
    for i in range(12):
        month_start = now - timedelta(days=30 * (12 - i))
        month_end = month_start + timedelta(days=30)
        count = ClientInteraction.objects.filter(
            interaction_date__gte=month_start,
            interaction_date__lt=month_end
        ).count()
        interactions_by_month.append(count)

    # Préparation des données JSON pour l'interface CRM (sérialisables)
    crm_clients_data = []
    now_date = now.date()

    for client in clients_list.prefetch_related("interactions"):
        # Conversion du type interne vers un libellé lisible
        client_type_label = dict(Client.CLIENT_TYPE_CHOICES).get(client.client_type, "Individuel")

        # Conversion du statut interne vers un libellé utilisé dans le front
        status_map = {
            Client.STATUS_ACTIVE: "Actif",
            Client.STATUS_INACTIVE: "Inactif",
        }
        status_label = status_map.get(client.status, "Actif")

        # Nombre de mois depuis la dernière activité (approximation, suffisant pour les KPIs)
        if client.last_activity_date:
            months_since_last = (now_date.year - client.last_activity_date.year) * 12 + (
                now_date.month - client.last_activity_date.month
            )
            if months_since_last < 0:
                months_since_last = 0
        else:
            months_since_last = 0

        # On utilise le score de fidélité (1-5) comme "satisfaction" pour la maquette CRM
        satisfaction_5_pts = client.loyalty_score or 3

        # Historique d'interactions sous forme de texte
        interactions_history = [
            f"{inter.interaction_date.date().isoformat()} · {inter.get_interaction_type_display()} · {inter.subject}"
            for inter in client.interactions.all()[:10]
        ]

        crm_clients_data.append(
            {
                "id": client.id,
                "nom": client.name,
                "type": client_type_label,
                "email": client.email,
                "telephone": client.phone,
                "statut": status_label,
                "satisfaction": satisfaction_5_pts,
                "commandes": client.total_orders,
                "ventes": client.total_spent,
                "derniereActiviteMois": months_since_last,
                "interactions": interactions_history,
                # La maquette prévoit des factures et des messages ; on laisse vide pour l'instant
                "factures": [],
                "messages": [],
            }
        )

    context = {
        # Liste déjà sérialisable pour l'utilisation avec le filtre `json_script`
        "crm_clients": crm_clients_data,
        "total_clients": total_clients,
        "active_clients": active_clients,
        "avg_satisfaction": round(avg_satisfaction, 1),
        "avg_loyalty": round(avg_loyalty, 1),
        "total_interactions": total_interactions,
        "monthly_growth": monthly_growth,
        "type_distribution": type_distribution,
        "interactions_by_month": interactions_by_month,
    }
    return render(request, "pgi/clients.html", context)


def client_create(request):
    """Créer un nouveau client (formulaire simple)."""
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client « {client.name} » créé avec succès.")
            return redirect("clients:clients")
    else:
        form = ClientForm()

    return render(request, "pgi/client_form.html", {"form": form})


def client_interaction_create(request, client_id=None):
    """Ajouter une interaction liée à un client."""
    initial = {}
    client = None
    if client_id is not None:
        client = get_object_or_404(Client, id=client_id)
        initial["client"] = client

    if request.method == "POST":
        form = ClientInteractionForm(request.POST, initial=initial)
        if form.is_valid():
            interaction = form.save(commit=False)
            # Pré-remplir le nom d'utilisateur si non saisi
            if not interaction.user_name and request.user.is_authenticated:
                interaction.user_name = request.user.get_full_name() or request.user.username
            interaction.save()
            messages.success(request, "Interaction client enregistrée avec succès.")
            return redirect("clients:clients")
    else:
        form = ClientInteractionForm(initial=initial)

    return render(
        request,
        "pgi/client_interaction_form.html",
        {
            "form": form,
            "client": client,
        },
    )


@login_required
def cart_view(request):
    """Afficher le panier d'achats."""
    try:
        client = Client.objects.get(email=request.user.email)
        cart, created = Cart.objects.get_or_create(client=client)
        cart_items = cart.items.all().select_related("product")
        
        # Utiliser les propriétés du modèle Cart pour les calculs
        context = {
            "cart": cart,
            "cart_items": cart_items,
            "subtotal": cart.subtotal,
            "tps": cart.tps,
            "tvq": cart.tvq,
            "total": cart.total,
        }
        return render(request, "pgi/cart.html", context)
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé. Veuillez vous inscrire.")
        return redirect("pgi:register")


@login_required
def add_to_cart(request, product_id):
    """Ajouter un produit au panier."""
    product = get_object_or_404(Product, id=product_id, status=Product.STATUS_ACTIVE)
    quantity = int(request.POST.get("quantity", 1))
    
    try:
        client = Client.objects.get(email=request.user.email)
        cart, created = Cart.objects.get_or_create(client=client)
        
        # Vérifier le stock
        if quantity > product.quantity_in_stock:
            messages.error(request, f"Stock insuffisant. Disponible: {product.quantity_in_stock}")
            return redirect("stocks:product_detail", product_id=product_id)
        
        # Ajouter ou mettre à jour l'article
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "unit_price": product.sale_price}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.quantity_in_stock:
                cart_item.quantity = product.quantity_in_stock
            cart_item.save()
        
        messages.success(request, f"{product.name} ajouté au panier.")
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé. Veuillez vous inscrire.")
        return redirect("pgi:register")
    
    return redirect("stocks:product_detail", product_id=product_id)


@login_required
def remove_from_cart(request, item_id):
    """Retirer un produit du panier."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    # Vérifier que l'article appartient au client connecté
    try:
        client = Client.objects.get(email=request.user.email)
        if cart_item.cart.client != client:
            messages.error(request, "Vous n'avez pas accès à cet article.")
            return redirect("clients:cart")
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé.")
        return redirect("pgi:login")
    
    cart_item.delete()
    messages.success(request, "Produit retiré du panier.")
    return redirect("clients:cart")


@login_required
def update_cart_item(request, item_id):
    """Modifier la quantité d'un article dans le panier."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    # Vérifier que l'article appartient au client connecté
    try:
        client = Client.objects.get(email=request.user.email)
        if cart_item.cart.client != client:
            messages.error(request, "Vous n'avez pas accès à cet article.")
            return redirect("clients:cart")
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé.")
        return redirect("pgi:login")
    
    quantity = int(request.POST.get("quantity", 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Produit retiré du panier.")
    elif quantity > cart_item.product.quantity_in_stock:
        messages.error(request, f"Stock insuffisant. Disponible: {cart_item.product.quantity_in_stock}")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Quantité mise à jour.")
    
    return redirect("clients:cart")


@login_required
def checkout(request):
    """Processus de commande - créer une commande depuis le panier."""
    try:
        client = Client.objects.get(email=request.user.email)
        cart, created = Cart.objects.get_or_create(client=client)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            messages.error(request, "Votre panier est vide.")
            return redirect("clients:cart")
        
        # Vérifier le stock pour tous les articles
        for item in cart_items:
            if item.quantity > item.product.quantity_in_stock:
                messages.error(
                    request, 
                    f"Stock insuffisant pour {item.product.name}. Disponible: {item.product.quantity_in_stock}"
                )
                return redirect("clients:cart")
        
        # Créer la commande
        from datetime import date, timedelta
        from finances.models import Invoice, InvoiceLineItem
        
        order = ClientOrder.objects.create(
            client=client,
            order_number=f"CMD-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            order_date=date.today(),
            total_amount=cart.total,
            status=ClientOrder.STATUS_RECEIVED,
        )
        
        # Créer les lignes de commande
        for item in cart_items:
            OrderLineItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        
        # Créer automatiquement une facture (règle d'affaires TP#2)
        invoice = Invoice.objects.create(
            invoice_number=f"FAC-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            client=client,
            amount=cart.subtotal,
            invoice_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            status=Invoice.STATUS_PENDING,
        )
        
        # Créer les lignes de facture
        for item in cart_items:
            InvoiceLineItem.objects.create(
                invoice=invoice,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        
        # Vider le panier
        cart.items.all().delete()
        
        # Mettre à jour le nombre de commandes du client
        client.total_orders += 1
        client.total_spent += order.total_amount
        client.save()
        
        messages.success(request, f"Commande #{order.order_number} créée avec succès!")
        return redirect("clients:my_orders")
        
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé.")
        return redirect("pgi:login")


@login_required
def my_orders(request):
    """Historique des commandes du client connecté."""
    try:
        client = Client.objects.get(email=request.user.email)
        orders = ClientOrder.objects.filter(client=client).order_by("-order_date")
        
        context = {
            "orders": orders,
            "client": client,
        }
        return render(request, "pgi/my_orders.html", context)
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé.")
        return redirect("pgi:login")


@login_required
def rate_order(request, order_id):
    """Évaluation de satisfaction client (1 à 5 étoiles) après un achat."""
    order = get_object_or_404(ClientOrder, id=order_id)
    
    # Vérifier que la commande appartient au client connecté
    try:
        client = Client.objects.get(email=request.user.email)
        if order.client != client:
            messages.error(request, "Vous n'avez pas accès à cette commande.")
            return redirect("clients:my_orders")
    except Client.DoesNotExist:
        messages.error(request, "Client non trouvé.")
        return redirect("pgi:login")
    
    # Vérifier si une évaluation existe déjà
    if hasattr(order, 'rating'):
        messages.info(request, "Vous avez déjà évalué cette commande.")
        return redirect("clients:my_orders")
    
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        comment = request.POST.get("comment", "")
        
        if 1 <= rating <= 5:
            OrderRating.objects.create(
                order=order,
                rating=rating,
                comment=comment,
            )
            messages.success(request, "Merci pour votre évaluation!")
            return redirect("clients:my_orders")
        else:
            messages.error(request, "La note doit être entre 1 et 5 étoiles.")
    
    context = {
        "order": order,
    }
    return render(request, "pgi/rate_order.html", context)


def is_staff_or_superuser(user):
    """Vérifie si l'utilisateur est staff ou superuser (employé/admin)."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_staff_or_superuser)
def client_activity_history(request, client_id):
    """Historique horodaté des actions d'un client - Zone restreinte employés uniquement."""
    client = get_object_or_404(Client, id=client_id)
    activities = ClientActivityLog.objects.filter(client=client).order_by("-created_at")
    
    context = {
        "client": client,
        "activities": activities,
    }
    return render(request, "pgi/client_activity_history.html", context)
