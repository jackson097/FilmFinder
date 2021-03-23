from django.db import models

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_title = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return str(self.genre_id)
