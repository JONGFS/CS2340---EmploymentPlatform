# Generated manually to fix missing fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('candidate', 'Job Seeker'), ('recruiter', 'Recruiter')], default='candidate', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='company',
            field=models.CharField(blank=True, help_text='Company name (if you are a recruiter)', max_length=100),
        ),
    ]

