from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=120, blank=True)
    education = models.CharField(max_length=60, blank=True)
    skills = models.CharField(max_length=120, blank=True)  # keep as you had it
    work_experience = models.ManyToManyField(Skill, blank=True)
    portfolio_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)

    def __str__(self) -> str:
        return self.user.username

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
    APPLIED = "APPLIED"; REVIEW = "REVIEW"; INTERVIEW = "INTERVIEW"; OFFER = "OFFER"; CLOSED = "CLOSED"
    STATUS_CHOICE = [
        (APPLIED, "Applied"),
        (REVIEW, "Review"),
        (INTERVIEW, "Interview"),
        (OFFER, "Offer"),
        (CLOSED, "Closed"),
    ]

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    note = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICE, default=APPLIED)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "candidate")

    def __str__(self) -> str:
        return f"{self.candidate} → {self.job} [{self.status}]"
