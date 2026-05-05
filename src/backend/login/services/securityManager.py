from django.contrib.auth.hashers import make_password, check_password
from ..models import UserModel

class securityManager():
    def hashPaaword(self,password):
        '''
        Hashes a plain-text password using Django's make_password utility.
 
        ### parameters
        - password: the password
 
        ### returns
        - The hashed password string.
        '''
        hased = make_password(password)
        return hased
    def SetPassowrd(self,user,password):
        '''
        Hashes and sets the password on a user object, then saves it to the database.
 
        ### parameters
        - user: The user instance to update.
        - password: The password
 
        ### returns
        - The updated user instance.
        '''
        hashed = self.hashPaaword(password)
        user.password = hashed
        user.save()
        return user
    def createUser(self,name,email,password):
        '''
        Creates and persists a new user with a hashed password.
 
        ### parameters
        - name: The display name of the new user.
        - email: The email address of the new user.
        - password: the password.
 
        ### returns
        - The newly created user instance.
        '''
        userEamil = email.lower().strip()
        userName = name.strip()
        newUser =UserModel(
            name = userName,
            email= userEamil
        )
        self.SetPassowrd(newUser,password)
        return newUser
    def checkPassword(self,user,Password):
        '''
        Checks whether a given plain-text password matches the user's stored hashed password.
 
        ### parameters
        - user: The user instance to check against.
        - Password: the password
 
        ### returns
        - True if the password matches, False otherwise.
        '''
        originalPassword=user.password
        isSame = check_password(Password, originalPassword)
        if isSame:
            return True
        else:
            return False
        
    def upadtePassword(self,User,oldPassword,newPassword):
        '''
        Check if the old password is true and then updates it

        ### parameters
        - User: The user instance whose password is being updated.
        - oldPassword: The current password to verify.
        - newPassword: The new password to set.
 
        ### returns
        - None on success, False if the old password is incorrect.
        '''
        isSame = self.checkPassword(User,oldPassword)
        if isSame:
            self.SetPassowrd(User, newPassword)
        else:
            return False

        

    

