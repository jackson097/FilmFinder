from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','title']
    class Meta:
        model = Movie

admin.site.register(Movie, MovieAdmin)
# admin.site.register(Movie)
