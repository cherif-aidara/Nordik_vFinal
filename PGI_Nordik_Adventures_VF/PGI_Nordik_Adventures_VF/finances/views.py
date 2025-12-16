from collections import defaultdict
from decimal import Decimal
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from stocks.utils import get_stock_statistics

from .models import Invoice, Expense, CashFlow, InvoiceLineItem
from .forms import InvoiceForm, ExpenseForm


def finances(request):
    """Module Finances & Facturation."""
    invoices = Invoice.objects.all()
    expenses = Expense.objects.all()

    # Chiffres issus des vraies factures / dépenses
    total_revenue = sum(
        inv.total_amount for inv in invoices if inv.status == Invoice.STATUS_PAID
    )
    total_expenses = sum(
        exp.amount for exp in expenses if exp.status == Expense.STATUS_PAID
    )
    net_balance = total_revenue - total_expenses
    unpaid_invoices = invoices.filter(
        status__in=[Invoice.STATUS_PENDING, Invoice.STATUS_OVERDUE]
    ).count()

    # Chiffres issus de l'inventaire produits (CA potentiel, profit, etc.)
    stock_stats = get_stock_statistics()
    potential_revenue = stock_stats["potential_revenue"]
    total_stock_value = stock_stats["total_stock_value"]
    potential_profit = stock_stats["potential_profit"]

    # Taux fixes utilisés dans tout le projet
    tps_rate = Decimal("0.05")
    tvq_rate = Decimal("0.09975")
    potential_revenue_ttc = (
        potential_revenue * (Decimal("1") + tps_rate + tvq_rate)
    ).quantize(Decimal("0.01"))

    # Séries mensuelles et par catégorie basées sur l'inventaire
    finance_month_labels = stock_stats["chart_month_labels"]
    finance_month_revenues = stock_stats["chart_month_revenues"]
    # On utilise la marge comme "coût" approximatif dans le graphique
    finance_month_costs = stock_stats["chart_month_margins"]
    finance_cat_labels = stock_stats["chart_cat_labels"]
    finance_cat_values = stock_stats["chart_cat_values"]

    # Petits payloads sérialisables pour le JS de la page finances
    invoice_summaries = [
        {
            "id": inv.id,
            "client_name": inv.client_name,
            "amount": float(inv.amount),
            "invoice_date": inv.invoice_date.isoformat() if inv.invoice_date else "",
            "status": inv.status,
        }
        for inv in invoices
    ]
    expense_summaries = [
        {
            "id": exp.id,
            "supplier_name": exp.supplier_name,
            "expense_type": exp.expense_type,
            "amount": float(exp.amount),
            "expense_date": exp.expense_date.isoformat() if exp.expense_date else "",
            "status": exp.status,
        }
        for exp in expenses
    ]

    context = {
        # Flux réels
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "unpaid_invoices": unpaid_invoices,
        "invoices": invoices[:10],
        "expenses": expenses[:10],
        "invoice_summaries": invoice_summaries,
        "expense_summaries": expense_summaries,
        # Inventaire (CA potentiel / profit)
        "potential_revenue": potential_revenue,
        "potential_revenue_ttc": potential_revenue_ttc,
        "potential_profit": potential_profit,
        "total_stock_value": total_stock_value,
        "tps_rate": tps_rate * 100,
        "tvq_rate": tvq_rate * 100,
        # Données pour les graphiques
        "finance_month_labels": finance_month_labels,
        "finance_month_revenues": finance_month_revenues,
        "finance_month_costs": finance_month_costs,
        "finance_cat_labels": finance_cat_labels,
        "finance_cat_values": finance_cat_values,
    }
    return render(request, "pgi/finances.html", context)


def finances_factures(request):
    """Vue détaillée des factures clients."""
    invoices = Invoice.objects.all().order_by("-invoice_date")
    context = {"invoices": invoices}
    return render(request, "pgi/finances_factures.html", context)


def finances_achats(request):
    """Vue détaillée des achats & dépenses."""
    expenses = Expense.objects.all().order_by("-expense_date")
    context = {"expenses": expenses}
    return render(request, "pgi/finances_achats.html", context)


def finances_tresorerie(request):
    """Vue détaillée des flux de trésorerie."""
    cash_flows = CashFlow.objects.all().order_by("-flow_date")
    context = {"cash_flows": cash_flows}
    return render(request, "pgi/finances_tresorerie.html", context)


def invoice_detail(request, invoice_id):
    """Génération d'un sommaire de facture détaillée (HTML)."""
    invoice = get_object_or_404(
        Invoice.objects.select_related("client"),
        id=invoice_id
    )
    line_items = invoice.line_items.all().select_related("product")
    
    context = {
        "invoice": invoice,
        "line_items": line_items,
    }
    return render(request, "pgi/invoice_detail.html", context)


