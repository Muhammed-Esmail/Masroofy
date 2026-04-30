from .Insights import Insights
from .PieMaker import PieMaker

class DonutMaker(Insights):
    def generate(self, transactions):
        '''
        ## Processes transactions to generate donut chart data.
        
        ### Parameters
        - transactions: A list of Transaction objects to be processed.

        ### returns
        - A dictionary containing a 'total_spent' float, alongside two separate lists: 'categories' (the labels) and 'percentages' (the data).
        '''
       
        # copy my homework but change it slightly
        pie_data = PieMaker().generate(transactions)
        
        total_spent = sum(float(t.amount) for t in transactions)
        
        return {
            "total_spent": round(total_spent, 2),
            "categories": pie_data["categories"],
            "percentages": pie_data["percentages"]
        }