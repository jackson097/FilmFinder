from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Movies.models import Movie

def home_page(request):
    movie = Movie.objects.all()
    context = {
        "title":"Film Finder",
        "movies": movie
    }
    return render(request, "search.html", context)