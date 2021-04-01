from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash

from .forms import LoginForm, RegisterForm, UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from Genres.models import Genre
from .models import User, get_filename_ext, upload_image_path

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
        "title":"Register",
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        full_name = form.cleaned_data.get("full_name")
        password = form.cleaned_data.get("password")
        password2 = form.cleaned_data.get("password2")

        qs = User.objects.filter(email=username)
        if qs.exists():
            messages.error(request, "An account with this email already exists.")
        
        if len(password) < 8:
            messages.error(request, "This password is too short. It must contain at least 8 characters.")
            return redirect('register')

        elif password != password2:
            messages.error(request, "The two password fields didn’t match.")
            return redirect('register')

        elif not qs.exists():
            # Create user
            new_user = User.objects.create_user(username, full_name, password)
            # Get info from form and sign in
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            login(request, user)

            return redirect('register_genres')
            print(new_user)

    return render(request, "accounts/register.html", context)


def register_genres_page(request):
    genres = Genre.objects.all()
    user = User.objects.get(email = request.user)

    if request.method == "POST":
        new_genres = request.POST.get('genre_form', user.genres)
        user.genres = new_genres
        user.save()
        # Go to main page
        return redirect('index')
        
    context = {
        "title": "Select Genres",
        "genres": genres
    }

    return render(request, "accounts/register_genres.html", context)


@csrf_exempt
@login_required
def account_page(request):
    genres = Genre.objects.all()
    user = User.objects.get(email = request.user)

    if request.method == "POST":
        if ('change_pass' in request.POST):
            form = PasswordChangeForm(request.user, request.POST)

            print(form.is_valid)
            print(form.errors)

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('account')
        else:
            full_name = request.POST.get('full_name', user.full_name)
            email = request.POST.get('email_form', user.email)
            new_genres = request.POST.get('genre_form', user.genres)
            image = request.FILES.get('image', user.profile_pic)
            user.genres = new_genres
            user.full_name = full_name
            user.email = email
            user.profile_pic = image
            print("{}, {}".format(full_name, email))
            user.save()
            # edit_form = UserUpdateForm(request.POST)
            
            # if edit_form.is_valid():
            #     print("qwe")
            #     user = User()
            #     user.full_name = edit_form.cleaned_data['full_name']

                # user.save()
                # form = edit_form.save(commit=False)
                # form.user = request.user
                # form.save()
                # messages.success(request, "Your profile has been updated!")
            return redirect('account')
    else:
        form = PasswordChangeForm(request.user)
    #     edit_form = UserUpdateForm(instance=user)

    context = {
        "title": "My Account",
        # "form": edit_form,
        "form": form,
        "genres": genres,
    }

    return render(request, "accounts/account.html", context)
