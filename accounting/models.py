"""
Modèles de données pour l'application de comptabilité.
Définit la structure des comptes, transactions et entrées de journal.
"""
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """
    Modèle représentant un compte comptable.
    Peut être de type Actif, Passif, Produit ou Charge.
    """
    ACCOUNT_TYPES = [
        ('ACTIF', 'Actif'),
        ('PASSIF', 'Passif'),
        ('PRODUIT', 'Produit'),
        ('CHARGE', 'Charge'),
    ]

    # Champs du modèle
    name = models.CharField(max_length=255, verbose_name="Intitulé du compte")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code du compte")
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, verbose_name="Type du compte")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Solde actuel")

    def __str__(self):
        return f"{self.code} - {self.name}"

class Transaction(models.Model):
    """
    Modèle représentant une transaction comptable.
    Chaque transaction implique un compte débité et un compte crédité.
    """
    date = models.DateField(verbose_name="Date de l'opération")
    description = models.CharField(max_length=255, verbose_name="Libellé de l'opération")
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', 
                                    on_delete=models.CASCADE, verbose_name="Compte débité")
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', 
                                     on_delete=models.CASCADE, verbose_name="Compte crédité")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant de l'opération")

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour ajouter des validations :
        - Empêche d'avoir le même compte en débit et crédit
        - Vérifie que le montant est positif
        """
        if self.debit_account == self.credit_account:
            raise ValueError("Le compte débité et le compte crédité ne peuvent pas être les mêmes.")
        if self.amount <= 0:
            raise ValueError("Le montant doit être positif.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.description}"

class JournalEntry(models.Model):
    """
    Modèle représentant une entrée dans le journal comptable.
    Enregistre qui a effectué quelle transaction et quand.
    """
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name="Transaction")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur ayant effectué l'opération")

    def __str__(self):
        return f"{self.created_at} - {self.transaction.description}"