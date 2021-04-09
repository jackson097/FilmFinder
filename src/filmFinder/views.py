# TODO: Get top movies function and pass to search page and top movies page
# TODO: Make login/register first page NOT search page
# TODO: Pass movie results to results page (are we going to search just through titles? Genres?)

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
import urllib.parse
import difflib

from Movies.models import Movie, MovieGenre, MoviePerson
from Genres.models import Genre
from accounts.forms import LoginForm
from Reception.models import Reception
from Background.models import Background
from Person.models import Person
from accounts.models import User

from filmFinder.utils import get_data, recommendations, get_related, search_actors, search_genres, get_suggestions, sort_by_user_genre

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
    user = User.objects.get(email = request.user)

    explore = []
    related = []

    suggestion = request.GET.get("suggestion", None)
    query = request.GET.get("search", None)

    # Get data for recommendations
    df, cosine_sim = get_data()

    # Get search query from url
    search_query = urllib.parse.unquote(request.GET.urlencode().split("=",1)[1].split("&",1)[0])
    search_query = search_query.replace("+", " ")
    
    # Get suggestion query from url
    if (suggestion):
        suggestion_query = urllib.parse.unquote(request.GET.urlencode().split("=",1)[1].split("&",1)[1])
        suggestion_id = suggestion_query.split("=",1)[1].split("+",1)[0]
        suggestion_type = suggestion_query.split("=",1)[1].split("+",1)[1]
        suggested_movies, suggestion_title = get_suggestions(suggestion_type, suggestion_id, df, cosine_sim, user.genres)
    else:
        suggestion_title = None
        suggestion_type = None
        suggested_movies = None

    # Search by title
    movies = Movie.objects.filter(title__icontains=query)
    movies = list(movies)

    for movie in movies:
        explore.append((movie.title.strip(), movie.movie_id, 'title'))

    # Search by actor
    movies_actors, explore = search_actors(search_query, explore)

    for movie in movies_actors:
        if (movie not in movies):
            movies.append(movie)

    # Get recommendations for each movie in result (only for actor and title queries)
    for movie in movies:
        # Returns list of movie ids
        rec = recommendations(df, movie.movie_id, cosine_sim)
        for mov in get_related(rec):
            if (mov not in related):
                related.append(mov)

    # Search by genre
    movies_genres, explore = search_genres(query, explore)
    
    for movie in movies_genres:
        if (movie not in movies):
            movies.append(movie)

    # Update recent searches
    if (search_query.isspace() == False and search_query != "" and not suggestion):
        previous_searches = user.recent_searches
        
        if (previous_searches == None):
            previous_searches = ""

        user.recent_searches = search_query + "," + previous_searches
        user.save()
    
    # Sort related movies based on users favourite genre
    related = sort_by_user_genre("all related", related, user.genres)

    # Add related movie only if not already retrieved from search query
    for movie in related:
        if (movie not in movies):
            movies.append(movie)

    num_results = len(movies)
    
    explore_sorted = []

    if (query):
        for term in explore:
            ratio = difflib.SequenceMatcher(None, term[0], query).ratio()
            explore_sorted.append((term[0], term[1], term[2], ratio))

        if (len(query) == 1): # User searching by letter
            explore_sorted = sorted(explore_sorted, key=lambda x: x[0], reverse=False)
        else:
            explore_sorted = sorted(explore_sorted, key=lambda x: x[3], reverse=True)
                
    if (suggested_movies):
        movies = suggested_movies

    context = {
        "title":"Search results for " + search_query,
        "search_query":search_query,
        "movies": movies, # ORDER IS: Exact title results, exact actor results, exact genre results, related title and actor results (if not suggestion)
        "num_results":num_results,
        "explore_sorted":explore_sorted[:10], # Return top 10 related results
        "suggestion_title":suggestion_title,
        "suggestion_type":suggestion_type,
    }

    return render(request, "results.html", context)

def top_movies_page(request):
    reception = Reception.objects.all()
    movies = MovieGenre.objects.all()
    background = Background.objects.all()

    explore = []

    query = request.GET.get("search", None)

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

    if query != None:
        top_movies = [] 
        filtered_top_movies = reception.filter(movie_id__title__icontains=query, avgRatings__gte=7).order_by('-avgRatings', '-numRatings')
        
        # Search by genre
        movies_genres, explore = search_genres(query, explore)
        for movie in movies_genres:
            r = reception.filter(movie_id=movie.movie_id, avgRatings__gte=7).order_by('-avgRatings', '-numRatings')  
            for r_movie in r:
                try:
                    release = background.get(movie_id=movie.movie_id).releaseDate
                except Background.DoesNotExist:
                    release = None

                # Length
                try:
                    length =  background.get(movie_id=movie.movie_id).length
                except Background.DoesNotExist:
                    length = None

                top_movies.append([r_movie, r_movie.avgRatings, release, length])
        
        #Search by Actor
        movies_actors, explore = search_actors(query, explore)
        for movie in movies_actors:
            r = reception.filter(movie_id=movie.movie_id, avgRatings__gte=7).order_by('-avgRatings', '-numRatings')  
            for r_movie in r:
                try:
                    release = background.get(movie_id=movie.movie_id).releaseDate
                except Background.DoesNotExist:
                    release = None

                # Length
                try:
                    length =  background.get(movie_id=movie.movie_id).length
                except Background.DoesNotExist:
                    length = None

                top_movies.append([r_movie, r_movie.avgRatings, release, length])

        #Search by title
        for movie in filtered_top_movies:  
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
        "top_movies": top_movies,                                   
        "query": query
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