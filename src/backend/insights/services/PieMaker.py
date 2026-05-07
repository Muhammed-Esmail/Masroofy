from .Insights import Insights

class PieMaker(Insights):
    def generate(self, transactions):
        '''
        ## Processes transactions to calculate spending percentages per category for a pie chart.
        
        ### Parameters
        - transactions: A list of Transaction objects to be processed.

        ### returns
        - A dictionary containing two separate lists: categories and percentages.
        '''
        total_spent = sum(float(t.amount) for t in transactions)
        
        if total_spent == 0:
            return {
                "categories": [], 
                "percentages": []
            }

        totals = {}
        for t in transactions:
            cat_name = t.category_name if t.category_name else "Other"
            totals[cat_name] = totals.get(cat_name, 0.0) + float(t.amount)
            
        categories_list = []
        percentages_list = []
        
        for cat_name, amount in totals.items():
            categories_list.append(cat_name)
            percentages_list.append(round((amount / total_spent) * 100, 2))
            
        return {
            "categories": categories_list,
            "percentages": percentages_list
        }