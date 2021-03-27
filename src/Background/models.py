from django.db import models
from Movies.models import Movie

class Background(models.Model):
    movie_id    = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    releaseDate = models.CharField(max_length=20, blank=True, null=True)
    length      = models.CharField(max_length=20, blank=True, null=True)

