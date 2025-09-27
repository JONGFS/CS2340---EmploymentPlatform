from django.shortcuts import render

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

def index(request):
    # get the request that tells job seeker or recuiter
    # add it to template data
    
    role = request.POST.get('role')
    if not role:
        role = "Job Seeker"
    

    title_filter = request.GET.get('title')
    skills_filter = request.GET.get("skills")
    location_filter = request.GET.get("location")
    salary_range = request.GET.get("salaryrange")
    remote_on_site = request.GET.get("remote")
    visa_sponsorship = request.GET.get("visa")
    jobs_filtered = []
    for job in jobs:
        jobs_filtered.append(job)

    if title_filter is not None and title_filter != "":
        ####For every job in jobs filtered 
        new_jobs_filtered = []
        for job in jobs_filtered:
            if title_filter.lower()  in job["Title"].lower():
                new_jobs_filtered.append(job)
        jobs_filtered = new_jobs_filtered
    if skills_filter is not None and skills_filter != "":
        new_jobs_filtered = []
        for job in jobs_filtered:
            if skills_filter.lower()  in job["Skills"].lower():
                new_jobs_filtered.append(job)
        jobs_filtered = new_jobs_filtered
    if location_filter is not None and location_filter != "" :
        new_jobs_filtered = []
        for job in jobs_filtered:
          if location_filter.lower() in job["Location"].lower():
               new_jobs_filtered.append(job)
        jobs_filtered = new_jobs_filtered

    if salary_range is not None and salary_range != "":
        new_jobs_filtered = []
        for job in jobs_filtered:
            if salary_range.lower() in job["SalaryRange"].lower():
                new_jobs_filtered.append(job)
        jobs_filtered = new_jobs_filtered

    if remote_on_site is not None and remote_on_site != "":
        new_jobs_filtered = []
        for job in jobs_filtered:
            if remote_on_site.lower() in job["remote"].lower():
                new_jobs_filtered.append(job)
        jobs_filtered = new_jobs_filtered

    if visa_sponsorship is not None and visa_sponsorship != "":
        new_jobs_filtered = []
        for job in jobs_filtered:
            if visa_sponsorship.lower() in job["visasponsorship"].lower():
                new_jobs_filtered.append(job)
        jobs_filtered = new_jobs_filtered
    
    if role == "Recruiter":
        jobs_filtered = jobs
    
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

    template_data = {}
    template_data["title"] = title_filter
    template_data["skills"] = skills_filter
    template_data["location"] = location_filter
    template_data["salaryrange"] = salary_range
    template_data["remote"] = remote_on_site
    template_data["visa"] = visa_sponsorship


    template_data["jobs"] = jobs_filtered
    template_data["role"] = role
    return render(request, 'jobs/index.html',
                  {'template_data' : template_data})



