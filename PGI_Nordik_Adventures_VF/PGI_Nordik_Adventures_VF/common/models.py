"""
Modèles communs partagés entre les applications.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """Abstraction de base avec dates de création/mise à jour.
    
    Cette classe abstraite peut être utilisée par tous les modèles
    qui nécessitent des timestamps automatiques.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        abstract = True


