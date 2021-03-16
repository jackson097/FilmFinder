from django.db import models
from Movies.models import Movie

class Audience(models.Model):
    movie_id    = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    region      = models.CharField(blank=True, null=True, max_length=120)
    language    = models.CharField(blank=True, null=True, max_length=120)
    isAdult     = models.BooleanField(blank=True, null=True)
