from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Movies.models import Movie, MovieGenre
from Genres.models import Genre

def home_page(request):
    movie = Movie.objects.all()
    genre = Genre.objects.all()
    context = {
        "title":"Film Finder",
        "movies": movie,
        "genre":genre
    }
    if request.method == "POST":
        #pass thru info here
        return redirect("result")
    return render(request, "search.html", context)

def results_page(request):

    return render(request, "results.html", {})
 