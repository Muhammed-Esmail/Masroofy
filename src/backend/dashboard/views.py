from django.shortcuts import render, redirect
from dashboard.forms import SettingsForm
from dashboard.models import SettingsModel
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
    context={}
    context['title'] = 'Dashboard'
    return render(request, 'pages/dashboard/dashboard.html',context)

def settings(request):
    context = {}
    context['title'] = 'settings'
    currentSettings = SettingsModel.objects.first()
    
    
        
    if request.method == 'POST':
        if 'btnSettingsUpdate' in request.POST:
            settingForm = SettingsForm(request.POST, instance=currentSettings)
            passwordform = PasswordChangeForm(request.user)
            if settingForm.is_valid():
                settingForm.save()
                return redirect('settings')
        elif 'btnChangePassword' in request.POST:
            passwordform = PasswordChangeForm(request.user,request.POST)
            settingForm = SettingsForm(instance=currentSettings)
            if passwordform.is_valid():
                user = passwordform.save()
                update_session_auth_hash(request,user)
                return redirect('settings')
            else:
                print(passwordform.errors)
    else:
        passwordform = PasswordChangeForm(request.user)
        settingForm = SettingsForm(instance=currentSettings)

    context['passwordForm'] = passwordform
    context['settingForm'] = settingForm


    return render(request, 'pages/settings/settings.html',context)
