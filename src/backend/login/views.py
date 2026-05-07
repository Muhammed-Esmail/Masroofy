from django.shortcuts import render
from django.http import JsonResponse
from .services.securityManager import securityManager 
from django.contrib.auth import get_user_model
from django.contrib.auth import login 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import json
from django.views.decorators.cache import never_cache
from userSettings.services.SettingsManager import SettingsManager
User = get_user_model()


# Create your views here
@never_cache
def home(request):
    userExists = User.objects.exists()
    context = {
        'needSignUp': not userExists,
        'settings': SettingsManager().fetchSettings(),
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
    userExists = User.objects.exists()
    context = {
        'needSignUp': not userExists,
        'settings': SettingsManager().fetchSettings(),
    }
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username', 'user')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        securityM = securityManager()
        if not userExists:
            try:
                validate_password(password)
                newUser=securityM.createUser(username,email,password)
                login(request, newUser)
                request.session['username'] = newUser.username
                return JsonResponse({"message": "Account created and logged in"}, status=200)
            except ValidationError as error:
                return JsonResponse({"message":"password is not valid", "errors":error.messages},status =400)
            
        else: 
            try:
                user = User.objects.get(email=email.lower().strip())
                isValid = securityM.checkPassword(user, password)
                if isValid:
                    login(request, user)
                    request.session['username'] = user.username 
                    return JsonResponse({"message": "Logged in successfully"}, status=200)
                else:
                    return JsonResponse({"message": "Invalid email or password55"}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"message": "Invalid email or password"}, status=400)
    
                
    return render(request, 'pages/login/login.html',context)