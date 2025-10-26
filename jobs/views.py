from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Role
from django.contrib.auth.decorators import login_required
from profiles.models import Application
from django.http import JsonResponse


jobs_data = [
    {'title': 'Software Engineer', 'skills': 'Python, Django, PostgreSQL', 'location': 'San Francisco, CA',
     'salaryRange': '$120,000 - $160,000', 'remote': 'Hybrid', 'visaSponsorship': 'Yes',
     'latitude': 37.7749, 'longitude': -122.4194},

    {'title': 'Frontend Developer', 'skills': 'React, JavaScript, CSS, HTML', 'location': 'New York, NY',
     'salaryRange': '$100,000 - $140,000', 'remote': 'Remote', 'visaSponsorship': 'No',
     'latitude': 40.7128, 'longitude': -74.0060},

    {'title': 'Data Scientist', 'skills': 'Python, Machine Learning, SQL, Pandas', 'location': 'Austin, TX',
     'salaryRange': '$110,000 - $150,000', 'remote': 'Yes', 'visaSponsorship': 'Yes',
     'latitude': 30.2672, 'longitude': -97.7431},

    {'title': 'DevOps Engineer', 'skills': 'AWS, Docker, Kubernetes, Jenkins', 'location': 'Seattle, WA',
     'salaryRange': '$130,000 - $170,000', 'remote': 'Hybrid', 'visaSponsorship': 'No',
     'latitude': 47.6062, 'longitude': -122.3321},

    {'title': 'Product Manager', 'skills': 'Agile, Jira, Product Strategy, Communication', 'location': 'Boston, MA',
     'salaryRange': '$115,000 - $155,000', 'remote': 'No', 'visaSponsorship': 'Yes',
     'latitude': 42.3601, 'longitude': -71.0589},
]


def index(request):
    # get the request that tells job seeker or recuiter
    # add it to template data
    template_data = {}
    job_seeker_remove_filters = False

    if not hasattr(request.user, "profile"):
        return redirect("/accounts/login/")

    jobs = Job.objects.all()
    db_role, created = Role.objects.get_or_create(id=1, defaults={'role': 'Job Seeker'})
    if not Job.objects.all().exists():
         for job_dict in jobs_data:
            Job.objects.create(**job_dict)
    role = request.POST.get('role')
    if role:
        template_data["role"] = role 
        if role == "Job Seeker":
            job_seeker_remove_filters = True
    else:
        template_data["role"] = db_role.role

    title_filter = request.GET.get('title')
    skills_filter = request.GET.get("skills")
    location_filter = request.GET.get("location")
    salary_range = request.GET.get("salaryrange")
    remote_on_site = request.GET.get("remote")
    visa_sponsorship = request.GET.get("visa")


    jobs_filtered = []
    for job in jobs:
        jobs_filtered.append(job)


    if template_data["role"] == "Job Seeker" and not job_seeker_remove_filters:
        if title_filter is not None and title_filter != "":
            ####For every job in jobs filtered 
            new_jobs_filtered = []
            for job in jobs_filtered:
                if title_filter.lower()  in job.title.lower():
                    new_jobs_filtered.append(job)
            jobs_filtered = new_jobs_filtered
        if skills_filter is not None and skills_filter != "":
            new_jobs_filtered = []
            for job in jobs_filtered:
                if skills_filter.lower()  in job.skills.lower():
                    new_jobs_filtered.append(job)
            jobs_filtered = new_jobs_filtered
        if location_filter is not None and location_filter != "" :
            new_jobs_filtered = []
            for job in jobs_filtered:
                if location_filter.lower() in job.location.lower():
                    new_jobs_filtered.append(job)
            jobs_filtered = new_jobs_filtered

        if salary_range is not None and salary_range != "":
            new_jobs_filtered = []
            for job in jobs_filtered:
                if salary_range.lower() in job.salaryRange.lower():
                    new_jobs_filtered.append(job)
            jobs_filtered = new_jobs_filtered

        if remote_on_site is not None and remote_on_site != "":
            new_jobs_filtered = []
            for job in jobs_filtered:
                if remote_on_site.lower() in job.remote.lower():
                    new_jobs_filtered.append(job)
            jobs_filtered = new_jobs_filtered

        if visa_sponsorship is not None and visa_sponsorship != "":
            new_jobs_filtered = []
            for job in jobs_filtered:
                if visa_sponsorship.lower() in job.visaSponsorship.lower():
                    new_jobs_filtered.append(job)
            jobs_filtered = new_jobs_filtered
        
        if title_filter is None:
            title_filter = ""

        if skills_filter is None:
            skills_filter = ""
        
        
        if location_filter is None:
            location_filter = ""
        
        if salary_range is None:
            salary_range  = ""
        
        if remote_on_site is None:
            remote_on_site = ""

        if visa_sponsorship is None:
            visa_sponsorship = ""
        

        template_data["title"] = title_filter
        template_data["skills"] = skills_filter
        template_data["location"] = location_filter
        template_data["salaryrange"] = salary_range
        template_data["remote"] = remote_on_site
        template_data["visa"] = visa_sponsorship

    
    
    if template_data['role'] == "Job Seeker":
        template_data["jobs"] = jobs_filtered

        
    if template_data['role'] == "Recruiter":
        if title_filter and skills_filter and location_filter and salary_range and remote_on_site and visa_sponsorship:
            if title_filter != "" and skills_filter != "" and location_filter != "" and salary_range != "" and remote_on_site != "" and visa_sponsorship != "":
                new_job = Job()
                new_job.title = title_filter
                new_job.skills = skills_filter
                new_job.location = location_filter
                new_job.salaryRange = salary_range
                new_job.remote = remote_on_site
                new_job.visaSponsorship =  visa_sponsorship
                new_job.save()
        template_data["jobs"]  = Job.objects.all()

    db_role.role = template_data["role"] 
    db_role.save() 
    list_of_applied_jobs = []
    applied_job_ids = []
    for job_application in Application.objects.all():
        if job_application.candidate == request.user:
            list_of_applied_jobs.append(job_application.job)
            current_job_id = str(job_application.job).split("-")[0]
            current_job_id = int(current_job_id)
            applied_job_ids.append(current_job_id)
    template_data["applied_jobs_list"] = list_of_applied_jobs

    profile_skills = request.user.profile.skills
    user_skills = []
    if '/n' in  profile_skills:
        user_skills = set(skill.strip().lower() for skill  in profile_skills.split('\n'))
    else:
        user_skills = set(skill.strip().lower() for skill  in profile_skills.split(','))
    template_data["My_skills"] = user_skills
    
    list_of_recommended_jobs = []
    for job in Job.objects.all():
        job_skills_string = job.skills

        job_skills= []
        if '\n' in job_skills_string:
            job_skills = set(skill.strip().lower() for skill in job_skills_string.split('\n'))
        else:
            job_skills = set(skill.strip().lower() for skill in job_skills_string.split(','))
        
        if (user_skills & job_skills) and (job.id not in applied_job_ids): 
            list_of_recommended_jobs.append(job)
    template_data["recommended_jobs"] = list_of_recommended_jobs
    return render(request, 'jobs/index.html',
                  {'template_data' : template_data})


