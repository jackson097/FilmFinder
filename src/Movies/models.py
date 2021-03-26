from django.db import models
from Genres.models import Genre
from Person.models import Person

def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class Movie(models.Model):
    movie_id    = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=120, blank=True, null=True)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    overview    = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.movie_id)

class MovieGenre(models.Model):
    movie_id = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.CASCADE)

class MoviePerson(models.Model):
    movie_id    = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    person_id   = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)

