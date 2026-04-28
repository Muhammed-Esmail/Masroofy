from django.test import TestCase
from history.services import *
from backend.shared_classes import *
from datetime import date

class CategoryCRUDTest(TestCase):
    def setUp(self):
        self.crud = CategoryCRUD()
        self.sample_category = Category(
            id=None,
            name="Clothing",
            description="Clothes Category"
        )

    def test_create(self):
        result = self.crud.create(self.sample_category)
        self.assertTrue(result)

    def test_fetchById(self):
        self.crud.create(self.sample_category)
        category = self.crud.fetchById(1)
        self.assertEqual(category.name, "Clothing")
        self.assertEqual(category.description, "Clothes Category")

    def test_update(self):
        self.crud.create(self.sample_category)
        updated = Category(id=None, name="Food", description="Food Category")
        self.crud.update(1, updated)
        category = self.crud.fetchById(1)
        self.assertEqual(category.name, "Food")

    def test_delete(self):
        self.crud.create(self.sample_category)
        self.crud.delete(1)
        with self.assertRaises(Exception):
            self.crud.fetchById(1)

class CycleCRUDTest(TestCase):
    def setUp(self):
        self.crud = CycleCRUD()
        self.sample_cycle = Cycle(
            id=None,
            startDate=date(2024, 1, 1),
            endDate=date(2024, 1, 31),
            amount=500
        )

    def test_create(self):
        result = self.crud.create(self.sample_cycle)
        self.assertTrue(result)

    def test_fetchById(self):
        self.crud.create(self.sample_cycle)
        cycle = self.crud.fetchById(1)
        self.assertEqual(cycle.amount, 500)
        self.assertEqual(cycle.startDate, date(2024, 1, 1))

    def test_update(self):
        self.crud.create(self.sample_cycle)
        updated = Cycle(id=1, startDate=date(2024, 1, 1), endDate=date(2024, 2, 28), amount=1000)
        self.crud.update(1, updated)
        cycle = self.crud.fetchById(1)
        self.assertEqual(cycle.amount, 1000)

    def test_delete(self):
        self.crud.create(self.sample_cycle)
        self.crud.delete(1)
        with self.assertRaises(Exception):
            self.crud.fetchById(1)

class TransactionCRUDTest(TestCase):
    def setUp(self):
        self.trans_crud = TransactionCRUD()
        self.cycle_crud = CycleCRUD()
        self.category_crud = CategoryCRUD()

        self.sample_cycle = Cycle(
            id=None,
            startDate=date(2024, 1, 1),
            endDate=date(2024, 1, 31),
            amount=500
        )

        self.sample_category = Category(
            id=None,
            name="Clothing",
            description="Clothes Category"
        )

        self.sample_transaction = Transaction(
            id=None,
            amount=100,
            cycle_id=1,
            category_id=1,
            log_date=date(2006,6,6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )

        self.cycle_crud.create(self.sample_cycle)
        self.category_crud.create(self.sample_category)

    def test_create(self):        
        result = self.trans_crud.create(self.sample_transaction)
        self.assertTrue(result)

    def test_fetchById(self):
        self.trans_crud.create(self.sample_transaction)
        transaction = self.trans_crud.fetchById(1)
        self.assertEqual(transaction.amount, 100)

    def test_fetchByFilters(self):
        self.trans_crud.create(self.sample_transaction)
        transaction_1 = self.trans_crud.fetchByFilters(category_id=1)
        transaction_2 = self.trans_crud.fetchByFilters(startDate=date(1999,7,7))
        self.assertTrue(transaction_1[0].amount, 100)
        self.assertTrue(transaction_2[0].amount, 100)

    def test_update(self):
        self.trans_crud.create(self.sample_transaction)
        updated = Transaction(
            id=None,
            amount=1000,
            cycle_id=1,
            category_id=1,
            log_date=date(2006,6,6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )

        self.trans_crud.update(1, updated)
        transaction = self.trans_crud.fetchById(1)
        self.assertEqual(transaction.amount, 1000)

    def test_delete(self):
        self.trans_crud.create(self.sample_transaction)
        self.trans_crud.delete(1)
        with self.assertRaises(Exception):
            self.trans_crud.fetchById(1)


class HistoryManagerTest(TestCase):
    def setUp(self):
        self.hist = HistoryManager()
        self.cycle_crud = CycleCRUD()
        self.category_crud = CategoryCRUD()
        self.trans_crud = TransactionCRUD()

        self.cycle_crud.create(Cycle(
            id=None,
            startDate=date(2024, 1, 1),
            endDate=date(2024, 1, 31),
            amount=500
        ))

        self.category_crud.create(Category(
            id=None,
            name="Clothing",
            description="Clothes Category"
        ))

        self.trans_crud.create(Transaction(
            id=None,
            amount=100,
            cycle_id=1,
            category_id=1,
            log_date=date(2024, 1, 15),
            description="Test transaction",
            note=None
        ))

    def test_fetchCycleData(self):
        cycle = self.hist.fetchCycleData(1)
        self.assertEqual(cycle.amount, 500)
        self.assertEqual(cycle.startDate, date(2024, 1, 1))

    def test_fetchTransactionData(self):
        results = self.hist.fetchTransactionData(
            startDate=date(2024, 1, 1),
            endDate=date(2024, 1, 31),
            category_id=1
        )
        self.assertEqual(results[0].amount, 100)

    def test_fetchFullHistory(self):
        results = self.hist.fetchFullHistory()
        self.assertEqual(results[0].description, "Test transaction")