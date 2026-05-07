from .Insights import Insights

class GraphMaker(Insights):
    """
    A specialized insight engine for generating time-series data visualizations.

    GraphMaker processes transaction records to aggregate spending on a daily basis, 
    formatting the results into a structure easily consumable by charting components.
    """

    def generate(self, transactions, amount) -> list[dict[str, any]]:
        """
        Transforms a list of transactions into an aggregated daily spending report.

        This method iterates through all provided transactions, sums the amounts 
        for each unique date, and returns a list of dictionaries sorted by the 
        occurrence in the input.

        Args:
            transactions (list[Transaction]): A collection of transaction objects 
                containing 'date' and 'amount' attributes.

        Returns:
            list[dict[str, Any]]: A list of data points, where each dictionary 
            contains:
                - "date" (str): The ISO string representation of the date.
                - "amount" (float): The total sum spent on that specific date.
        """
        daily_totals = {}
        for t in transactions:
            # Aggregate totals by date string key
            date_str = str(t.log_date)
            daily_totals[date_str] = daily_totals.get(date_str, 0.0) + float(t.amount)
            
        return [
            {"date": date, "amount": amount}
            for date, amount in daily_totals.items()
        ]