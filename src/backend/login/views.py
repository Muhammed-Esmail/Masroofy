from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services.securityManager import securityManager 
from .models import UserModel
import json


# Create your views here
def home(request):
    userExists = UserModel.objects.exists()
    context = {
        'needSignUp': not userExists
    }
    return render(request, 'pages/login/login.html', context)
def Auth(request):
    '''
    handel both login and signup
    
    ### parameters
    - request: The incoming HTTP POST request containing JSON with email, username, and password.
 
    ### returns
    - A JSON response indicating success or failure, or the rendered login page on GET.
    '''
    userExists = UserModel.objects.exists()
    context = {
            'needSignUp': not userExists
        }
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            name = data.get('username', 'user')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        securityM = securityManager()
        if not userExists:
            newUser=securityM.createUser(name,email,password)
            request.session['userId'] = newUser.id
            request.session['userName'] = newUser.name
            return JsonResponse({"message": "Account created and logged in"}, status=200)
        else: 
                try:
                    user = UserModel.objects.get(email=email.lower().strip())
                    isValid = securityM.checkPassword(user, password)
                    if isValid:
                        request.session['userId'] = user.id
                        request.session['userName'] = user.name 
                        return JsonResponse({"message": "Logged in successfully"}, status=200)
                    else:
                        return JsonResponse({"message": "Invalid email or password"}, status=400)
                except UserModel.DoesNotExist:
                    return JsonResponse({"message": "Invalid email or password"}, status=400)
        
                
    return render(request, 'pages/login/login.html',context)

def verifySession(request):
    '''
    check if the user has an active session
    
    ### parameters
    - request: The incoming HTTP request.
 
    ### returns
    - A JSON response indicating whether the session is valid, including the username if so.
    '''
    if 'userId' in request.session:
        return JsonResponse({"message": "session is vaild","userName":request.session.get('userName')},status=200)
    else:
        return JsonResponse({"message": "no valid session"},status=400)