from django import forms
from .models import SettingsModel

class SettingsForm(forms.ModelForm):
    class Meta: 
        model = SettingsModel
        fields = ['currency','language', 'theme']


