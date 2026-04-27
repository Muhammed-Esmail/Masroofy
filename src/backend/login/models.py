from django.db import models

# Create your models here.
class UserModel(models.Model):
    password = models.TextField(max_length=100)
    name = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    current_cycle_id = models.ForeignKey(
        'cycle.CycleModel',
        on_delete=models.PROTECT,
        null=False
    )

    class Meta:
        db_table='User'