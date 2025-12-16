===========================================
NORDIK ADVENTURES - SYSTÈME PGI
TP#3 - INF23307
Django Web Application
===========================================

INSTRUCTIONS D'INSTALLATION
============================

1. PRÉREQUIS
-----------
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel, pour cloner le projet)

2. INSTALLATION DES DÉPENDANCES
-------------------------------
a) Ouvrez un terminal/console dans le dossier du projet
b) Créez un environnement virtuel (recommandé):
   Windows:
     python -m venv venv
     venv\Scripts\activate
   
   Linux/Mac:
     python3 -m venv venv
     source venv/bin/activate

c) Installez les dépendances:
   pip install -r requirements.txt

3. CONFIGURATION DE LA BASE DE DONNÉES
--------------------------------------
a) Le projet utilise SQLite par défaut (db.sqlite3)
b) Pour créer/mettre à jour la base de données:
   python manage.py migrate

c) (Optionnel) Créer un superutilisateur pour l'admin Django:
   python manage.py createsuperuser

4. IMPORTATION DES DONNÉES DE DÉMONSTRATION
--------------------------------------------
a) Importer des produits de démonstration:
   python manage.py import_demo_stock

b) (Optionnel) Exporter la base de données en SQL:
   python export_database.py

5. DÉMARRAGE DU SERVEUR
-----------------------
a) Dans le terminal, exécutez:
   python manage.py runserver

b) Ouvrez votre navigateur et allez à:
   http://127.0.0.1:8000/

c) Pour accéder à l'interface d'administration Django:
   http://127.0.0.1:8000/admin/

6. COMPTES DE TEST
------------------

Pour créer des comptes de test, utilisez l'interface d'inscription:
http://127.0.0.1:8000/register/

OU créez-les via le shell Django:
python manage.py shell

>>> from django.contrib.auth.models import User
>>> from clients.models import Client
>>> user = User.objects.create_user('admin', 'admin@nordik.local', 'Azerty123!')
>>> user.is_staff = True
>>> user.save()
>>> client = Client.objects.create(name='Admin', email='admin@nordik.local', status=Client.STATUS_ACTIVE)

7. STRUCTURE DU PROJET
----------------------
PGI_Nordik_Adventures_VF/
├── backend/              (Configuration Django)
│   ├── settings.py       (Paramètres du projet)
│   ├── urls.py           (URLs principales)
│   └── wsgi.py           (Interface WSGI)
├── pgi/                  (Application principale)
│   ├── views.py          (Vues: dashboard, login, register)
│   ├── urls.py           (URLs de l'app principale)
│   └── models.py         (Modèles communs)
├── stocks/               (Module Stocks)
│   ├── models.py         (Product, Supplier, StockMovement)
│   ├── views.py          (Vues: catalogue, product_detail)
│   └── urls.py           (URLs du module stocks)
├── finances/             (Module Finances)
│   ├── models.py         (Invoice, Expense, CashFlow)
│   ├── views.py          (Vues: finances, invoice_detail)
│   └── urls.py           (URLs du module finances)
├── clients/              (Module Clients)
│   ├── models.py         (Client, ClientOrder, Cart, etc.)
│   ├── views.py          (Vues: cart, checkout, my_orders)
│   ├── signals.py        (Signaux Django pour automatisation)
│   └── urls.py           (URLs du module clients)
├── templates/            (Templates HTML)
│   └── pgi/              (Templates de l'application)
├── static/               (Fichiers statiques: CSS, JS, images)
├── db.sqlite3            (Base de données SQLite)
├── manage.py             (Script de gestion Django)
├── requirements.txt      (Dépendances Python)
└── README.txt           (Ce fichier)

8. FONCTIONNALITÉS IMPLÉMENTÉES
-------------------------------
✓ Système d'authentification Django (inscription/connexion/déconnexion)
✓ Catalogue de produits public avec recherche et filtres par catégorie
✓ Fiche produit détaillée
✓ Panier d'achat fonctionnel (ajout, modification, suppression)
✓ Processus de commande (checkout)
✓ Calcul automatique des taxes (TPS 5%, TVQ 9.975%)
✓ Génération automatique de factures
✓ Historique des commandes client
✓ Évaluation de satisfaction client (1-5 étoiles)
✓ Gestion des stocks avec alertes de réapprovisionnement
✓ Interface d'administration Django complète
✓ Historique d'activités client (pour employés)
✓ Signaux Django pour automatisation des règles d'affaires

9. RÈGLES D'AFFAIRES IMPLÉMENTÉES
---------------------------------
- Validation SKU unique pour les produits
- Prix de vente > coût d'achat (validation)
- Vente → diminution automatique du stock
- Achat → augmentation automatique du stock
- Calcul automatique des taxes (TPS/TVQ)
- Changement automatique de statut client:
  * Prospect → Actif (première commande)
  * Actif → Fidèle (5 commandes OU 3000$ dépensés)
- Alertes de réapprovisionnement (stock ≤ seuil)
- Vérification du stock disponible avant vente
- Enregistrement automatique des mouvements de stock
- Création automatique de facture lors du checkout
- Création automatique d'activités client (logs)
- Message de bienvenue automatique (première commande)

10. URLS PRINCIPALES
--------------------
- /                          → Tableau de bord
- /login/                    → Connexion
- /register/                 → Inscription
- /logout/                   → Déconnexion
- /stocks/catalogue/         → Catalogue produits public
- /stocks/produit/<id>/      → Fiche produit
- /clients/panier/           → Panier d'achat
- /clients/commander/        → Checkout
- /clients/mes-commandes/    → Historique commandes
- /finances/factures/        → Liste des factures
- /finances/factures/<id>/   → Détails d'une facture
- /admin/                    → Interface d'administration Django

11. COMMANDES UTILES
--------------------
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver

# Accéder au shell Django
python manage.py shell

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Exporter la base de données en SQL
python export_database.py

12. NOTES IMPORTANTES
---------------------
- Le projet utilise SQLite par défaut (développement)
- Pour la production, configurez PostgreSQL ou MySQL dans settings.py
- Les mots de passe sont hashés avec Django (PBKDF2)
- Les sessions sont gérées par Django
- Protection CSRF activée par défaut
- Les requêtes utilisent l'ORM Django (protection contre SQL injection)
- Les signaux Django sont dans clients/signals.py
- Les templates utilisent le système de templates Django

13. DÉPANNAGE
-------------
Problème: "No module named django"
Solution: pip install -r requirements.txt

Problème: "Table doesn't exist"
Solution: python manage.py migrate

Problème: "Static files not found"
Solution: Vérifiez STATIC_URL et STATICFILES_DIRS dans settings.py

Problème: "CSRF verification failed"
Solution: Assurez-vous d'utiliser {% csrf_token %} dans les formulaires

14. SUPPORT
-----------
Pour toute question ou problème, contactez l'équipe de développement.

===========================================
© 2025 Nordik Adventures - TP#3 INF23307
Django Version
===========================================
