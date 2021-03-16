from django.contrib import admin
from .models import Genre

class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_id','genre_title']
    class Meta:
        model = Genre

admin.site.register(Genre, GenreAdmin)
