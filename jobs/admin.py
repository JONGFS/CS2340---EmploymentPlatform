from django.contrib import admin
from accounts.models import Job, Recommendation
from profiles.models import Application

admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Recommendation)

