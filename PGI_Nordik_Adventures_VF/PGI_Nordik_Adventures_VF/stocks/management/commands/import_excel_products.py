"""
Commande Django pour importer les produits depuis le fichier Excel
Usage: python manage.py import_excel_products
"""
import os
import sys
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime
from decimal import Decimal

from stocks.models import Product, ProductCategory, Supplier


class Command(BaseCommand):
    help = "Importe les produits depuis le fichier Excel 'NordikAdventures - Liste des produits PGI (1).xlsx'"

    def add_arguments(self, parser):
        parser.add_argument(
            '--excel-file',
            type=str,
            default='NordikAdventures - Liste des produits PGI (1).xlsx',
            help='Chemin vers le fichier Excel (par défaut: à la racine du projet)',
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Met à jour les produits existants au lieu de les ignorer',
        )

    def handle(self, *args, **options):
        try:
            import openpyxl
        except ImportError:
            self.stdout.write(
                self.style.ERROR(
                    "Erreur: openpyxl n'est pas installé.\n"
                    "Installez-le avec: pip install openpyxl"
                )
            )
            return

        # Chemin vers le fichier Excel
        excel_file = options['excel_file']
        if not os.path.isabs(excel_file):
            # Chemin relatif depuis la racine du projet
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            excel_file = os.path.join(base_dir, excel_file)

        if not os.path.exists(excel_file):
            self.stdout.write(
                self.style.ERROR(f"Fichier non trouvé: {excel_file}")
            )
            return

        self.stdout.write(f"Lecture du fichier: {excel_file}")

        # Charger le fichier Excel
        try:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erreur lors de la lecture du fichier: {e}")
            )
            return

        # Lire les en-têtes
        headers = []
        for col in range(1, sheet.max_column + 1):
            cell_value = sheet.cell(row=1, column=col).value
            if cell_value:
                headers.append(str(cell_value).strip())

        self.stdout.write(f"Colonnes trouvées: {', '.join(headers)}")
        self.stdout.write(f"Nombre de lignes de données: {sheet.max_row - 1}")

        # Mapping flexible basé sur des mots-clés dans les en-têtes
        def find_column_index(headers, keywords):
            """Trouve l'index d'une colonne en cherchant des mots-clés dans les en-têtes."""
            for idx, header in enumerate(headers, start=1):
                header_lower = header.lower()
                if all(keyword.lower() in header_lower for keyword in keywords):
                    return idx
            return None

        # Créer un dictionnaire d'index de colonnes
        col_indices = {}
        col_indices['sku'] = find_column_index(headers, ['SKU'])
        col_indices['category'] = find_column_index(headers, ['Catégorie'])
        col_indices['name'] = find_column_index(headers, ['Nom', 'produit'])
        col_indices['purchase_cost'] = find_column_index(headers, ['Coût', 'achat'])
        col_indices['sale_price'] = find_column_index(headers, ['Prix', 'vente'])
        col_indices['gross_margin_percent'] = find_column_index(headers, ['Marge', 'brute'])
        col_indices['quantity_in_stock'] = find_column_index(headers, ['Quantité', 'stock'])
        col_indices['reorder_threshold'] = find_column_index(headers, ['Seuil', 'réapprovisionnement'])
        col_indices['safety_stock'] = find_column_index(headers, ['Stock', 'minimum', 'sécurité'])
        col_indices['delivery_delay'] = find_column_index(headers, ['Délai', 'livraison'])
        col_indices['supplier_name'] = find_column_index(headers, ['Fournisseur'])
        col_indices['supplier_code'] = find_column_index(headers, ['Code', 'fournisseur'])
        col_indices['supplier_discount'] = find_column_index(headers, ['Remise', 'fournisseur'])
        col_indices['weight_kg'] = find_column_index(headers, ['Poids'])
        col_indices['stock_entry_date'] = find_column_index(headers, ['Date', 'entrée', 'stock'])
        col_indices['warehouse_location'] = find_column_index(headers, ['Emplacement', 'entrepôt'])
        col_indices['status'] = find_column_index(headers, ['Statut', 'produit'])
        
        # Afficher les colonnes trouvées
        for field, idx in col_indices.items():
            if idx:
                self.stdout.write(f"  {field}: colonne {idx} ({headers[idx-1]})")
            else:
                self.stdout.write(self.style.WARNING(f"  {field}: NON TROUVÉ"))

        # Vérifier que les colonnes essentielles sont présentes
        required_cols = ['sku', 'category', 'name', 'purchase_cost', 'sale_price', 'supplier_name', 'supplier_code']
        missing_cols = [col for col in required_cols if col not in col_indices]
        if missing_cols:
            self.stdout.write(
                self.style.ERROR(f"Colonnes manquantes: {', '.join(missing_cols)}")
            )
            return

        # Traitement des lignes
        created_products = 0
        updated_products = 0
        skipped_products = 0
        errors = []

        with transaction.atomic():
            for row_idx in range(2, sheet.max_row + 1):
                try:
                    # Lire les valeurs de la ligne
                    row_data = {}
                    for field, col_idx in col_indices.items():
                        cell_value = sheet.cell(row=row_idx, column=col_idx).value
                        row_data[field] = cell_value

                    # Ignorer les lignes vides
                    if not row_data.get('sku'):
                        continue

                    # Traitement des données
                    sku = str(row_data['sku']).strip()
                    category_name = str(row_data['category']).strip()
                    product_name = str(row_data['name']).strip()
                    
                    # Conversion des valeurs numériques
                    purchase_cost = Decimal(str(row_data.get('purchase_cost', 0)))
                    sale_price = Decimal(str(row_data.get('sale_price', 0)))
                    gross_margin_raw = row_data.get('gross_margin_percent', 0)
                    # Convertir la marge brute: si < 1, c'est une décimale (0.515), sinon c'est un pourcentage (51.5)
                    if isinstance(gross_margin_raw, (int, float)):
                        if gross_margin_raw < 1:
                            # C'est une décimale, convertir en pourcentage
                            gross_margin = Decimal(str(gross_margin_raw * 100)).quantize(Decimal('0.01'))
                        else:
                            gross_margin = Decimal(str(gross_margin_raw)).quantize(Decimal('0.01'))
                    else:
                        gross_margin = Decimal(str(gross_margin_raw)).quantize(Decimal('0.01'))
                    quantity = int(row_data.get('quantity_in_stock', 0) or 0)
                    reorder_threshold = int(row_data.get('reorder_threshold', 0) or 0)
                    safety_stock = int(row_data.get('safety_stock', 0) or 0)
                    delivery_delay = int(row_data.get('delivery_delay', 0) or 0)
                    supplier_discount = Decimal(str(row_data.get('supplier_discount', 0) or 0))
                    weight_kg = Decimal(str(row_data.get('weight_kg', 0) or 0))
                    warehouse_location = str(row_data.get('warehouse_location', '')).strip()
                    
                    # Traitement de la date
                    stock_entry_date = row_data.get('stock_entry_date')
                    if isinstance(stock_entry_date, datetime):
                        stock_entry_date = stock_entry_date.date()
                    elif isinstance(stock_entry_date, str):
                        try:
                            stock_entry_date = datetime.strptime(stock_entry_date, '%Y-%m-%d').date()
                        except:
                            stock_entry_date = datetime.now().date()
                    else:
                        stock_entry_date = datetime.now().date()
                    
                    # Statut
                    status_str = str(row_data.get('status', 'Actif')).strip().lower()
                    if 'actif' in status_str:
                        status = Product.STATUS_ACTIVE
                    else:
                        status = Product.STATUS_INACTIVE
                    
                    # Fournisseur
                    supplier_name = str(row_data['supplier_name']).strip()
                    supplier_code = str(row_data['supplier_code']).strip()

                    # Créer ou récupérer la catégorie
                    category, _ = ProductCategory.objects.get_or_create(
                        name=category_name,
                        defaults={'description': f'Catégorie: {category_name}'}
                    )

                    # Créer ou récupérer le fournisseur
                    supplier, _ = Supplier.objects.get_or_create(
                        code=supplier_code,
                        defaults={
                            'name': supplier_name,
                            'default_discount': supplier_discount,
                            'delivery_delay_days': delivery_delay,
                        }
                    )
                    # Mettre à jour le fournisseur si nécessaire
                    if options['update']:
                        supplier.name = supplier_name
                        supplier.default_discount = supplier_discount
                        supplier.delivery_delay_days = delivery_delay
                        supplier.save()

                    # Créer ou mettre à jour le produit
                    product, created = Product.objects.get_or_create(
                        sku=sku,
                        defaults={
                            'category': category,
                            'name': product_name,
                            'purchase_cost': purchase_cost,
                            'sale_price': sale_price,
                            'gross_margin_percent': gross_margin,
                            'quantity_in_stock': quantity,
                            'reorder_threshold': reorder_threshold,
                            'safety_stock': safety_stock,
                            'supplier': supplier,
                            'supplier_discount': supplier_discount,
                            'weight_kg': weight_kg,
                            'stock_entry_date': stock_entry_date,
                            'warehouse_location': warehouse_location,
                            'status': status,
                        }
                    )

                    if created:
                        created_products += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ Créé: {sku} - {product_name}")
                        )
                    elif options['update']:
                        # Mettre à jour le produit existant
                        product.category = category
                        product.name = product_name
                        product.purchase_cost = purchase_cost
                        product.sale_price = sale_price
                        product.gross_margin_percent = gross_margin
                        product.quantity_in_stock = quantity
                        product.reorder_threshold = reorder_threshold
                        product.safety_stock = safety_stock
                        product.supplier = supplier
                        product.supplier_discount = supplier_discount
                        product.weight_kg = weight_kg
                        product.stock_entry_date = stock_entry_date
                        product.warehouse_location = warehouse_location
                        product.status = status
                        product.save()
                        updated_products += 1
                        self.stdout.write(
                            self.style.WARNING(f"↻ Mis à jour: {sku} - {product_name}")
                        )
                    else:
                        skipped_products += 1
                        self.stdout.write(
                            f"⊘ Ignoré (existe déjà): {sku} - {product_name}"
                        )

                except Exception as e:
                    error_msg = f"Erreur ligne {row_idx}: {str(e)}"
                    errors.append(error_msg)
                    self.stdout.write(
                        self.style.ERROR(f"✗ {error_msg}")
                    )

        # Résumé
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("RÉSUMÉ DE L'IMPORT"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"Produits créés: {created_products}")
        if options['update']:
            self.stdout.write(f"Produits mis à jour: {updated_products}")
        self.stdout.write(f"Produits ignorés: {skipped_products}")
        if errors:
            self.stdout.write(self.style.ERROR(f"Erreurs: {len(errors)}"))
            for error in errors:
                self.stdout.write(self.style.ERROR(f"  - {error}"))
        self.stdout.write("=" * 60)

