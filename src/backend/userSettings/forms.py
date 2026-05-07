from django import forms
from .models import SettingsModel

class SettingsForm(forms.ModelForm):
    class Meta: 
        model = SettingsModel
        fields = ['currency', 'cycle_duration', 'budget_threshold', 'language', 'theme']


