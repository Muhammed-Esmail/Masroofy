from django.db import models

class CategoryModel(models.Model):
    category_name = models.TextField()
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
    category_id = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_DEFAULT,
        null=False,
        default=1
    )

    class Meta:
        db_table = 'Transaction'