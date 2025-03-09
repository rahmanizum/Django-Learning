from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

def home(request):

    records = Record.objects.all()


    if request.method == 'POST':
         return login_user(request)
    else:
        return render(request,'home.html',{'records':records})

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

def register_user(request):
    if request.method == 'POST':
        reg_form = SignUpForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            username = reg_form.cleaned_data.get('username')
            raw_password = reg_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request,'You have successfully registered')
            return redirect('home')
    else:
        reg_form = SignUpForm()
        return render(request,'register.html',{'reg_form':reg_form})
    
    return render(request,'register.html',{'reg_form':reg_form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.error(request,'You must be logged in to view records')
        return redirect('home')

def delete_record(request , pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, f'Record {record.first_name} deleted successfully')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to delete records')
        return redirect('home')
    