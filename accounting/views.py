"""
Vues de l'application de comptabilité.
Gère toute la logique métier et les réponses aux requêtes HTTP.
"""

# Imports nécessaires
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
import csv
from datetime import datetime

from .models import Account, Transaction, JournalEntry
from .serializers import AccountSerializer, TransactionSerializer, JournalEntrySerializer

class AccountViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les opérations CRUD sur les comptes.
    Permet de lister, créer, modifier et supprimer des comptes.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les opérations CRUD sur les transactions.
    Gère la création et la consultation des transactions comptables.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Surcharge de la création pour enregistrer l'entrée dans le journal.
        """
        # Sauvegarde de la transaction
        transaction = serializer.save()
        
        # Création de l'entrée de journal associée
        JournalEntry.objects.create(
            transaction=transaction,
            user=self.request.user
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def export_balance(request):
    """
    Vue pour exporter la balance des comptes au format CSV.
    Génère un fichier CSV avec le solde de tous les comptes.
    """
    # Création de la réponse HTTP avec l'en-tête pour le CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="balance_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    # Création du writer CSV
    writer = csv.writer(response)
    
    # En-têtes du fichier
    writer.writerow(['Code', 'Intitulé', 'Type', 'Solde'])
    
    # Écriture des données
    for account in Account.objects.all():
        writer.writerow([
            account.code,
            account.name,
            account.type,
            account.balance
        ])
    
    return response