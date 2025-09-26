from django.shortcuts import render

jobs = [

 {
     
     'id': 1, "Title": "Manager", "Skills": "Good at PR, Soft skills, AI, Communication, Leadership",
     "Location": "Atlanta, Georgia", "SalaryRange": "200 to 300 thounsand", "remote": "on-site",  "visasponsorship": "Yes"

 },


 { 
     'id': 2, "Title": "Worker", "Skills": "Good at PR, Soft skills, AI, can follow directions, and listen",
     "Location": "Atlanta, Georgia", "SalaryRange": "20 dollars per day", "remote": "on-site",  "visasponsorship": "Yes"

 },

]
def index(request):
    template_data = {}
    template_data["title"] = 'Jobs'
    template_data["jobs"] = jobs
    return render(request, 'jobs/index.html',
                  {'template_data' : template_data})
