from django.contrib.auth.hashers import make_password, check_password
from ..models import UserModel

class securityManager():
    def hashPaaword(self,password):
        '''
        Hash the Password in SHA256 format
        '''
        hased = make_password(password)
        return hased
    def SetPassowrd(self,user,password):
        '''
        Set the user password the first time
        '''
        hashed = self.hashPaaword(password)
        user.password = hashed
        user.save()
        return user
    def createUser(self,name,email,password):
        '''Creats a new user'''
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
        return true if the password matches the password in the database
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
        '''
        isSame = self.checkPassword(User,oldPassword)
        if isSame:
            self.SetPassowrd(User, newPassword)
        else:
            return False

        

    

