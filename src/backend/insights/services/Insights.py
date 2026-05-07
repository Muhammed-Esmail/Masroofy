from abc import ABC, abstractmethod

class Insights(ABC):
    @abstractmethod
    def generate(self, transactions, amount):
        '''
        ## abstract method to generate chart data from a list of transactions

        ### parameters 
        - transactions: A list of transactions

        ### returns
        -  The data for the chart you chose.
        '''
        pass