from django.db import models
from Jobs.models import Job

class Person(models.Model):
    person_id   = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=120, blank=True, null=True, unique=True)
    birthYear   = models.CharField(max_length=120, blank=True, null=True)
    DeathYear   = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return str(self.person_id)

class PersonJob(models.Model):
    person_id   = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    job_id      = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)

