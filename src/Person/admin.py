from django.contrib import admin
from .models import Person, PersonJob

class PersonAdmin(admin.ModelAdmin):
    list_display = ['person_id','name','birthYear','DeathYear']
    class Meta:
        model = Person

admin.site.register(Person, PersonAdmin)

class PersonJobAdmin(admin.ModelAdmin):
    list_display = ['person_id','job_id']
    class Meta:
        model = PersonJob

admin.site.register(PersonJob, PersonJobAdmin)
