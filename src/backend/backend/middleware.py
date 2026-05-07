from django.shortcuts import redirect
from django.urls import reverse, resolve
from cycle.services.AllowanceManager import AllowanceManager

TOKEN_NAME = 'token'
LOGIN_PAGE_NAME = 'login:login'
CYCLE_PAGE_NAME = 'cycle:welcome'

class MasroofyAuthMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        
        cycle_url = reverse(CYCLE_PAGE_NAME)
        login_url = reverse(LOGIN_PAGE_NAME)
        requested_url = request.path

        try:
            match = resolve(request.path)
            app_name = match.app_name  # Look for 'app_name' in urls.py
        except:
            app_name = None

        # Exclude if it belongs to the 'login' app or a static file
        if app_name == 'login':
            return self.get_response(request)

        # Must verify auth
        is_auth = False 

        try:
            is_auth = request.user.is_authenticated
        except:
            pass

        if not is_auth:
            return redirect(login_url)

        # User is logged in
        # Check if there is an active cycle
        if not app_name == 'cycle' and not self.checkActiveCycle():
            return redirect(cycle_url)

        # User passed checks
        return self.get_response(request) 

    def checkActiveCycle(self):
        '''
        # Verifies the user has an active cycle in server's DB 
        '''
        allowanceManager = AllowanceManager()
        return allowanceManager.checkActivityStatus()