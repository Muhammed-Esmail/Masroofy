from django import forms
from .models import PeriodicExpense

class PeriodicExpenseForm(forms.ModelForm):
    DAYS_CHOICES = [
        ('SUN', 'Sunday'), ('MON', 'Monday'), ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')
    ]
    MONTH_DAYS_CHOICES = [(i, str(i)) for i in range(1, 32)]

    weekly_days_input = forms.MultipleChoiceField(
        choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False
    )
    
    monthly_days_input = forms.MultipleChoiceField(
        choices=MONTH_DAYS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = PeriodicExpense
        fields = ['name', 'amount', 'frequency'] 

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')
        monthly_days = cleaned_data.get('monthly_days_input')
        weekly_days = cleaned_data.get('weekly_days_input')

        if frequency == 'MONTHLY' and not monthly_days:
            self.add_error('monthly_days_input', 'Select at least one day of the month.')
        
        if frequency == 'WEEKLY' and not weekly_days:
            self.add_error('weekly_days_input', 'Select at least one day for weekly expenses.')
            
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if instance.frequency == 'MONTHLY':
            instance.days_of_month = [int(day) for day in self.cleaned_data.get('monthly_days_input', [])]
            instance.days_of_week = []
            
        elif instance.frequency == 'WEEKLY':
            instance.days_of_week = self.cleaned_data.get('weekly_days_input', [])
            instance.days_of_month = [] 
            
        if commit:
            instance.save()
        return instance