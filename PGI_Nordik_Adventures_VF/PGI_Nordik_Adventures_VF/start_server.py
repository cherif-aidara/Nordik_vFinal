#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script pour démarrer le serveur Django"""
import os
import sys
import subprocess

# Chemin du projet (utiliser le répertoire actuel)
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

print(f"Répertoire de travail: {project_dir}")
print("Vérification des migrations...")

# Vérifier les migrations
result = subprocess.run([sys.executable, "manage.py", "makemigrations"], 
                       capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)

# Appliquer les migrations
print("\nApplication des migrations...")
result = subprocess.run([sys.executable, "manage.py", "migrate"], 
                       capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)

# Lancer le serveur
print("\nDémarrage du serveur Django sur http://127.0.0.1:8000/")
print("Appuyez sur Ctrl+C pour arrêter le serveur\n")
os.execv(sys.executable, [sys.executable, "manage.py", "runserver"])



