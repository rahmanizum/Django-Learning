from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.method == 'POST':
         return login_user(request)
    else:
        return render(request,'home.html',{})

def login_user(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request,'Invalid login')
            return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('home')
