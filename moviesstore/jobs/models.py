from django.db import models

class Job(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.TextField()
    skills = models.TextField()
    location = models.TextField()
    salaryRange = models.TextField()
    remote = models.TextField()
    visaSponsorship = models.TextField()
    def __str__(self):
        return str(self.id) + '-' + self.title
