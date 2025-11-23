from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Job,  Recommendation,Profile
from helpers import is_match
from django.contrib.auth.decorators import login_required
from profiles.models import Application
from django.http import JsonResponse, HttpResponseForbidden
from accounts.models import Profile 
from django.views.decorators.http import require_http_methods
import json


def geocode_location(location_string):
    """Convert location string to lat/lng using Nominatim API."""
    import urllib.parse
    import urllib.request
    import ssl
    
    try:
        encoded_location = urllib.parse.quote(location_string)
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={encoded_location}"
        req = urllib.request.Request(url, headers={'User-Agent': 'EmploymentPlatform/1.0'})
        
        # Create SSL context that doesn't verify certificates
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None, None


jobs_data = [
   {'title': 'Software Engineer', 'skills': 'Python, Django, PostgreSQL', 'location': 'San Francisco, CA',
 'salaryRange': '$120,000 - $160,000', 'remote': 'Hybrid', 'visaSponsorship': 'Yes', 'savedCandidateSearch':False,
 'latitude': 37.7749, 'longitude': -122.4194},
 {'title': 'Frontend Developer', 'skills': 'React, JavaScript, CSS, HTML', 'location': 'New York, NY',
 'salaryRange': '$100,000 - $140,000', 'remote': 'Remote', 'visaSponsorship': 'No','savedCandidateSearch':False,
 'latitude': 40.7128, 'longitude': -74.0060},
 {'title': 'Data Scientist', 'skills': 'Python, Machine Learning, SQL, Pandas', 'location': 'Austin, TX',
 'salaryRange': '$110,000 - $150,000', 'remote': 'Yes', 'visaSponsorship': 'Yes','savedCandidateSearch':False,
 'latitude': 30.2672, 'longitude': -97.7431},
 {'title': 'DevOps Engineer', 'skills': 'AWS, Docker, Kubernetes, Jenkins', 'location': 'Seattle, WA',
 'salaryRange': '$130,000 - $170,000', 'remote': 'Hybrid', 'visaSponsorship': 'No','savedCandidateSearch':False,
 'latitude': 47.6062, 'longitude': -122.3321},
 {'title': 'Product Manager', 'skills': 'Agile, Jira, Product Strategy, Communication', 'location': 'Boston, MA',
 'salaryRange': '$115,000 - $155,000', 'remote': 'No', 'visaSponsorship': 'Yes','savedCandidateSearch':False,
 'latitude': 42.3601, 'longitude': -71.0589},
]


