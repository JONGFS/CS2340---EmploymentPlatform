from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from helpers import parse_skills_string

class Profile(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('recruiters', 'Recruiters only'),
        ('private', 'Private'),
    ]
    ROLE_CHOICES = [
        ('candidate', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate', null=True)
    company = models.CharField(max_length=100, blank=True, help_text="Company name (if you are a recruiter)")
    
    location = models.CharField(max_length=255, blank=True, help_text="City, state or address (free text)")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Job seeker profile fields
    headline = models.CharField(max_length=200, blank=True, help_text="Professional headline or title")
    skills = models.TextField(blank=True, help_text="List your skills (one per line or comma-separated)")
    education = models.TextField(blank=True, help_text="Educational background and qualifications")
    work_experience = models.TextField(blank=True, help_text="Work experience and professional history")
    portfolio_link = models.URLField(blank=True, help_text="Link to your portfolio or personal website")
    linkedin_link = models.URLField(blank=True, help_text="LinkedIn profile URL")
    github_link = models.URLField(blank=True, help_text="GitHub profile URL")
    other_links = models.TextField(blank=True, help_text="Other relevant links (one per line)")

    def __str__(self):
        return f"{self.user.username}'s profile"
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None
    def get_recommended_jobs(self):
        return Job.objects.filter(recommendations__profile=self)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Ensure a Profile exists for every User. If the user was just created,
    # create a Profile. If not, create one if missing and save it.
    profile, _ = Profile.objects.get_or_create(user=instance)
    # Save to trigger any profile-level logic or defaults
    try:
        profile.save()
    except Exception:
        # In the unlikely event save fails, avoid crashing the whole request.
        pass

class Job(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.TextField()
    skills = models.TextField()
    location = models.TextField()
    salaryRange = models.TextField()
    remote = models.TextField()
    visaSponsorship = models.TextField()
    savedCandidateSearch = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.id) + '-' + self.title
    def get_recommended_seekers(self):
        return Profile.objects.filter(recommendations__job=self)

class Recommendation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommendations')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recommendations')
    class Meta:
        unique_together = ['profile', 'job']
    def __str__(self):
        return f"{self.profile.user.username} -> {str(self.job.id) + '-' + self.job.title}"
