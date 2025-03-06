"""
Tests unitaires pour l'application accounting.
Teste les modèles, les vues et les fonctionnalités de l'application.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account, Transaction, JournalEntry
from decimal import Decimal

class AccountTests(TestCase):
    """Tests pour le modèle Account"""
    
    def setUp(self):
        """Initialisation des données de test"""
        self.account = Account.objects.create(
            name="Banque",
            code="512000",
            type="ACTIF",
            balance=0.0
        )

    def test_account_creation(self):
        """Teste la création d'un compte"""
        self.assertEqual(self.account.name, "Banque")
        self.assertEqual(self.account.code, "512000")
        self.assertEqual(self.account.type, "ACTIF")
        self.assertEqual(self.account.balance, 0.0)

class TransactionTests(TestCase):
    """Tests pour le modèle Transaction"""

    def setUp(self):
        """Initialisation des données de test"""
        self.account1 = Account.objects.create(
            name="Banque",
            code="512000",
            type="ACTIF"
        )
        self.account2 = Account.objects.create(
            name="Caisse",
            code="531000",
            type="ACTIF"
        )

    def test_transaction_creation(self):
        """Teste la création d'une transaction"""
        transaction = Transaction.objects.create(
            date="2024-03-15",
            description="Test transaction",
            debit_account=self.account1,
            credit_account=self.account2,
            amount=100.00
        )
        self.assertEqual(transaction.amount, Decimal('100.00'))
