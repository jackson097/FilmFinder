from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import LoginForm, RegisterForm

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('login')  
    
    return render(request, "accounts/login.html", context)

User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)

    return render(request, "accounts/register.html", context)
