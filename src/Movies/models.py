from django.db import models

class Movie(models.Model):
    movie_id    = models.CharField(max_length=120, blank=True, null=True)
    title       = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.movie_id