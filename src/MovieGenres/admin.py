from django.contrib import admin
from .models import MovieGenre

class MovieGenreAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','genre_id']
    class Meta:
        model = MovieGenre

admin.site.register(MovieGenre, MovieGenreAdmin)
# Register your models here.
