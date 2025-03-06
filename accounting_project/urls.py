"""
Configuration des URLs pour le projet accounting_project.

Ce fichier définit les routes principales de l'application, notamment :
- L'interface d'administration
- Les API REST
- La documentation Swagger/OpenAPI
- L'export de la balance
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounting.views import export_balance

# Configuration de la vue Swagger pour la documentation de l'API
schema_view = get_schema_view(
    openapi.Info(
        title="API de Comptabilité",
        default_version='v1',
        description="API pour la gestion de la comptabilité",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@votredomaine.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Définition des URLs de l'application
urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Routes de l'API comptable
    path('api/', include('accounting.urls')),
    
    # Documentation de l'API (format Swagger)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Documentation de l'API (format ReDoc)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Export de la balance comptable
    path('export-balance/', export_balance, name='export_balance'),
]