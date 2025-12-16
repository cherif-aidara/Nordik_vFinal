"""
Fonctions utilitaires pour le module clients.
Utilisées par le tableau de bord et autres vues.
"""
from django.db.models import Count, Avg
from .models import Client, ClientInteraction, ClientOrder


def get_client_statistics():
    """Retourne les statistiques clients pour le tableau de bord."""
    clients_list = Client.objects.all()
    
    total_clients = clients_list.count()
    active_clients = clients_list.filter(status=Client.STATUS_ACTIVE).count()
    avg_satisfaction = clients_list.aggregate(avg=Avg("satisfaction_score"))["avg"] or 0
    avg_loyalty = clients_list.aggregate(avg=Avg("loyalty_score"))["avg"] or 0
    total_interactions = ClientInteraction.objects.count()
    total_orders = ClientOrder.objects.count()
    
    return {
        "total_clients": total_clients,
        "active_clients": active_clients,
        "avg_satisfaction": round(avg_satisfaction, 1),
        "avg_loyalty": round(avg_loyalty, 1),
        "total_interactions": total_interactions,
        "total_orders": total_orders,
    }


