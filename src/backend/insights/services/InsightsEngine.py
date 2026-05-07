from .PieMaker import PieMaker
from .DonutMaker import DonutMaker
from .GraphMaker import GraphMaker
from typing import Optional

class InsightsEngine:
    def __init__(self):
        self._makers = {
            "pie": PieMaker,
            "donut": DonutMaker,
            "graph": GraphMaker,
        }

    def generate_chart(self, chart_type: str, transactions, amount):
        '''
        ## Finds the right maker and generates the chart data.
        
        ### Parameters
        - chart_type: 
        - transactions:
        - amount : amount of money available in cycle

        ### returns
        - a dictionary depending on the type of chart.
    
        '''
        MakerClass = self._makers.get(chart_type.lower())
        
        if not MakerClass:
            raise ValueError(f"Chart type '{chart_type}' is not supported.")
            
        maker_instance = MakerClass()
        return maker_instance.generate(transactions, amount)


# Engine start—no problem!
# Five minute—tidin tidin tidin tidin...
# Problem!
# Engine kaput!