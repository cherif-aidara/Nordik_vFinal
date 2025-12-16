"""
Fonctions utilitaires pour le module stocks.
Utilisées par le tableau de bord et autres vues.
"""
from collections import defaultdict
from django.db.models import F, Count, Sum
from .models import Product, Supplier, ProductCategory


def get_stock_statistics():
    """Retourne les statistiques de stock pour le tableau de bord."""
    products = list(Product.objects.all())
    total_stock_value = sum(p.total_stock_value for p in products)
    total_products = len(products)
    total_suppliers = Supplier.objects.count()
    low_stock_count = (
        Product.objects.filter(quantity_in_stock__lte=F("reorder_threshold")).count()
        if Product.objects.exists()
        else 0
    )
    
    # Calcul du revenu potentiel basé sur l'inventaire
    potential_revenue = sum(p.sale_price * p.quantity_in_stock for p in products)
    potential_profit = potential_revenue - total_stock_value
    
    # Données pour les graphiques par mois
    month_buckets = defaultdict(lambda: {"revenue": 0, "margin": 0})
    for p in products:
        if not p.stock_entry_date:
            continue
        key = p.stock_entry_date.strftime("%Y-%m")
        month_buckets[key]["revenue"] += p.sale_price * p.quantity_in_stock
        month_buckets[key]["margin"] += (
            (p.sale_price - p.purchase_cost) * p.quantity_in_stock
        )
    
    sorted_month_keys = sorted(month_buckets.keys())
    chart_month_labels = [k for k in sorted_month_keys]
    chart_month_revenues = [month_buckets[k]["revenue"] for k in sorted_month_keys]
    chart_month_margins = [month_buckets[k]["margin"] for k in sorted_month_keys]
    
    # Valeur de stock par catégorie
    category_buckets = defaultdict(lambda: 0)
    for p in products:
        if p.category:
            category_buckets[p.category.name] += p.total_stock_value
    chart_cat_labels = list(category_buckets.keys())
    chart_cat_values = [category_buckets[name] for name in chart_cat_labels]
    
    return {
        "total_stock_value": total_stock_value,
        "total_products": total_products,
        "total_suppliers": total_suppliers,
        "low_stock_count": low_stock_count,
        "potential_revenue": potential_revenue,
        "potential_profit": potential_profit,
        "chart_month_labels": chart_month_labels,
        "chart_month_revenues": chart_month_revenues,
        "chart_month_margins": chart_month_margins,
        "chart_cat_labels": chart_cat_labels,
        "chart_cat_values": chart_cat_values,
    }


