from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    context={}
    context['title'] = 'Dashboard'
    return render(request, 'pages/dashboard/dashboard.html',context)

