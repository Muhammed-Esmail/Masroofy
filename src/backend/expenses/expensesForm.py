from django import forms
from .models import PeriodicExpense

class PeriodicExpenseForm(forms.ModelForm):
    """
    A form for creating and updating PeriodicExpense instances.

    This form handles dynamic frequency logic, allowing users to select specific
    days of the week for weekly expenses or specific dates for monthly expenses.
    It performs conditional validation to ensure the appropriate days are selected
    based on the chosen frequency.

    Attributes:
        DAYS_CHOICES (list): Mapping of abbreviated days to human-readable labels.
        MONTH_DAYS_CHOICES (list): Numeric options from 1 to 31 for monthly dates.
        weekly_days_input (MultipleChoiceField): UI checkboxes for selecting weekdays.
        monthly_days_input (MultipleChoiceField): UI checkboxes for selecting month dates.
    """
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
        """
        Validates that the required day inputs are provided based on the frequency.

        If frequency is 'MONTHLY', monthly_days_input must not be empty.
        If frequency is 'WEEKLY', weekly_days_input must not be empty.

        Returns:
            dict: The cleaned data dictionary.
        """
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
        """
        Maps the virtual input fields to the model's actual fields before saving.

        This method transforms the list data from the MultipleChoiceFields into 
        the format expected by the PeriodicExpense model (e.g., converting 
        string dates to integers) and clears irrelevant data for the 
        non-selected frequency.

        Args:
            commit (bool): If True, saves the instance to the database.

        Returns:
            PeriodicExpense: The saved model instance.
        """
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