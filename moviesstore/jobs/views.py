from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Role

'''
jobs = [
    {
        'id': 1, "Title": "Manager", 
        "Skills": "Good at PR, Soft skills, AI, Communication, Leadership",
        "Location": "Atlanta, Georgia", 
        "SalaryRange": "200 to 300 thousand", 
        "remote": "on-site",  
        "visasponsorship": "Yes"
    },

    {
        'id': 2, "Title": "Worker", 
        "Skills": "Good at PR, Soft skills, AI, can follow directions, and listen",
        "Location": "Atlanta, Georgia", 
        "SalaryRange": "20 dollars per day", 
        "remote": "on-site",  
        "visasponsorship": "Yes"
    },

    {
        'id': 3, "Title": "Software Engineer", 
        "Skills": "Python, Django, REST APIs, Problem-solving, Teamwork", 
        "Location": "New York, New York", 
        "SalaryRange": "90 to 120 thousand", 
        "remote": "hybrid", 
        "visasponsorship": "No"
    },

    {
        'id': 4, "Title": "Data Scientist", 
        "Skills": "Python, Machine Learning, AI, Statistics, Communication", 
        "Location": "San Francisco, California", 
        "SalaryRange": "120 to 150 thousand", 
        "remote": "remote", 
        "visasponsorship": "Yes"
    },

    {
        'id': 5, "Title": "Manager", 
        "Skills": "Leadership, Negotiation, PR, Strategic Planning", 
        "Location": "Chicago, Illinois", 
        "SalaryRange": "180 to 250 thousand", 
        "remote": "on-site", 
        "visasponsorship": "No"
    },

    {
        'id': 6, "Title": "UX Designer", 
        "Skills": "Figma, UI Design, Creativity, Communication", 
        "Location": "Austin, Texas", 
        "SalaryRange": "70 to 100 thousand", 
        "remote": "hybrid", 
        "visasponsorship": "No"
    },

    {
        'id': 7, "Title": "Software Engineer", 
        "Skills": "Java, Spring Boot, SQL, Teamwork", 
        "Location": "Atlanta, Georgia", 
        "SalaryRange": "80 to 110 thousand", 
        "remote": "on-site", 
        "visasponsorship": "Yes"
    },

    {
        'id': 8, "Title": "Worker", 
        "Skills": "Physical labor, Attention to detail, Safety, Listening", 
        "Location": "Houston, Texas", 
        "SalaryRange": "15 dollars per hour", 
        "remote": "on-site", 
        "visasponsorship": "No"
    },

    {
        'id': 9, "Title": "Data Scientist", 
        "Skills": "R, SQL, Data Visualization, Communication", 
        "Location": "Boston, Massachusetts", 
        "SalaryRange": "100 to 130 thousand", 
        "remote": "remote", 
        "visasponsorship": "Yes"
    },

    {
        'id': 10, "Title": "HR Manager", 
        "Skills": "Recruitment, Soft skills, Leadership, Conflict resolution", 
        "Location": "Miami, Florida", 
        "SalaryRange": "90 to 140 thousand", 
        "remote": "on-site", 
        "visasponsorship": "No"
    },

    {
        'id': 11, "Title": "Software Engineer", 
        "Skills": "C++, Algorithms, Problem-solving, AI", 
        "Location": "Seattle, Washington", 
        "SalaryRange": "100 to 140 thousand", 
        "remote": "remote", 
        "visasponsorship": "Yes"
    },

    {
        'id': 12, "Title": "Worker", 
        "Skills": "Teamwork, Safety, Manual handling, Listening", 
        "Location": "New York, New York", 
        "SalaryRange": "18 dollars per hour", 
        "remote": "on-site", 
        "visasponsorship": "No"
    },

    {
        'id': 13, "Title": "Manager", 
        "Skills": "Leadership, PR, Communication, Project Management", 
        "Location": "Los Angeles, California", 
        "SalaryRange": "150 to 220 thousand", 
        "remote": "hybrid", 
        "visasponsorship": "Yes"
    },

    {
        'id': 14, "Title": "Data Analyst", 
        "Skills": "SQL, Excel, Tableau, Communication", 
        "Location": "Chicago, Illinois", 
        "SalaryRange": "60 to 90 thousand", 
        "remote": "remote", 
        "visasponsorship": "No"
    },

    {
        'id': 15, "Title": "UX Designer", 
        "Skills": "Adobe XD, Wireframing, User research, Creativity", 
        "Location": "San Diego, California", 
        "SalaryRange": "65 to 95 thousand", 
        "remote": "hybrid", 
        "visasponsorship": "Yes"
    },
]
'''

def index(request):
    # get the request that tells job seeker or recuiter
    # add it to template data
    template_data = {}
    job_seeker_remove_filters = False

    jobs = Job.objects.all()
    db_role = Role.objects.get(id = 1)


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


def apply_job(request, id):
    """Handle a job seeker applying to a job. Accepts POST with optional name, email, cover_letter."""
    job = get_object_or_404(Job, id=id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cover = request.POST.get('cover_letter', '')
        # Create application record
        from .models import Application
        Application.objects.create(job=job, applicant_name=name, applicant_email=email, cover_letter=cover)
        # Add a success message and redirect back to jobs index
        from django.contrib import messages
        messages.success(request, 'Your application has been submitted.')
        return redirect('jobs.index')
    # If GET, show a minimal apply form template (could be modal in future)
    return render(request, 'jobs/apply.html', {'job': job})







