# TODO: Get top movies function and pass to search page and top movies page
# TODO: Make login/register first page NOT search page
# TODO: Pass movie results to results page (are we going to search just through titles? Genres?)

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
import urllib.parse

from Movies.models import Movie, MovieGenre, MoviePerson
from Genres.models import Genre
from accounts.forms import LoginForm
from Reception.models import Reception
from Background.models import Background
from Person.models import Person

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
    top_movie_ids = reception.order_by('-avgRatings', '-numRatings')[:6]
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
    if (search_query.isspace() == False and search_query != ""):
        previous_searches = request.user.recent_searches
        
        if (previous_searches == None):
            previous_searches = ""

        request.user.recent_searches = search_query + "," + previous_searches
        request.user.save()

    context = {
        "title":"Search results for " + search_query,
        "search_query":search_query,
        # Movie results
    }

    # Find movies


    return render(request, "results.html", context)

def top_movies_page(request):

    reception = Reception.objects.all()
    movies = MovieGenre.objects.all()
    background = Background.objects.all()

    top_movie_ids = reception.filter(avgRatings__gte=7).order_by('-avgRatings', '-numRatings')
    top_movies = []

    for movie in top_movie_ids:
        # Release date
        try:
            release = background.get(movie_id=movie.movie_id).releaseDate
        except Background.DoesNotExist:
            release = None

        # Length
        try:
            length =  background.get(movie_id=movie.movie_id).length
        except Background.DoesNotExist:
            length = None

        top_movies.append([movie, reception.get(movie_id=movie.movie_id.movie_id).avgRatings, release, length])

    context = {
        "title": "Top Movies",
        "top_movies": top_movies
        # Top Movies
    }

    return render(request, "topmovies.html", context)

def movie_page(request, movie_id):
    movies = Movie.objects.all() 
    movies_genres = MovieGenre.objects.all()
    movies_people = MoviePerson.objects.all()
    people = Person.objects.all()
    all_genres = Genre.objects.all()
    ratings = Reception.objects.all()
    background = Background.objects.all()
    genres = []
    cast = []

    movie = movies.get(movie_id=movie_id)

    # Create list of genres
    movie_genre = movies_genres.filter(movie_id=movie.movie_id)

    for genre in movie_genre:
        genres.append(all_genres.get(genre_id=genre.genre_id.genre_id).genre_title)

    # Ratings
    try:
        rating = ratings.get(movie_id=movie.movie_id).avgRatings
    except Reception.DoesNotExist:
        rating = None
    
    # Release date
    try:
        release = background.get(movie_id=movie.movie_id).releaseDate
    except Background.DoesNotExist:
        release = None

    # Length
    try:
        length =  background.get(movie_id=movie.movie_id).length
    except Background.DoesNotExist:
        length = None

    # Create list of cast
    movie_person = movies_people.filter(movie_id=movie.movie_id)

    for person in movie_person:
        cast.append(person.person_id.name)

    context = {
        "title": movie.title,
        "movie": movie,
        "genres": genres,
        "rating":rating,
        "duration":length,
        "cast":cast,
        "description":movie.overview,
        "release":release,
    }

    return render(request, "movie.html", context)