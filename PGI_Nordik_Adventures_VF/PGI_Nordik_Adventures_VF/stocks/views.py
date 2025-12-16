from collections import defaultdict
from django.db.models import Sum, Count, F, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Supplier, ProductCategory, StockMovement
from .forms import ProductForm


def stock_list(request):
    """Vue de gestion des stocks (liste + recherche rapide)."""
    qs = Product.objects.select_related("category", "supplier")

    # Recherche serveur (SKU, nom, fournisseur) pour la barre de recherche
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(sku__icontains=query)
            | Q(name__icontains=query)
            | Q(supplier__name__icontains=query)
        )

    products = list(qs)

    total_value = sum(p.total_stock_value for p in products)
    low_stock = [p for p in products if p.is_below_reorder]
    suppliers_count = Supplier.objects.aggregate(count=Count("id"))["count"] or 0
    categories = (
        qs.values("category__name")
        .annotate(total_qty=Sum("quantity_in_stock"))
        .order_by("category__name")
    )
    suppliers = Supplier.objects.all()

    context = {
        "products": products,
        "total_value": total_value,
        "low_stock_count": len(low_stock),
        "suppliers_count": suppliers_count,
        "categories": categories,
        "low_stock_products": low_stock,
        "suppliers": suppliers,
        "search_query": query,
    }
    return render(request, "pgi/stocks.html", context)


def catalogue(request):
    """Catalogue produits public - accessible sans authentification."""
    # Filtrer uniquement les produits actifs
    products = Product.objects.filter(
        status=Product.STATUS_ACTIVE
    ).select_related("category", "supplier").order_by("name")
    
    # Récupérer les catégories pour filtrage
    categories = ProductCategory.objects.all()
    
    # Filtrage par catégorie si demandé
    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Recherche par nom si demandé
    search_query = request.GET.get("search", "")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(sku__icontains=search_query)
        )
    
    context = {
        "products": products,
        "categories": categories,
        "selected_category": int(category_id) if category_id else None,
        "search_query": search_query,
    }
    return render(request, "pgi/catalogue.html", context)


def product_detail(request, product_id):
    """Fiche produit détaillée avec toutes les informations."""
    product = get_object_or_404(
        Product.objects.select_related("category", "supplier"),
        id=product_id,
        status=Product.STATUS_ACTIVE
    )
    
    # Récupérer les produits similaires (même catégorie)
    similar_products = Product.objects.filter(
        category=product.category,
        status=Product.STATUS_ACTIVE
    ).exclude(id=product_id)[:4]
    
    context = {
        "product": product,
        "similar_products": similar_products,
        "is_below_reorder": product.is_below_reorder,
    }
    return render(request, "pgi/product_detail.html", context)


def product_create(request):
    """Création d'un nouveau produit de stock via un formulaire simple."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request,
                f"Le produit {product.sku} - {product.name} a été ajouté au stock.",
            )
            return redirect("stocks:stock_list")
    else:
        form = ProductForm()

    return render(request, "pgi/product_form.html", {"form": form})

