from django.shortcuts import render
from Movies.models import Movie, MovieGenre
from Genres.models import Genre
from Movies.models import MovieGenre

# Create your views here.
def home(request): 
    movies = MovieGenre.objects.all() 
    genres = Genre.objects.all()
    
    context = {
        "obj":movies,
        "genre":genres
    }
    return render(request,'search.html', context) 
