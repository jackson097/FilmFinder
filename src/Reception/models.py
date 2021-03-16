from django.db import models
from Movies.models import Movie

class Reception(models.Model):
    movie_id    = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    avgRatings  = models.FloatField()
    numRatings  = models.IntegerField()
