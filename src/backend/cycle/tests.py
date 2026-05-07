from datetime import date
from django.test import TestCase

from backend.shared_classes import Cycle
from cycle.models import CycleModel, ActiveCycleModel
from cycle.services.AllowanceManager import AllowanceManager, NoCycleException
from backend.Controller import Controller


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_manager() -> AllowanceManager:
    """
    Returns a fresh (non-singleton) AllowanceManager wired to a real Controller.
    Bypasses __new__ so each test gets a fully isolated instance.
    """
    manager = AllowanceManager.__new__(AllowanceManager)
    controller = Controller.__new__(Controller)
    controller._initialize()
    manager.setController(controller)
    return manager


def make_cycle_in_db(amount=1000) -> CycleModel:
    """Creates and returns a CycleModel row. Not active unless set_active_cycle is called."""
    return CycleModel.objects.create(
        startDate=date(2024, 1, 1),
        endDate=date(2024, 1, 31),
        amount=amount,
    )


def set_active_cycle(cycle: CycleModel) -> None:
    """Points ActiveCycleModel at the given cycle."""
    ActiveCycleModel.objects.all().delete()
    ActiveCycleModel.objects.create(cycle=cycle)


def make_active_cycle_in_db(amount=1000) -> CycleModel:
    """Creates a CycleModel row and makes it the active cycle."""
    cycle = make_cycle_in_db(amount=amount)
    set_active_cycle(cycle)
    return cycle


def make_cycle(amount=1000) -> Cycle:
    """Creates a Cycle dataclass (not saved to DB) to pass into initializeCycle."""
    return Cycle(
        id=None,
        startDate=date(2024, 1, 1),
        endDate=date(2024, 1, 31),
        amount=amount,
    )


# ── checkActivityStatus ────────────────────────────────────────────────────────

class CheckActivityStatusTests(TestCase):

    def test_returns_true_when_active_cycle_exists(self):
        make_active_cycle_in_db()
        manager = make_manager()

        self.assertTrue(manager.checkActivityStatus())

    def test_returns_false_when_no_active_cycle(self):
        # ActiveCycleModel table is empty
        manager = make_manager()

        self.assertFalse(manager.checkActivityStatus())

    def test_returns_false_when_cycle_exists_but_not_active(self):
        make_cycle_in_db()  # cycle in DB but no ActiveCycleModel row
        manager = make_manager()

        self.assertFalse(manager.checkActivityStatus())


# ── getCurrentCycle ────────────────────────────────────────────────────────────

class GetCurrentCycleTests(TestCase):

    def test_returns_correct_cycle_from_db(self):
        db_cycle = make_active_cycle_in_db(amount=500)
        manager = make_manager()

        result = manager.getCurrentCycle()

        self.assertEqual(result.id, db_cycle.id)
        self.assertEqual(result.amount, 500)

    def test_raises_when_no_active_cycle(self):
        manager = make_manager()

        with self.assertRaises(NoCycleException):
            manager.getCurrentCycle()

    def test_raises_when_cycle_exists_but_not_active(self):
        make_cycle_in_db()  # in DB but not pointed to by ActiveCycleModel
        manager = make_manager()

        with self.assertRaises(NoCycleException):
            manager.getCurrentCycle()

    def test_returns_correct_cycle_when_multiple_exist(self):
        make_cycle_in_db(amount=100)          # old cycle, not active
        active = make_active_cycle_in_db(amount=999)
        manager = make_manager()

        result = manager.getCurrentCycle()

        self.assertEqual(result.id, active.id)
        self.assertEqual(result.amount, 999)


# ── resetCycle ─────────────────────────────────────────────────────────────────

class ResetCycleTests(TestCase):

    def test_clears_active_cycle_from_db(self):
        make_active_cycle_in_db()
        manager = make_manager()

        manager.resetCycle()

        self.assertEqual(ActiveCycleModel.objects.count(), 0)

    def test_does_not_delete_cycle_row(self):
        """resetCycle clears the pointer, not the historical data."""
        make_active_cycle_in_db()
        manager = make_manager()

        manager.resetCycle()

        self.assertEqual(CycleModel.objects.count(), 1)

    def test_does_nothing_when_no_active_cycle(self):
        manager = make_manager()

        manager.resetCycle()  # must not raise

        self.assertEqual(ActiveCycleModel.objects.count(), 0)

    def test_does_not_affect_other_cycle_rows(self):
        make_cycle_in_db(amount=100)   # old inactive cycle
        make_active_cycle_in_db(amount=200)
        manager = make_manager()

        manager.resetCycle()

        # Both CycleModel rows still exist, only the pointer is gone
        self.assertEqual(CycleModel.objects.count(), 2)
        self.assertEqual(ActiveCycleModel.objects.count(), 0)


# ── initializeCycle ────────────────────────────────────────────────────────────

class InitializeCycleTests(TestCase):

    def test_creates_new_cycle_row_in_db(self):
        manager = make_manager()

        manager.initializeCycle(make_cycle(amount=2000))

        self.assertEqual(CycleModel.objects.count(), 1)
        self.assertEqual(CycleModel.objects.first().amount, 2000)

    def test_sets_new_cycle_as_active(self):
        manager = make_manager()

        manager.initializeCycle(make_cycle(amount=2000))

        self.assertEqual(ActiveCycleModel.objects.count(), 1)
        self.assertEqual(ActiveCycleModel.objects.first().cycle.amount, 2000)

    def test_clears_old_active_cycle_before_creating_new(self):
        old = make_active_cycle_in_db(amount=1000)
        manager = make_manager()

        manager.initializeCycle(make_cycle(amount=3000))

        # Old cycle row still exists (history preserved)
        self.assertTrue(CycleModel.objects.filter(id=old.id).exists())
        # But it is no longer the active cycle
        self.assertNotEqual(ActiveCycleModel.objects.first().cycle.id, old.id)

    def test_only_one_active_cycle_after_initialize(self):
        make_active_cycle_in_db()
        manager = make_manager()

        manager.initializeCycle(make_cycle(amount=1500))

        self.assertEqual(ActiveCycleModel.objects.count(), 1)

    def test_total_cycle_count_increments(self):
        make_active_cycle_in_db()
        manager = make_manager()

        manager.initializeCycle(make_cycle(amount=1500))

        self.assertEqual(CycleModel.objects.count(), 2)

    def test_new_cycle_is_retrievable_via_getCurrentCycle(self):
        manager = make_manager()

        manager.initializeCycle(make_cycle(amount=2500))
        result = manager.getCurrentCycle()

        self.assertEqual(result.amount, 2500)


# ── Singleton ──────────────────────────────────────────────────────────────────

class SingletonTests(TestCase):

    def setUp(self):
        AllowanceManager._instance = None

    def tearDown(self):
        AllowanceManager._instance = None

    def test_same_instance_returned(self):
        a = AllowanceManager()
        b = AllowanceManager()
        self.assertIs(a, b)

    def test_setController_persists_on_singleton(self):
        manager = AllowanceManager()
        controller = Controller.__new__(Controller)
        controller._initialize()
        manager.setController(controller)

        same_manager = AllowanceManager()
        self.assertIs(same_manager._controller, controller)