from django.test import TestCase

from backend.shared_classes.Category import Category
from transaction.models import CategoryModel
from transaction.services.CategoryManager import CategoryManager
from history.services import CategoryCRUD


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_manager() -> CategoryManager:
    """Returns a fresh (non-singleton) CategoryManager."""
    CategoryCRUD._instance = None
    manager = CategoryManager.__new__(CategoryManager)
    manager._catagoryCRUD = CategoryCRUD()
    return manager


# ── addCategory ────────────────────────────────────────────────────────────────

class AddCategoryTests(TestCase):

    def test_returns_category_on_success(self):
        manager = make_manager()

        result = manager.addCategory("Food", "Food expenses")

        self.assertIsNotNone(result)

    def test_returned_category_has_correct_name(self):
        manager = make_manager()

        result = manager.addCategory("Food", "Food expenses")

        self.assertEqual(result.name, "Food")

    def test_returned_category_has_correct_description(self):
        manager = make_manager()

        result = manager.addCategory("Food", "Food expenses")

        self.assertEqual(result.description, "Food expenses")

    def test_returned_category_has_real_db_id(self):
        manager = make_manager()

        result = manager.addCategory("Food", "Food expenses")

        self.assertIsNotNone(result.id)
        self.assertGreater(result.id, 0)

    def test_category_row_exists_in_db_after_add(self):
        manager = make_manager()

        manager.addCategory("Food", "Food expenses")

        self.assertTrue(CategoryModel.objects.filter(category_name="Food").exists())

    def test_two_different_names_both_succeed(self):
        manager = make_manager()

        food = manager.addCategory("Food", "Food expenses")
        transport = manager.addCategory("Transport", "Transport expenses")

        self.assertIsNotNone(food)
        self.assertIsNotNone(transport)
        self.assertNotEqual(food.id, transport.id)

    def test_returns_none_on_duplicate_name(self):
        manager = make_manager()
        manager.addCategory("Food", "First")

        result = manager.addCategory("Food", "Duplicate")

        self.assertIsNone(result)

    def test_duplicate_does_not_create_extra_db_row(self):
        manager = make_manager()
        manager.addCategory("Food", "First")

        manager.addCategory("Food", "Duplicate")

        self.assertEqual(CategoryModel.objects.filter(category_name="Food").count(), 1)


# ── deleteCategory by name (only working overload) ─────────────────────────────

class DeleteCategoryByNameTests(TestCase):

    def test_deletes_existing_category(self):
        manager = make_manager()
        manager.addCategory("Food", "Food expenses")

        manager.deleteCategory("Food")

        self.assertFalse(CategoryModel.objects.filter(category_name="Food").exists())

    def test_does_nothing_when_category_does_not_exist(self):
        manager = make_manager()

        manager.deleteCategory("Nonexistent")  # must not raise

    def test_does_not_delete_other_categories(self):
        manager = make_manager()
        manager.addCategory("Food", "Food expenses")
        manager.addCategory("Transport", "Transport expenses")

        manager.deleteCategory("Food")

        self.assertTrue(CategoryModel.objects.filter(category_name="Transport").exists())

    def test_total_row_count_decrements(self):
        manager = make_manager()
        manager.addCategory("Food", "Food expenses")
        manager.addCategory("Transport", "Transport expenses")

        manager.deleteCategory("Food")

        self.assertEqual(CategoryModel.objects.count(), 1)


# ── Singleton ──────────────────────────────────────────────────────────────────

class SingletonTests(TestCase):

    def setUp(self):
        CategoryManager._instance = None
        CategoryCRUD._instance = None

    def tearDown(self):
        CategoryManager._instance = None
        CategoryCRUD._instance = None

    def test_same_instance_returned(self):
        a = CategoryManager()
        b = CategoryManager()

        self.assertIs(a, b)

    def test_crud_initialized_on_first_instantiation(self):
        manager = CategoryManager()

        self.assertIsNotNone(manager._catagoryCRUD)