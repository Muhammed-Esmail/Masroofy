from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
User = get_user_model()


class securityManager():
    
    def hashPassword(self,password):
        '''
        Hashes a plain-text password using Django's make_password utility.
 
        ### parameters
        - password: the password
 
        ### returns
        - The hashed password string.
        '''
        hased = make_password(password)
        return hased
    def SetPassword(self,user,password):
        '''
        Hashes and sets the password on a User object, then saves it to the database.
 
        ### parameters
        - User: The User instance to update.
        - password: The password
 
        ### returns
        - The updated User instance.
        '''
        hashed = self.hashPassword(password)
        user.password = hashed
        user.save()
        return user
    def createUser(self,username,email,password):
        '''
        Creates and persists a new User with a hashed password.
 
        ### parameters
        - username: The display username of the new User.
        - email: The email address of the new User.
        - password: the password.
 
        ### returns
        - The newly created User instance.
        '''
        userEamil = email.lower().strip()
        userName = username.strip()
        newUser =User(
            username = userName,
            email= userEamil
        )
        self.SetPassword(newUser,password)
        return newUser
    def checkPassword(self,user,Password):
        '''
        Checks whether a given plain-text password matches the User's stored hashed password.
 
        ### parameters
        - User: The User instance to check against.
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
        
    def updatePassword(self,user,oldPassword,newPassword):
        '''
        Check if the old password is true and then updates it

        ### parameters
        - User: The User instance whose password is being updated.
        - oldPassword: The current password to verify.
        - newPassword: The new password to set.
 
        ### returns
        - None on success, False if the old password is incorrect.
        '''
        isSame = self.checkPassword(user,oldPassword)
        if isSame:
            self.SetPassword(user, newPassword)
        else:
            return False

        

    

