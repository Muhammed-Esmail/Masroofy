from django.db import models

# Create your models here.
class Settings(models.Model):
    class languageChoices(models.TextChoices):
        ENGLISH = "EN"
        ARABIC = "AR"
        ...

    class currencyChoices(models.TextChoices):
        US_DOLLAR = "$"
        EGYPTIAN_POUND = "EGP"
        ...

    class themeChoices(models.TextChoices):
        LIGHT = "Light Mode"
        DARK = "Dark Mode"

    language = models.TextField(choices=languageChoices)
    currency = models.TextField(choices=currencyChoices)
    theme = models.TextField(choices=themeChoices)

    cycle_duration = models.IntegerField(null=False)
    budget_threshold = models.FloatField(null=False)