def index(request):
    template_data = {}


    if not hasattr(request.user, "profile"):
        return redirect("/accounts/login/")

    # Map the profile role to template role
    template_data["role"] = "Recruiter" if request.user.profile.role == "recruiter" else "Job Seeker"

    # Initialize job listings
    jobs = Job.objects.all()
    if not jobs.exists():
        for job_dict in jobs_data:
            job = Job.objects.create(**job_dict)
            all_user_profiles = Profile.objects.all()
            for user_profile in all_user_profiles:
                if user_profile.role == 'candidate':
                    if is_match(user_profile, job):
                        Recommendation.objects.get_or_create(profile=user_profile, job=job)

    for job in jobs:
        all_user_profiles = Profile.objects.all()
        for user_profile in all_user_profiles:
            if user_profile.role == 'candidate':
                if is_match(user_profile, job):
                    Recommendation.objects.get_or_create(profile=user_profile, job=job)
        
    if request.method == 'POST' and template_data["role"] == "Recruiter":
        title = request.POST.get('title')
        skills = request.POST.get("skills")
        location = request.POST.get("location")
        salary_range = request.POST.get("salaryrange")
        remote_on_site = request.POST.get("remote")
        visa_sponsorship = request.POST.get("visa")

        if all(val and val.strip() for val in [title, skills, location, salary_range, remote_on_site, visa_sponsorship]):
            # Geocode the location
            latitude, longitude = geocode_location(location)

            
            Job.objects.create(
                title=title,
                skills=skills,
                location=location,
                salaryRange=salary_range,
                remote=remote_on_site,
                visaSponsorship=visa_sponsorship,
                latitude=latitude,
                longitude=longitude
            )
            all_user_profiles = Profile.objects.all()
            for user_profile in all_user_profiles:
                  if user_profile.role == 'candidate':
                      if is_match(user_profile, job):
                        Recommendation.objects.get_or_create(profile=user_profile, job=job)
            
            from django.contrib import messages
            messages.success(request, 'Job posting created successfully')
            return redirect('jobs.index')
        else:
            from django.contrib import messages
            messages.error(request, 'Please fill in all fields')

    title_filter = request.GET.get('title')
    skills_filter = request.GET.get("skills")
    location_filter = request.GET.get("location")
    salary_range = request.GET.get("salaryrange")
    remote_on_site = request.GET.get("remote")
    visa_sponsorship = request.GET.get("visa")

    jobs_filtered = list(jobs)

    if template_data["role"] == "Job Seeker":
        if title_filter:
            jobs_filtered = [job for job in jobs_filtered if title_filter.lower() in job.title.lower()]
        if skills_filter:
            jobs_filtered = [job for job in jobs_filtered if skills_filter.lower() in job.skills.lower()]
        if location_filter:
            jobs_filtered = [job for job in jobs_filtered if location_filter.lower() in job.location.lower()]
        if salary_range:
            jobs_filtered = [job for job in jobs_filtered if salary_range.lower() in job.salaryRange.lower()]
        if remote_on_site:
            jobs_filtered = [job for job in jobs_filtered if remote_on_site.lower() in job.remote.lower()]
        if visa_sponsorship:
            jobs_filtered = [job for job in jobs_filtered if visa_sponsorship.lower() in job.visaSponsorship.lower()]

    template_data["jobs"] = jobs_filtered

    template_data.update({
        "title": title_filter or "",
        "skills": skills_filter or "",
        "location": location_filter or "",
        "salaryrange": salary_range or "",
        "remote": remote_on_site or "",
        "visa": visa_sponsorship or ""
    })

    list_of_applied_jobs = []
    applied_job_ids = []
    for job_application in Application.objects.all():
        if job_application.candidate == request.user:
            list_of_applied_jobs.append(job_application.job)
            current_job_id = str(job_application.job).split("-")[0]
            current_job_id = int(current_job_id)
            applied_job_ids.append(current_job_id)
    template_data["applied_jobs_list"] = list_of_applied_jobs

    profile_skills = getattr(request.user.profile, 'skills', '') or ''
    if '\n' in profile_skills:
        user_skills = set(skill.strip().lower() for skill in profile_skills.split('\n') if skill.strip())
    elif ',' in profile_skills:
        user_skills = set(skill.strip().lower() for skill in profile_skills.split(',') if skill.strip())
    else:
        user_skills = set([profile_skills.strip().lower()]) if profile_skills.strip() else set()
    template_data["My_skills"] = user_skills
    
    list_of_recommended_jobs = []
    for job in request.user.profile.get_recommended_jobs():
        if job.id not in applied_job_ids:
            list_of_recommended_jobs.append(job)
    template_data["recommended_jobs"] = list_of_recommended_jobs
    return render(request, 'jobs/index.html',
                  {'template_data' : template_data, 'user': request.user})


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
            
            updated_job = Job.objects.get(id=id)
            
            # If location changed, re-geocode
            if updated_job.location != updated_location:
                latitude, longitude = geocode_location(updated_location)
                updated_job.latitude = latitude
                updated_job.longitude = longitude
            
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
        app, created = Application.objects.get_or_create(job=job, candidate=request.user, applicant_name=name, applicant_email=email, cover_letter=cover)
        from django.contrib import messages
        messages.success(request, 'Your application has been submitted.')
        return redirect('jobs.index')
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

@login_required
def hiring_stages_view(request):
    """Display the hiring stages board for recruiters."""
    if not hasattr(request.user, "profile"):
        return redirect("/accounts/login/")
    
    if request.user.profile.role != "recruiter":
        return redirect('jobs.index')
    
    applications = Application.objects.select_related('job').exclude(status='REJECTED').order_by('-created_at')
    return render(request, 'jobs/hiring_stages.html', {'applications': applications})