def invoice_create(request):
    """Création manuelle d'une facture (bouton 'Nouvelle facture')."""
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f"Facture {invoice.invoice_number} créée.")
            return redirect("finances:finances_factures")
    else:
        form = InvoiceForm()

    return render(request, "pgi/finance_invoice_form.html", {"form": form})


def expense_create(request):
    """Création d'une dépense / achat (bouton 'Nouvel achat')."""
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            messages.success(
                request, f"Dépense {expense.amount} $ pour {expense.supplier_name} créée."
            )
            return redirect("finances:finances_achats")
    else:
        form = ExpenseForm()

    return render(request, "pgi/finance_expense_form.html", {"form": form})


def invoice_update(request, invoice_id):
    """Modification d'une facture existante."""
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f"Facture {invoice.invoice_number} mise à jour.")
            return redirect("finances:finances_factures")
    else:
        form = InvoiceForm(instance=invoice)

    return render(
        request,
        "pgi/finance_invoice_form.html",
        {"form": form, "invoice": invoice, "is_edit": True},
    )


def invoice_delete(request, invoice_id):
    """Suppression d'une facture (avec page de confirmation)."""
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == "POST":
        num = invoice.invoice_number
        invoice.delete()
        messages.success(request, f"Facture {num} supprimée.")
        return redirect("finances:finances_factures")

    return render(request, "pgi/finance_invoice_confirm_delete.html", {"invoice": invoice})


def invoice_pdf(request, invoice_id):
    """Téléchargement d'une facture en PDF (résumé simple)."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    invoice = get_object_or_404(Invoice, id=invoice_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, 750, "Nordik Adventures - Facture client")

    p.setFont("Helvetica", 11)
    p.drawString(40, 720, f"Facture #: {invoice.invoice_number}")
    p.drawString(40, 705, f"Client   : {invoice.client_name}")
    p.drawString(40, 690, f"Email    : {invoice.client_email}")
    p.drawString(40, 675, f"Date     : {invoice.invoice_date or ''}")
    p.drawString(40, 660, f"Échéance : {invoice.due_date or ''}")

    # Montants
    y = 630
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Récapitulatif")
    p.setFont("Helvetica", 11)

    y -= 20
    p.drawString(40, y, f"Sous-total HT : {invoice.amount} $")
    y -= 15
    p.drawString(40, y, f"TPS (5%)      : {invoice.tps} $")
    y -= 15
    p.drawString(40, y, f"TVQ (9.975%) : {invoice.tvq} $")
    y -= 15
    p.drawString(40, y, f"Total TTC     : {invoice.total_amount} $")

    # Notes
    if invoice.notes:
        y -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "Notes :")
        y -= 15
        p.setFont("Helvetica", 11)
        for line in str(invoice.notes).splitlines():
            p.drawString(40, y, line)
            y -= 14

    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"facture_{invoice.invoice_number or invoice.id}.pdf"
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename=\"{filename}\"'
    return response


def export_invoices_csv(request):
    """Export CSV des factures (bouton 'Ventes CSV')."""
    invoices = Invoice.objects.all().order_by("invoice_date")

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="factures_nordik.csv"'

    header = "Numero,Date,Client,Email,MontantHT,TPS,TVQ,TotalTTC,Statut\n"
    response.write(header)
    for inv in invoices:
        line = (
            f"{inv.invoice_number},"
            f"{inv.invoice_date or ''},"
            f"\"{inv.client_name}\","
            f"{inv.client_email},"
            f"{inv.amount},"
            f"{inv.tps},"
            f"{inv.tvq},"
            f"{inv.total_amount},"
            f"{inv.status}\n"
        )
        response.write(line)

    return response


def export_monthly_report_csv(request):
    """Export CSV d'un petit rapport mensuel (bouton 'Rapport mensuel')."""
    invoices = Invoice.objects.all()
    expenses = Expense.objects.all()

    month_buckets = defaultdict(lambda: {"revenue": Decimal("0"), "cost": Decimal("0")})
    for inv in invoices:
        if inv.invoice_date:
            key = inv.invoice_date.strftime("%Y-%m")
            month_buckets[key]["revenue"] += inv.total_amount
    for exp in expenses:
        if exp.expense_date:
            key = exp.expense_date.strftime("%Y-%m")
            month_buckets[key]["cost"] += exp.amount

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="rapport_mensuel_nordik.csv"'

    response.write("Mois,RevenusTTC,Depenses,Profit\n")
    for month in sorted(month_buckets.keys()):
        revenue = month_buckets[month]["revenue"]
        cost = month_buckets[month]["cost"]
        profit = revenue - cost
        response.write(f"{month},{revenue},{cost},{profit}\n")

    return response
