from django.shortcuts import render
from django.http import JsonResponse
from .services.securityManager import securityManager 
from django.contrib.auth import get_user_model
from django.contrib.auth import login 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
import json
from django.views.decorators.cache import never_cache

User = get_user_model()


# Create your views here
@never_cache
def home(request):
    userExists = User.objects.exists()
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
    userExists = User.objects.exists()
    context = {
            'needSignUp': not userExists
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
                token, _ = Token.objects.get_or_create(user=newUser)
                login(request, newUser)
                request.session['username'] = newUser.username
                return JsonResponse({"message": "Account created and logged in", "token":token.key}, status=200)
            except ValidationError as error:
                return JsonResponse({"message":"password is not valid", "errors":error.messages},status =400)
            
        else: 
                try:
                    user = User.objects.get(email=email.lower().strip())
                    isValid = securityM.checkPassword(user, password)
                    if isValid:
                        login(request, user)
                        token, _ = Token.objects.get_or_create(user=User)
                        request.session['username'] = user.username 
                        return JsonResponse({"message": "Logged in successfully", "token":token.key}, status=200)
                    else:
                        return JsonResponse({"message": "Invalid email or password55"}, status=400)
                except User.DoesNotExist:
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
    authHeader = request.META.get('HTTP_AUTHORIZATION', '')
    if not authHeader.startswith('Token '):
        return JsonResponse({"valid": False, "message": "No token provided"}, status=401)
    
    token_key = authHeader.split(' ')[1]
    try:
        token = Token.objects.get(key=token_key)
        return JsonResponse({"valid": True, "username": token.user.username}, status=200)
    except Token.DoesNotExist:
        return JsonResponse({"valid": False, "message": "Invalid token"}, status=401)

