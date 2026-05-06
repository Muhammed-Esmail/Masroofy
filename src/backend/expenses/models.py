from django.db import models

# Create your models here.

class PeriodicExpense(models.Model):
    class Frequency(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Specific Dates of the Month'
        WEEKLY = 'WEEKLY', 'Specific Days of the Week'

    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.MONTHLY)
    
    days_of_month = models.JSONField(
        null=True, blank=True,
        default=list,
    )
    
    days_of_week = models.JSONField(
        null=True, blank=True,
        default=list,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}(L.E.) ({self.get_frequency_display()})"