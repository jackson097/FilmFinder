from django.shortcuts import render
from Movies.models import Movie
from Genres.models import Genre

# Create your views here.
def home(request): 
    movies = Movie.objects.all() 
    genres = Genre.objects.all()
    
    context = {
        "movies":movies,
        "genres":genres
    }

    return render(request,'search.html', context) 