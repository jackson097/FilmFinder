from django.contrib import admin
from .models import Background

class BackgroundAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','releaseDate', 'length']
    class Meta:
        model = Background

admin.site.register(Background, BackgroundAdmin)
