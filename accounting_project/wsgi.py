"""
Configuration WSGI pour le projet accounting_project.
Permet le déploiement de l'application sur un serveur web compatible WSGI.
"""

# Importation des modules nécessaires
import os
from django.core.wsgi import get_wsgi_application

# Définition du module de paramètres Django à utiliser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_project.settings')

# Création de l'application WSGI
application = get_wsgi_application()
