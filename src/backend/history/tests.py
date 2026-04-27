from django.test import TestCase
from history.services import *
from backend.shared_classes import *
from datetime import date

class HistoryManagerTest(TestCase):
    ...

class CategoryCRUDTest(TestCase):
    ...

class TransactionCRUDTest(TestCase):
    def setUp(self):
        self.crud = TransactionCRUD()
        self.sample_transaction = Transaction(
            id=None,
            amount=100,
            category_id=1,
            log_date=date(2006,6,6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )

    def test_create(self):
        result = self.crud.create(self.sample_transaction)
        self.assertTrue(result)

    def test_fetchById(self):
        self.crud.create(self.sample_transaction)
        transaction = self.crud.fetchById(1)
        self.assertEqual(transaction.amount, 100)

    def test_fetchByFilters(self):
        self.crud.create(self.sample_transaction)
        transaction_1 = self.crud.fetchByFilters(category_id=1)
        # transaction_2 = self.crud.fetchByFilters(startDate=date(1111,1,1))
        self.assertTrue(transaction_1.amount, 100)

    def test_update(self):
        self.crud.create(self.sample_cycle)
        updated = Transaction(id=1, startDate=date(2024, 1, 1), endDate=date(2024, 2, 28), amount=1000)
        self.crud.update(1, updated)
        transaction = self.crud.fetchById(1)
        self.assertEqual(transaction.amount, 1000)

    def test_delete(self):
        self.crud.create(self.sample_transaction)
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