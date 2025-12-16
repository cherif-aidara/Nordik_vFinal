"""
Script pour exporter la base de données SQLite en fichier SQL
Usage: python export_database.py
"""
import sqlite3
import os
from django.conf import settings
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def export_database():
    """Exporte la base de données SQLite en fichier SQL."""
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    output_path = os.path.join(os.path.dirname(__file__), 'database.sql')
    
    if not os.path.exists(db_path):
        print(f"Erreur: La base de données {db_path} n'existe pas.")
        print("Veuillez d'abord exécuter 'python manage.py migrate' pour créer la base de données.")
        return
    
    conn = sqlite3.connect(db_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Écrire l'en-tête
        f.write("-- ===========================================\n")
        f.write("-- EXPORT BASE DE DONNÉES NORDIK ADVENTURES\n")
        f.write("-- TP#3 - INF23307\n")
        f.write("-- ===========================================\n\n")
        f.write("-- Ce fichier contient la structure et les données de la base de données SQLite\n")
        f.write("-- Pour l'importer dans MySQL/PostgreSQL, vous devrez adapter les types de données\n\n")
        
        # Itérer sur toutes les tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Ignorer les tables système SQLite
            if table_name.startswith('sqlite_'):
                continue
            
            f.write(f"\n-- ===========================================\n")
            f.write(f"-- Table: {table_name}\n")
            f.write(f"-- ===========================================\n\n")
            
            # Obtenir la structure de la table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # Créer la commande CREATE TABLE
            f.write(f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n")
            column_defs = []
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] else ""
                default = f"DEFAULT {col[4]}" if col[4] is not None else ""
                pk = "PRIMARY KEY" if col[5] else ""
                
                # Adapter les types SQLite pour MySQL/PostgreSQL
                if col_type.upper() == 'INTEGER':
                    col_type = 'INTEGER'
                elif col_type.upper() == 'TEXT':
                    col_type = 'TEXT'
                elif col_type.upper() == 'REAL':
                    col_type = 'DECIMAL(10,2)'
                elif col_type.upper() == 'BLOB':
                    col_type = 'BLOB'
                
                parts = [f"`{col_name}`", col_type]
                if pk:
                    parts.append(pk)
                if not_null:
                    parts.append(not_null)
                if default:
                    parts.append(default)
                
                column_defs.append(" ".join(parts))
            
            f.write("  " + ",\n  ".join(column_defs) + "\n")
            f.write(");\n\n")
            
            # Exporter les données
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if rows:
                f.write(f"-- Données pour la table {table_name}\n")
                f.write(f"INSERT INTO `{table_name}` VALUES\n")
                
                row_strings = []
                for row in rows:
                    # Convertir les valeurs en chaînes SQL
                    values = []
                    for i, val in enumerate(row):
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, bytes):
                            values.append(f"X'{val.hex()}'")
                        else:
                            # Échapper les apostrophes
                            val_str = str(val).replace("'", "''")
                            values.append(f"'{val_str}'")
                    
                    row_strings.append(f"({', '.join(values)})")
                
                f.write(",\n".join(row_strings) + ";\n\n")
            else:
                f.write(f"-- Aucune donnée dans la table {table_name}\n\n")
    
    conn.close()
    print(f"✓ Export terminé: {output_path}")
    print(f"  {len(tables)} tables exportées")

if __name__ == '__main__':
    export_database()

