from django.contrib import admin
from .models import Reception

class ReceptionAdmin(admin.ModelAdmin):
    list_display = ['id','movie_id','avgRatings', 'numRatings']
    class Meta:
        model = Reception

admin.site.register(Reception, ReceptionAdmin)
