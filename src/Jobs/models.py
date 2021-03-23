from django.db import models

class Job(models.Model):
    job_id      = models.AutoField(primary_key=True)
    job_title   = models.CharField(max_length=120, blank=True, null=True)
    character   = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return str(self.job_id)