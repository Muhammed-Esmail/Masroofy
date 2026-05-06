from django.db import models

class CategoryModel(models.Model):
    name = models.TextField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = 'Category'

class TransactionModel(models.Model):
    amount = models.FloatField()
    log_date = models.DateField()
    description = models.TextField()
    note = models.TextField(null=True)
    cycle = models.ForeignKey(
        'cycle.CycleModel',
        on_delete=models.PROTECT,
        null=False,
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        null=False,
        default='General',
        db_column='category_name',
    )

    class Meta:
        db_table = 'Transaction'