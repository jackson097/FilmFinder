from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ['job_id','job_title','character']
    class Meta:
        model = Job

admin.site.register(Job, JobAdmin)
