from django.contrib import admin
from .models import Invoice, Expense, CashFlow, InvoiceLineItem


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "client",
        "client_name",
        "total_amount",
        "invoice_date",
        "due_date",
        "status",
    )
    list_filter = ("status", "invoice_date")
    search_fields = ("invoice_number", "client__name", "client_name", "client_email")
    readonly_fields = ("created_at", "updated_at", "tps", "tvq", "total_amount")
    date_hierarchy = "invoice_date"


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "supplier_name",
        "expense_type",
        "amount",
        "expense_date",
        "status",
    )
    list_filter = ("expense_type", "status", "expense_date")
    search_fields = ("supplier_name", "reference")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "expense_date"


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ("flow_type", "amount", "description", "flow_date")
    list_filter = ("flow_type", "flow_date")
    search_fields = ("description",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "flow_date"


@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "quantity", "unit_price", "line_total")
    list_filter = ("invoice__status", "invoice__invoice_date")
    search_fields = ("invoice__invoice_number", "product__name", "product__sku")
    readonly_fields = ("created_at", "updated_at", "line_total")
