from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import LoginForm, RegisterForm

User = get_user_model()


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form,
        "title":"Login"
    }
    if form.is_valid():
        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Email or password is incorrect")
            return redirect('login')  
    
    return render(request, "accounts/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form,
        "title":"Register"
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        full_name = form.cleaned_data.get("full_name")
        password = form.cleaned_data.get("password")
        password2 = form.cleaned_data.get("password2")

        qs = User.objects.filter(email=username)
        if qs.exists():
            messages.error(request, "Email is taken")

        if len(password) < 5:
            messages.error(request, "Passwords must have a length of at least 5")
            return redirect('register')

        elif password != password2:
           messages.error(request, "Passwords must be the same")
           return redirect('register')

        else:
            # Below will need to be modified when we add genres as an option
            new_user = User.objects.create_user(username, full_name, password)
            return redirect('register_genres')  
            print(new_user)

    return render(request, "accounts/register.html", context)


def register_genres_page(request):
    return render(request, "accounts/register_genres.html")
