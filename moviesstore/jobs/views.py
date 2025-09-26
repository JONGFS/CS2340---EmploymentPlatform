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
    template_data = {}
    template_data["title"] = 'Jobs'
    template_data["jobs"] = jobs
    return render(request, 'jobs/index.html',
                  {'template_data' : template_data})
