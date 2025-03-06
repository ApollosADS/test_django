"""
Configuration des URLs pour l'application accounting.
Définit les routes pour accéder aux différentes vues de l'application.
"""

# Imports nécessaires
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Création du routeur pour les vues basées sur ViewSet
router = DefaultRouter()

# Enregistrement des routes pour les comptes et les transactions
router.register(r'accounts', views.AccountViewSet)
router.register(r'transactions', views.TransactionViewSet)

# Liste des URLs de l'application
urlpatterns = [
    # Inclusion des routes automatiques du routeur
    path('', include(router.urls)),
]