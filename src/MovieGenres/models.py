from django.db import models
from Movies.models import Movie

class MovieGenre(models.Model):
    movie_id = models.OneToOneField(Movie, null=True, blank=True, on_delete=models.CASCADE)
    genre_id = models.CharField(blank=True, null=True, max_length=120)

    # def __str__(self):
    #     return self.movie_id