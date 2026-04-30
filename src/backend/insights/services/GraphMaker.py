from .Insights import Insights

class GraphMaker(Insights):
    def generate(self, transactions):
        daily_totals = {}
        for t in transactions:
            date_str = str(t.date)
            daily_totals[date_str] = daily_totals.get(date_str, 0.0) + float(t.amount)
            
        return [
            {"date": date, "amount": amount}
            for date, amount in daily_totals.items()
        ]