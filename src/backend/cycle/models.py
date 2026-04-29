from django.db import models

class CycleModel(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    amount = models.FloatField()

    class Meta:
        db_table = 'Cycle'

class ActiveCycleModel(models.Model):
    cycle = models.OneToOneField(CycleModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'active_cycle'