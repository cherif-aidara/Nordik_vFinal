from django.contrib import admin
from .models import ProductCategory, Supplier, Product, StockMovement


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "default_discount", "delivery_delay_days")
    search_fields = ("code", "name")
    list_filter = ("default_discount",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "sale_price",
        "quantity_in_stock",
        "status",
        "supplier",
    )
    list_filter = ("status", "category", "supplier")
    search_fields = ("sku", "name", "description")
    readonly_fields = ("created_at", "updated_at", "total_stock_value", "is_below_reorder")
    fieldsets = (
        ("Informations générales", {
            "fields": ("sku", "name", "description", "category", "image", "status")
        }),
        ("Prix et coûts", {
            "fields": ("purchase_cost", "sale_price", "gross_margin_percent", "supplier_discount")
        }),
        ("Stock", {
            "fields": ("quantity_in_stock", "reorder_threshold", "safety_stock", "stock_entry_date", "warehouse_location")
        }),
        ("Fournisseur", {
            "fields": ("supplier",)
        }),
        ("Informations techniques", {
            "fields": ("weight_kg",)
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at")
        }),
        ("Propriétés calculées", {
            "fields": ("total_stock_value", "is_below_reorder")
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__sku", "product__name", "reference")
    readonly_fields = ("created_at", "updated_at")
