from django.shortcuts import render, redirect
from .forms import SettingsForm
from .models import SettingsModel
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from userSettings.services.SettingsManager import SettingsManager
from backend.Controller import Controller
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def settings(request):

    currentSettings = SettingsModel.objects.first()

    settingForm = SettingsForm(instance=currentSettings)
    passwordform = PasswordChangeForm(request.user)
    
    if request.method == 'POST':
        if 'btnSettingsUpdate' in request.POST:
            settingForm = SettingsForm(request.POST, instance=currentSettings)
            passwordform = PasswordChangeForm(request.user)
            if settingForm.is_valid():
                settingForm.save()
                return redirect('settings')
        elif 'btnChangePassword' in request.POST:
            settingForm = SettingsForm(instance=currentSettings)
            passwordform = PasswordChangeForm(request.user,request.POST)
            if passwordform.is_valid():
                user = passwordform.save()
                update_session_auth_hash(request,user)
                return redirect('settings')
            else:
                print(passwordform.errors)

    context = {
        'title': 'Settings',
        'settingForm': settingForm,
        'passwordForm': passwordform,
        'settings': SettingsManager().fetchSettings(),
    }


    return render(request, 'pages/settings/settings.html', context)
