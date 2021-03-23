from django.contrib import admin
from .models import Audience

class AudienceAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','region','language','isAdult']
    class Meta:
        model = Audience

admin.site.register(Audience, AudienceAdmin)
