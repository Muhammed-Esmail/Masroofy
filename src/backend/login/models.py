from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    username = models.CharField(
        max_length=150, 
        unique=True, 
        default="user"
        )
    current_cycle = models.ForeignKey(
        'cycle.CycleModel',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    class Meta:
        db_table='User'
    def __str__(self):
        return self.name or self.username