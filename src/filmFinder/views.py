# TODO: Get top movies function and pass to search page and top movies page
# TODO: Make login/register first page NOT search page
# TODO: Pass movie results to results page (are we going to search just through titles? Genres?)

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
import urllib.parse

from Movies.models import Movie, MovieGenre
from Genres.models import Genre
from accounts.forms import LoginForm
from Reception.models import Reception

def home_page(request):
    movies = Movie.objects.all() 
    genres = Genre.objects.all()
    movies_genres = MovieGenre.objects.all()
    reception = Reception.objects.all()

    movie_genre_list = []
    form = LoginForm()

    for movie in movies:
        # Takes first genre for a given movie (movies can have more than one genre)
        movie_genre = movies_genres.filter(movie_id=movie.movie_id).first()

        if movie_genre is not None:
            genre = genres.get(genre_id=movie_genre.genre_id.genre_id).genre_title
        else: # If movie has no genre
            genre = "No genre"

        movie_genre_list.append([movie, genre]) # Format: [Movie Object, string]
    
    # Get top movies
    top_movie_ids = reception.order_by('-avgRatings', '-numRatings')[:4]
    top_movies = []

    for movie in top_movie_ids:
        top_movies.append(movies.get(movie_id=movie.movie_id.movie_id))
    
    context = {
        "title":"Film Finder",
        "movies": movie_genre_list,
        "top_movies": top_movies,
    }

    if request.method == 'POST':
        request.user.recent_searches = ""
        request.user.save()

    if request.user.is_authenticated:
        return render(request, "search.html", context)
    
    return redirect("login")

def results_page(request):
    search_query = urllib.parse.unquote(request.GET.urlencode().split("=",1)[1])
    search_query = search_query.replace("+", " ")

    # Update recent searches
    request.user.recent_searches = search_query + "," + request.user.recent_searches
    request.user.save()

    context = {
        "title":"Search results for " + search_query,
        "search_query":search_query,
        # Movie results
    }

    # Find movies


    return render(request, "results.html", context)

def top_movies_page(request):

    # Get top movies

    context = {
        "title": "Top Movies",
        # Top Movies
    }

    return render(request, "topmovies.html", context)
 
def account_page(request):
    context = {
        "title": "My Account",
    }

    return render(request, "account.html", context)

def movie_page(request, movie_id):
    movies = Movie.objects.all() 
    movie = movies.get(movie_id=movie_id)

    context = {
        "title": movie.title,
        "movie": movie,
    }

    return render(request, "movie.html", context)