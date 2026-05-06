from django.db import IntegrityError, transaction
from typing import Optional

from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Category
from transaction.models import CategoryModel

class CategoryCRUD(Fetchable[Category], CRUD[Category]):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    
    def fetchById(self, name: str) -> Category:
        category = CategoryModel.objects.get(name=name)
        return self.createDataObject(category.name, category.description)
        
    def fetchAllCategoriesNames(self) -> list[str]:
        try:
            categories = CategoryModel.objects.all()
            return [category.name for category in categories]
        
        except CategoryModel.DoesNotExist:
            return None
        
    def create(self, newCategory: Category) -> Optional[str]:
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
        CategoryModel.objects.filter(name=name).update(
            name=newCategory.name,
            description=newCategory.description
        )
        return True

    def delete(self, name: str) -> bool:
        CategoryModel.objects.filter(name=name).delete()
        return True


    def createDataObject(self, category_name: str, description: str) -> Category:
        return Category(
            name=category_name,
            description=description
        )