from .Insights import Insights
from .PieMaker import PieMaker

class DonutMaker(Insights):
    def generate(self, transactions, amount):
        '''
        ## Processes transactions to generate donut chart data.
        
        ### Parameters
        - transactions: A list of Transaction objects to be processed.
        - amount: A float representing the total available money.

        ### returns
        - A dictionary containing a 'total_spent' float, a 'total_unspent' float,
          alongside two separate lists: 'categories' (the labels) and 'values' (the data).
        '''
        
        total_spent = round(sum(float(t.amount) for t in transactions), 2)
        total_unspent = max(0,round(amount - total_spent, 2))
        
        return {
            "total_unspent": total_unspent,
            "total_spent": total_spent,
            "categories": ["Unspent", "Spent"],
            "values": [total_unspent, total_spent]
        }