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

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
