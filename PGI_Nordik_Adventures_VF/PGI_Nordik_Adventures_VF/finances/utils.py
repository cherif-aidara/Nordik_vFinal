"""
Fonctions utilitaires pour le module finances.
Utilisées par le tableau de bord et autres vues.
"""
from collections import defaultdict
from decimal import Decimal
from .models import Invoice, Expense, CashFlow


def get_finance_statistics():
    """Retourne les statistiques financières pour le tableau de bord."""
    invoices = Invoice.objects.all()
    expenses = Expense.objects.all()
    
    total_revenue = sum(
        inv.total_amount for inv in invoices 
        if inv.status == Invoice.STATUS_PAID
    )
    total_expenses = sum(
        exp.amount for exp in expenses 
        if exp.status == Expense.STATUS_PAID
    )
    net_balance = total_revenue - total_expenses
    unpaid_invoices_count = invoices.filter(
        status__in=[Invoice.STATUS_PENDING, Invoice.STATUS_OVERDUE]
    ).count()
    
    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "unpaid_invoices_count": unpaid_invoices_count,
    }


