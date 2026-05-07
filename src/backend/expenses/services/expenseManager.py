from expenses.models import PeriodicExpense

class ExpenseManager:
    def getAllExpenses(self):
        '''
        Fetches all recurring expenses for the user.
        '''
        return list(PeriodicExpense.objects.all())
    
    # I refine and add the rest of the functionality here later.