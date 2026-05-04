from datetime import date
from django.test import TestCase

from backend.shared_classes import Transaction
from transaction.models import TransactionModel, CategoryModel
from cycle.models import CycleModel
from transaction.services.TransactionManager import TransactionManager
from history.services import TransactionCRUD


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_manager() -> TransactionManager:
    """Returns a fresh (non-singleton) TransactionManager with real TransactionCRUD."""
    TransactionCRUD._instance = None
    manager = TransactionManager.__new__(TransactionManager)
    manager._transCRUD = TransactionCRUD()
    return manager


def make_db_cycle() -> CycleModel:
    return CycleModel.objects.create(
        startDate=date(2024, 1, 1),
        endDate=date(2024, 1, 31),
        amount=1000,
    )


def make_db_category() -> CategoryModel:
    return CategoryModel.objects.create(
        category_name="Food",
        description="Food expenses",
    )


def make_transaction(cycle: CycleModel, category: CategoryModel, amount=100, note=None) -> Transaction:
    return Transaction(
        id=None,
        amount=amount,
        cycle_id=cycle.id,
        category_id=category.id,
        log_date=date(2024, 1, 15),
        description="Test transaction",
        note=note,
    )


def log_and_fetch(manager: TransactionManager, transaction: Transaction) -> TransactionModel:
    """Logs a transaction and returns the resulting DB row."""
    manager.logTransaction(transaction)
    return TransactionModel.objects.latest('id')


# ── logTransaction ─────────────────────────────────────────────────────────────

class LogTransactionTests(TestCase):

    def setUp(self):
        self.cycle = make_db_cycle()
        self.category = make_db_category()
        self.manager = make_manager()

    def test_creates_row_in_db(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category))

        self.assertEqual(TransactionModel.objects.count(), 1)

    def test_persists_correct_amount(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category, amount=250))

        row = TransactionModel.objects.first()
        self.assertEqual(row.amount, 250)

    def test_persists_correct_cycle(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category))

        row = TransactionModel.objects.first()
        self.assertEqual(row.cycle_id, self.cycle.id)

    def test_persists_correct_category(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category))

        row = TransactionModel.objects.first()
        self.assertEqual(row.category_id, self.category.id)

    def test_persists_correct_log_date(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category))

        row = TransactionModel.objects.first()
        self.assertEqual(row.log_date, date(2024, 1, 15))

    def test_persists_correct_description(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category))

        row = TransactionModel.objects.first()
        self.assertEqual(row.description, "Test transaction")

    def test_persists_note_when_provided(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category, note="Some note"))

        row = TransactionModel.objects.first()
        self.assertEqual(row.note, "Some note")

    def test_persists_null_note(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category, note=None))

        row = TransactionModel.objects.first()
        self.assertIsNone(row.note)

    def test_multiple_transactions_all_persisted(self):
        self.manager.logTransaction(make_transaction(self.cycle, self.category, amount=100))
        self.manager.logTransaction(make_transaction(self.cycle, self.category, amount=200))
        self.manager.logTransaction(make_transaction(self.cycle, self.category, amount=300))

        self.assertEqual(TransactionModel.objects.count(), 3)


# ── updateTransaction ──────────────────────────────────────────────────────────

class UpdateTransactionTests(TestCase):

    def setUp(self):
        self.cycle = make_db_cycle()
        self.category = make_db_category()
        self.manager = make_manager()

    def test_updates_amount_in_db(self):
        row = log_and_fetch(self.manager, make_transaction(self.cycle, self.category, amount=100))

        updated = Transaction(
            id=row.id,
            amount=999,
            cycle_id=self.cycle.id,
            category_id=self.category.id,
            log_date=date(2024, 1, 15),
            description="Test transaction",
            note=None,
        )
        self.manager.updateTransaction(updated)

        row.refresh_from_db()
        self.assertEqual(row.amount, 999)

    def test_updates_description_in_db(self):
        row = log_and_fetch(self.manager, make_transaction(self.cycle, self.category))

        updated = Transaction(
            id=row.id,
            amount=100,
            cycle_id=self.cycle.id,
            category_id=self.category.id,
            log_date=date(2024, 1, 15),
            description="Updated description",
            note=None,
        )
        self.manager.updateTransaction(updated)

        row.refresh_from_db()
        self.assertEqual(row.description, "Updated description")

    def test_updates_note_in_db(self):
        row = log_and_fetch(self.manager, make_transaction(self.cycle, self.category, note=None))

        updated = Transaction(
            id=row.id,
            amount=100,
            cycle_id=self.cycle.id,
            category_id=self.category.id,
            log_date=date(2024, 1, 15),
            description="Test transaction",
            note="Added note",
        )
        self.manager.updateTransaction(updated)

        row.refresh_from_db()
        self.assertEqual(row.note, "Added note")

    def test_does_not_affect_other_transactions(self):
        row1 = log_and_fetch(self.manager, make_transaction(self.cycle, self.category, amount=100))
        row2 = log_and_fetch(self.manager, make_transaction(self.cycle, self.category, amount=200))

        updated = Transaction(
            id=row1.id,
            amount=999,
            cycle_id=self.cycle.id,
            category_id=self.category.id,
            log_date=date(2024, 1, 15),
            description="Test transaction",
            note=None,
        )
        self.manager.updateTransaction(updated)

        row2.refresh_from_db()
        self.assertEqual(row2.amount, 200)


# ── deleteTransaction ──────────────────────────────────────────────────────────

class DeleteTransactionTests(TestCase):

    def setUp(self):
        self.cycle = make_db_cycle()
        self.category = make_db_category()
        self.manager = make_manager()

    def test_removes_row_from_db(self):
        row = log_and_fetch(self.manager, make_transaction(self.cycle, self.category))

        self.manager.deleteTransaction(row.id)

        self.assertFalse(TransactionModel.objects.filter(id=row.id).exists())

    def test_does_nothing_on_nonexistent_id(self):
        self.manager.deleteTransaction(99999)  # must not raise

    def test_does_not_delete_other_transactions(self):
        row1 = log_and_fetch(self.manager, make_transaction(self.cycle, self.category, amount=100))
        row2 = log_and_fetch(self.manager, make_transaction(self.cycle, self.category, amount=200))

        self.manager.deleteTransaction(row1.id)

        self.assertTrue(TransactionModel.objects.filter(id=row2.id).exists())

    def test_total_count_decrements(self):
        row1 = log_and_fetch(self.manager, make_transaction(self.cycle, self.category))
        row2 = log_and_fetch(self.manager, make_transaction(self.cycle, self.category))

        self.manager.deleteTransaction(row1.id)

        self.assertEqual(TransactionModel.objects.count(), 1)


# ── Singleton ──────────────────────────────────────────────────────────────────

class SingletonTests(TestCase):

    def setUp(self):
        TransactionManager._instance = None

    def tearDown(self):
        TransactionManager._instance = None

    def test_same_instance_returned(self):
        a = TransactionManager()
        b = TransactionManager()

        self.assertIs(a, b)