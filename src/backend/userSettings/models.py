from django.db import models

# Create your models here.
class SettingsModel(models.Model):
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

    language = models.TextField(choices=languageChoices, default=languageChoices.ENGLISH)
    currency = models.TextField(choices=currencyChoices, default=currencyChoices.US_DOLLAR)
    theme = models.TextField(choices=themeChoices, default=themeChoices.LIGHT)

    class Meta:
        db_table='Settings'