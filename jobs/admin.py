from django.contrib import admin
from .models import Job
from profiles.models import Application

admin.site.register(Job)
admin.site.register(Application)

