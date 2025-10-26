from django.db import models

class Job(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.TextField()
    skills = models.TextField()
    location = models.TextField()
    salaryRange = models.TextField()
    remote = models.TextField()
    visaSponsorship = models.TextField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + '-' + self.title
class Role(models.Model):
    role = models.TextField()


#class Application(models.Model):
    
#    """Simple model to record a job application from a job seeker."""
#   id = models.AutoField(primary_key=True)
#   job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
#   applicant_name = models.TextField(blank=True)
#   applicant_email = models.TextField(blank=True)
#   cover_letter = models.TextField(blank=True)
#   created_at = models.DateTimeField(auto_now_add=True)
#    
#    def __str__(self):
#        return f"Application {self.id} for Job {self.job_id}"
