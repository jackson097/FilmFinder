from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Movies.models import Movie, MovieGenre
from Genres.models import Genre

def home_page(request):
    movies = Movie.objects.all() 
    genres = Genre.objects.all()
    movies_genres = MovieGenre.objects.all()
    movie_genre_list = []

    for movie in movies:
        # Takes first genre for a given movie (movies can have more than one genre)
        movie_genre = movies_genres.filter(movie_id=movie.movie_id).first()

        if movie_genre is not None:
            genre = genres.get(genre_id=movie_genre.genre_id.genre_id).genre_title
        else: # If movie has no genre
            genre = "No genre"

        movie_genre_list.append([movie, genre]) # Format: [Movie Object, string]
    
    context = {
        "title":"Film Finder",
        "movies": movie_genre_list
    }
    if request.method == "POST":
        #pass thru info here
        return redirect("result")
    
    return render(request, "search.html", context)

def results_page(request):
    return render(request, "results.html", {})

def recommendations_page(request):
    return render(request, "recommendations.html", {})
 
def account_page(request):
    return render(request, "account.html", {})