from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('recruiters', 'Recruiters only'),
        ('private', 'Private'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    
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

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
