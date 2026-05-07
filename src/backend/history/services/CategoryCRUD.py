from django.db import IntegrityError, transaction
from typing import Optional

from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Category
from transaction.models import CategoryModel

class CategoryCRUD(Fetchable[Category], CRUD[Category]):
    """
    A Singleton service responsible for the persistence and retrieval of Categories.

    This class implements the CRUD and Fetchable interfaces to map the business-logic 
    Category objects to the Django CategoryModel database records.

    Attributes:
        _instance (CategoryCRUD): The single shared instance of this class.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures a single instance of CategoryCRUD is maintained.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def fetchById(self, name: str) -> Category:
        """
        Retrieves a category from the database by its unique name.

        Args:
            name (str): The unique name of the category.

        Returns:
            Category: A data object representing the category.
            
        Raises:
            CategoryModel.DoesNotExist: If no category matches the provided name.
        """
        category = CategoryModel.objects.get(name=name)
        return self.createDataObject(category.name, category.description)
        
    def fetchAllCategoriesNames(self) -> list[str]:
        """
        Retrieves a list of all existing category names.

        Returns:
            list[str]: A list of category names, or None if an error occurs.
        """
        try:
            categories = CategoryModel.objects.all()
            return [category.name for category in categories]
        except CategoryModel.DoesNotExist:
            return None
        
    def create(self, newCategory: Category) -> Optional[str]:
        """
        Persists a new Category record to the database.

        Uses an atomic transaction to ensure data integrity during creation.

        Args:
            newCategory (Category): The category data object to save.

        Returns:
            Optional[str]: The name of the created category if successful, 
            None if an IntegrityError (e.g., duplicate name) occurs.
        """
        try:
            with transaction.atomic():
                obj = CategoryModel.objects.create(
                    name=newCategory.name,
                    description=newCategory.description
                )
            return obj.name
        except IntegrityError:
            return None

    def update(self, name: str, newCategory: Category) -> bool:
        """
        Updates an existing Category record.

        Args:
            name (str): The current name of the category to locate it.
            newCategory (Category): The new data to be applied.

        Returns:
            bool: Always returns True as the update is performed via QuerySet.
        """
        CategoryModel.objects.filter(name=name).update(
            name=newCategory.name,
            description=newCategory.description
        )
        return True

    def delete(self, name: str) -> bool:
        """
        Deletes a Category record from the database.

        Args:
            name (str): The name of the category to remove.

        Returns:
            bool: Always returns True after the deletion attempt.
        """
        CategoryModel.objects.filter(name=name).delete()
        return True

    def createDataObject(self, category_name: str, description: str) -> Category:
        """
        Factory method to instantiate a Category data object.

        This helper ensures consistent creation of business-layer objects 
        from database-layer data.

        Args:
            category_name (str): Name of the category.
            description (str): Description of the category.

        Returns:
            Category: A populated Category object.
        """
        return Category(
            name=category_name,
            description=description
        )