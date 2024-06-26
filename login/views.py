# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Calidad').exists():
                return redirect('pull/test')
            if user.groups.filter(name='rh_').exists():
                return redirect('rh/')
            else:    
                return redirect('pull/')  
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')  
