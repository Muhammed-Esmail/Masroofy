from django.test import TestCase
from insights.services.InsightsEngine import InsightsEngine
from insights.services.PieMaker import PieMaker
from insights.services.DonutMaker import DonutMaker
from insights.services.GraphMaker import GraphMaker

class MockCategory:
    '''
    Simulates a Django Category model.
    '''
    def __init__(self, name):
        self.name = name

class MockTransaction:
    '''
    Simulates a Django Transaction model.
    '''
    def __init__(self, amount, category_name, date):
        self.amount = amount
        self.date = date
        if category_name:
            self.category = MockCategory(category_name)
        else:
            self.category = None

class InsightsServicesTests(TestCase):
    
    def setUp(self):
        '''
        Setup runs before every single test. 
        We create a standard set of mock transactions to reuse.
        Total spent here is 250.0.
        '''
        self.transactions = [
            MockTransaction(amount=50.0, category_name="Food", date="2023-10-01"),
            MockTransaction(amount=50.0, category_name="Food", date="2023-10-01"),
            MockTransaction(amount=100.0, category_name="Transport", date="2023-10-02"),
            MockTransaction(amount=50.0, category_name=None, date="2023-10-02"), # Tests the "Other" fallback
        ]

    # PieMaker Tests
    
    def test_piemaker_generates_correct_percentages(self):
        maker = PieMaker()
        result = maker.generate(self.transactions)
        
        # Expected totals: Food=100, Transport=100, Other=50. Total = 250.
        # Expected percentages: Food=40.0%, Transport=40.0%, Other=20.0%
        self.assertEqual(result["categories"], ["Food", "Transport", "Other"])
        self.assertEqual(result["percentages"], [40.0, 40.0, 20.0])

    def test_piemaker_handles_zero_total(self):
        '''
        Tests the edge case where the total spent is 0 (prevents ZeroDivisionError).
        '''
        maker = PieMaker()
        zero_transactions = [MockTransaction(amount=0.0, category_name="Food", date="2023-10-01")]
        result = maker.generate(zero_transactions)
        
        self.assertEqual(result["categories"], [])
        self.assertEqual(result["percentages"], [])

    # DonutMaker Tests 
    
    def test_donutmaker_generates_correct_data(self):
        maker = DonutMaker()
        result = maker.generate(self.transactions)
        
        # DonutMaker should return everything PieMaker does, PLUS total_spent
        self.assertEqual(result["total_spent"], 250.0)
        self.assertEqual(result["categories"], ["Food", "Transport", "Other"])
        self.assertEqual(result["percentages"], [40.0, 40.0, 20.0])

    # GraphMaker Tests
    
    def test_graphmaker_aggregates_by_date(self):
        maker = GraphMaker()
        result = maker.generate(self.transactions)
        
        # Expected aggregation:
        # "2023-10-01": 50 + 50 = 100
        # "2023-10-02": 100 + 50 = 150
        expected_result = [
            {"date": "2023-10-01", "amount": 100.0},
            {"date": "2023-10-02", "amount": 150.0},
        ]
        
        self.assertEqual(result, expected_result)

    # InsightsEngine Tests

    def test_insightsengine_valid_charts(self):
        engine = InsightsEngine()
        
        # Test routing to PieMaker
        pie_result = engine.generate_chart("pie", self.transactions)
        self.assertIn("categories", pie_result)
        self.assertIn("percentages", pie_result)
        self.assertNotIn("total_spent", pie_result)
        
        # Test routing to DonutMaker (case-insensitive due to .lower() in Engine)
        donut_result = engine.generate_chart("DONUT", self.transactions)
        self.assertIn("total_spent", donut_result)
        
        # Test routing to GraphMaker
        graph_result = engine.generate_chart("graph", self.transactions)
        self.assertTrue(isinstance(graph_result, list)) # GraphMaker returns a list, not a dict

    def test_insightsengine_invalid_chart(self):
        engine = InsightsEngine()
        
        # Assert that passing an unknown chart type raises a ValueError
        with self.assertRaises(ValueError) as context:
            engine.generate_chart("scatter_plot", self.transactions)
            
        self.assertEqual(str(context.exception), "Chart type 'scatter_plot' is not supported.")