@login_required
@require_http_methods(["POST"])
def update_application_stage(request, application_id):
    """Update the stage of an application."""
    if not request.user.profile or request.user.profile.role != "recruiter":
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        new_stage = data.get('stage')
        if new_stage not in [choice[0] for choice in Application.STATUS_CHOICE]:
            return JsonResponse({'success': False, 'error': 'Invalid stage'}, status=400)
        
        application = Application.objects.get(id=application_id)
        application.status = new_stage
        application.save()
        
        return JsonResponse({'success': True})
    except Application.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Application not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def application_details(request, application_id):
    """Get detailed information about an application."""
    if not request.user.profile or request.user.profile.role != "recruiter":
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        application = Application.objects.select_related('job').get(id=application_id)
        data = {
            'applicant_name': application.applicant_name,
            'applicant_email': application.applicant_email,
            'job_title': application.job.title,
            'cover_letter': application.cover_letter,
            'status': application.status,
        }
        return JsonResponse(data)
    except Application.DoesNotExist:
        return JsonResponse({'error': 'Application not found'}, status=404)



@login_required
def applicants_map_view(request):
    """Render the applicants map template — recruiter-only."""
    if not hasattr(request.user, "profile"):
        return redirect("/accounts/login/")
    if request.user.profile.role != "recruiter":
        # Non-recruiters should not access this page
        return redirect('jobs.index')
    return render(request, 'jobs/applicants_map.html', {})


@login_required
def job_map_view(request, job_id):
    """Render the map template with a specific job pinned."""
    job = get_object_or_404(Job, id=job_id)
    # Pass the job ID to the template so JavaScript can highlight this job
    return render(request, 'jobs/job_map.html', {'job': job, 'job_id': job_id})

@login_required
def applicants_api_view(request):
    """
    Return candidate (applicant) locations as JSON for clustering on the map.
    If a candidate has a 'location' string but missing lat/lng, attempt to geocode
    it and save coordinates (simple on-demand geocoding).
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != "recruiter":
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    candidates = Profile.objects.filter(role='candidate')
    data = []

    for cand in candidates:
        lat = cand.latitude
        lon = cand.longitude
        # If they gave a free-text location but no coordinates, try geocoding and save
        if (lat is None or lon is None) and getattr(cand, 'location', None):
            try:
                new_lat, new_lon = geocode_location(cand.location)
                # If geocoding succeeded, save to model
                if new_lat is not None and new_lon is not None:
                    cand.latitude = new_lat
                    cand.longitude = new_lon
                    cand.save(update_fields=['latitude', 'longitude'])
                    lat, lon = new_lat, new_lon
            except Exception as e:
                # Ignore geocoding failures here — frontend will skip empty coords
                print(f"Geocode fail for profile {cand.user.username}: {e}")
        
        if lat is not None and lon is not None:
            data.append({
                'username': cand.user.username,
                'display_name': f"{cand.user.first_name} {cand.user.last_name}".strip() or cand.user.username,
                'id': cand.user.id,
                'location': cand.location or "",
                'latitude': lat,
                'longitude': lon,
                'headline': cand.headline or "",
                'skills': cand.skills or "",
            })
    return JsonResponse({'candidates': data})


from django.core.mail import send_mail
from django.conf import settings

@login_required
def email_candidate_view(request, candidate_id):
    if request.user.profile.role != "recruiter":
        return HttpResponseForbidden("Only recruiters can send emails")

    candidate = Profile.objects.get(user__id=candidate_id)
    
    return render(request, "jobs/email_candidate.html", {
        "candidate": candidate
    })

@login_required
def send_candidate_email(request, candidate_id):
    if request.user.profile.role != "recruiter":
        return HttpResponseForbidden("Unauthorized")

    candidate = Profile.objects.get(user__id=candidate_id)

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not subject or not message:
            return JsonResponse({"success": False, "error": "Missing fields"}, status=400)

        # Send email using your Django email backend
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,   # gmail account
            [candidate.user.email],        # send TO candidate
            fail_silently=False,
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=405)


@login_required
def delete_job(request, id):
    """Delete a job posting - only accessible to superusers."""
    if not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'You do not have permission to delete job postings.')
        return redirect('jobs.index')
    
    job = get_object_or_404(Job, id=id)
    
    if request.method == 'POST':
        job.delete()
        from django.contrib import messages
        messages.success(request, f'Job posting "{job.title}" has been successfully deleted.')
        return redirect('jobs.index')
    
    # If GET request, render confirmation page
    return render(request, 'jobs/delete_job.html', {'job': job})
