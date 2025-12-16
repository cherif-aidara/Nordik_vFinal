from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
    path("", views.finances, name="finances"),
    path("factures/", views.finances_factures, name="finances_factures"),
    path("factures/nouvelle/", views.invoice_create, name="invoice_create"),
    path("factures/<int:invoice_id>/", views.invoice_detail, name="invoice_detail"),
    path("factures/<int:invoice_id>/modifier/", views.invoice_update, name="invoice_update"),
    path("factures/<int:invoice_id>/supprimer/", views.invoice_delete, name="invoice_delete"),
    path("factures/<int:invoice_id>/pdf/", views.invoice_pdf, name="invoice_pdf"),
    path("achats/", views.finances_achats, name="finances_achats"),
    path("achats/nouveau/", views.expense_create, name="expense_create"),
    path("tresorerie/", views.finances_tresorerie, name="finances_tresorerie"),
    path("export/factures.csv", views.export_invoices_csv, name="export_invoices_csv"),
    path("export/rapport-mensuel.csv", views.export_monthly_report_csv, name="export_monthly_report_csv"),
]
