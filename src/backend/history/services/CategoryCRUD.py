from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Category
from transaction.models import CategoryModel

class CategoryCRUD(Fetchable[Category], CRUD[Category]):
    def fetchById(self, id: int):
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