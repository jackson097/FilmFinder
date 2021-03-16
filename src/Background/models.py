from django.db import models
from Movies.models import Movie

class Background(models.Model):
    movie_id    = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    releaseDate = models.DateField(auto_now=False, auto_now_add=False)
    length      = models.IntegerField(null=True, blank=True)

