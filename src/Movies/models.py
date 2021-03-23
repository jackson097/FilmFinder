from django.db import models
from Genres.models import Genre
from Person.models import Person

class Movie(models.Model):
    movie_id    = models.CharField(max_length=120, blank=True, null=True)
    title       = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.movie_id

class MovieGenre(models.Model):
    movie_id = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.CASCADE)

class MoviePerson(models.Model):
    movie_id    = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    person_id   = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
