from django.db import models


class Category(models.Model):
    category_name = models.TextField()
    description = models.TextField()

class Transaction(models.Model):
    amount = models.FloatField()
    log_date = models.DateField()
    description = models.TextField(1)
    note = models.TextField(null=True)
    cycle = models.ForeignKey(
        'cycle.Cycle',
        on_delete=models.PROTECT,
        null=False,
    ),
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        null=False,
        default=1
    )

