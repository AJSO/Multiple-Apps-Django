from django.shortcuts import render



def mybudget_home(request):
       
    return render(request, 'mybudget/index.html', {})