def edit_job(request, id):
    editjob = get_object_or_404(Job, id=id)
    template_data = {} 
    template_data['editjob'] = editjob 

    if request.method =="POST" :
        updated_title = request.POST.get('title')
        updated_skills = request.POST.get('skills')
        updated_location = request.POST.get('location')
        updated_salary_range = request.POST.get('salaryrange')
        updated_remote_onsite = request.POST.get('remote')
        updated_visa_sponsorship = request.POST.get('visa')

        if updated_title != "" and updated_skills != "" and updated_location != "" and updated_salary_range != "" and updated_remote_onsite != "" and updated_visa_sponsorship != "":
            
            updated_job  = Job.objects.get(id = id)
            updated_job.title = updated_title
            updated_job.skills = updated_skills
            updated_job.location = updated_location
            updated_job.salaryRange = updated_salary_range
            updated_job.remote = updated_remote_onsite
            updated_job.visaSponsorship = updated_visa_sponsorship
            updated_job.save()

            return redirect('jobs.index')
    return render(request, 'jobs/edit_job.html',  {'template_data' : template_data})

@login_required
def apply_job(request, id):
    """Handle a job seeker applying to a job. Accepts POST with optional name, email, cover_letter."""
    job = get_object_or_404(Job, pk=id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cover = request.POST.get('cover_letter', '')
        # Create application record
        app, created = Application.objects.get_or_create(job=job, candidate=request.user, applicant_name=name, applicant_email=email, cover_letter=cover)
        # Add a success message and redirect back to jobs index
        from django.contrib import messages
        messages.success(request, 'Your application has been submitted.')
        return redirect('jobs.index')
    # If GET, show a minimal apply form template (could be modal in future)
    return render(request, 'jobs/apply.html', {'job': job})

def jobs_map_view(request):
    """Render the map template."""
    return render(request, 'jobs/map.html')

def jobs_api_view(request):
    """Return all job postings as JSON for the map."""
    jobs = Job.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    data = []
    for job in jobs:
        data.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'latitude': job.latitude,
            'longitude': job.longitude,
            'skills': job.skills,
            'salaryRange': job.salaryRange,
            'remote': job.remote,
            'visaSponsorship': job.visaSponsorship,
        })
    return JsonResponse({'jobs': data})
