from django.shortcuts import render
from Movies.models import Movie

# Create your views here.
def home(request): 
    movies = Movie.objects.all() 
    return render(request,'main/index.html',{"movies":movies}) 