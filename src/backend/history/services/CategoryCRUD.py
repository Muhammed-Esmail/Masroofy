from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Category
from transaction.models import CategoryModel

class CategoryCRUD(Fetchable[Category], CRUD[Category]):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    
    def fetchById(self, id: int) -> Category:
        category = CategoryModel.objects.get(id=id)
        return self.createDataObject(category.id, category.category_name, category.description)

    def create(self, newCategory: Category):
        CategoryModel.objects.create(
            category_name=newCategory.name,
            description=newCategory.description
        )
        return True

    def update(self, id: int, newCategory: Category):
        CategoryModel.objects.filter(id=id).update(
            category_name=newCategory.name,
            description=newCategory.description
        )
        return True

    def delete(self, id: int):
        CategoryModel.objects.filter(id=id).delete()
        return True


    def createDataObject(self, id: int, category_name: str, description: str):
        return Category(
            id=id,
            name=category_name,
            description=description
        )