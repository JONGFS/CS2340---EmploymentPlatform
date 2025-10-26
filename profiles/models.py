from django.db import models
from django.conf import settings
from jobs.models import Job
class Skill(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name

#class CandidateProfile(models.Model):
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #headline = models.CharField(max_length=120, blank=True)
    #education = models.CharField(max_length=60, blank=True)
    #skills = models.CharField(max_length=120, blank=True)  # keep as you had it
    #work_experience = models.ManyToManyField(Skill, blank=True)
    #portfolio_url = models.URLField(blank=True)
    #location = models.CharField(max_length=120, blank=True)

    #def __str__(self) -> str:
        #return self.user.username
class CandidateExtras(models.Model):
    profile = models.OneToOneField('accounts.Profile',
                                   on_delete=models.CASCADE,
                                   related_name='extras')
                                   
class JobPosting(models.Model):
    title = models.CharField(max_length=140)
    company = models.CharField(max_length=140)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # recruiter
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} @ {self.company}"

class Application(models.Model):
    APPLIED = "APPLIED"; INTERVIEWING = "INTERVIEWING"; SELECTED = "SELECTED"; REJECTED = "REJECTED"
    STATUS_CHOICE = [
        (APPLIED, "Applied"),
        (INTERVIEWING, "Interviewing"),
        (SELECTED, "Selected for Position"),
        (REJECTED, "Rejected"),
    ]
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.TextField(blank=True)
    applicant_email = models.TextField(blank=True)
    cover_letter = models.TextField(blank=True)
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    note = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICE, default=APPLIED)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "candidate")

    def __str__(self) -> str:
        return f"{self.candidate} → {self.job} [{self.status}]"
