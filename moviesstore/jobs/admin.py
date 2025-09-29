from django.contrib import admin
# ...existing code...
from .models import Job, Role
from profiles.models import Application
# Register your models here.

admin.site.register(Job)
admin.site.register(Role)
admin.site.register(Application)

