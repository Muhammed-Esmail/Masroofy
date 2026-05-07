from history.services import CategoryCRUD
from backend.shared_classes.Category import Category
from typing import Optional

class CategoryManager:
    _catagoryCRUD: CategoryCRUD = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._catagoryCRUD = CategoryCRUD()
        return cls._instance
    
    def addCategory(self, category: Category) -> Optional[Category]:
        '''
        ## Adds a new category to the DB.
        
        ### Parameters
        - category: Category

        ### Returns
        - [Category]: If the new category ID if inserted successfully

        - [None]: If the name was associated with another existing category
        '''

        newCat = self._catagoryCRUD.create(category)

        if newCat is None: # Name was not unique / DB failed
            return None

        return newCat
    
    def fetchAllCategories(self) -> list[str]:
        return self._catagoryCRUD.fetchAllCategoriesNames()
    
    def updateCategory(self, name: str, newCategory: Category) -> bool:
        self._catagoryCRUD.update(name, newCategory)
        return True
        
    def deleteCategory(self, category: Category) -> None:
        '''
        ## Deletes an existing category given a category object.

        ### Parameters
        - category: Category

        ### Returns
        - [None]: if the category did not exist it will ignore, otherwise delete normally
        '''
        self.deleteCategory(category_name=category.name)

    def deleteCategory(self, category_name: str) -> None:
        '''
        ## Deletes an existing category given its name.

        ### Parameters
        - category_name: str

        ### Returns
        - [None]: if the category did not exist it will ignore, otherwise delete normally
        '''
        self._catagoryCRUD.delete(category_name)