from django.db import models

class CycleModel(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    amount = models.FloatField()

    class Meta:
        db_table = 'Cycle'