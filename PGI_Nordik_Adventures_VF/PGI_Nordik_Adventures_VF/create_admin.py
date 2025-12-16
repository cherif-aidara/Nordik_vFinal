"""
Script pour créer un superutilisateur Django pour l'administration.
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Configuration du superutilisateur
username = 'admin'
email = 'admin@nordik.local'
password = 'Azerty123!'

try:
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.save()
        print(f"✅ Mot de passe mis à jour pour le superutilisateur '{username}'")
    else:
        # Créer un nouveau superutilisateur
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superutilisateur '{username}' créé avec succès!")
    
    print(f"\n📋 Informations de connexion :")
    print(f"   URL: http://localhost:8000/admin/")
    print(f"   Nom d'utilisateur: {username}")
    print(f"   Email: {email}")
    print(f"   Mot de passe: {password}")
    print(f"\n⚠️  Note: Changez le mot de passe après la première connexion!")
    
except Exception as e:
    print(f"❌ Erreur lors de la création du superutilisateur: {e}")
    print("\n💡 Essayez d'exécuter les migrations d'abord:")
    print("   python manage.py migrate")

