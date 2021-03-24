from django.contrib import admin
from .models import Movie, MovieGenre, MoviePerson

class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_id','title']
    class Meta:
        model = Movie

admin.site.register(Movie, MovieAdmin)

class MovieGenreAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','genre_id']
    class Meta:
        model = MovieGenre

admin.site.register(MovieGenre, MovieGenreAdmin)

class MoviePersonAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','person_id']
    class Meta:
        model = MoviePerson

admin.site.register(MoviePerson, MoviePersonAdmin)
