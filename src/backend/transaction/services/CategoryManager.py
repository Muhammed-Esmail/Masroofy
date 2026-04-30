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
    
    def addCategory(self, cat_name: str, cat_description: str) -> Optional[Category]:
        '''
        ## Adds a new category to the DB.
        
        ### Parameters
        - cat_name: str
        - cat_description: str

        ### Returns
        - [Category]: If the new category ID if inserted successfully

        - [None]: If the name was associated with another existing category
        '''
        newCat = self._catagoryCRUD.createDataObject(
            id=-1, # Unknown yet
            category_name=cat_name,
            description=cat_description
        )

        newID = self._catagoryCRUD.create(newCat)

        if newID is None: # Name was not unique / DB failed
            return None
        
        newCat.id = newID

        return newCat

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

        catObj = self._catagoryCRUD.fetchByName(category_name)

        if catObj is None:
            return
        
        self._catagoryCRUD.delete(catObj.id)