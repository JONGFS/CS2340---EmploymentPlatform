from django.urls import path 
from . import views


app_name = "jobs"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/edit/', views.edit_job, name='edit_job'),
    path('<int:id>/delete/', views.delete_job, name='delete_job'),
    path('<int:id>/apply/', views.apply_job, name='apply_job'),
    path('<int:job_id>/map/', views.job_map_view, name='job_map'),

    path('map/', views.jobs_map_view, name='map'),
    path('api/', views.jobs_api_view, name='api'),

    path('hiring-stages/', views.hiring_stages_view, name='hiring_stages'),
    path('application/<int:application_id>/update-stage/', views.update_application_stage, name='update_application_stage'),
    path('application/<int:application_id>/details/', views.application_details, name='application_details'),

    path('applicants/map/', views.applicants_map_view, name='applicants_map'),
    path('applicants/api/', views.applicants_api_view, name='applicants_api'),

    path('email/<int:candidate_id>/', views.email_candidate_view, name='email_candidate'),
    path('email/<int:candidate_id>/send/', views.send_candidate_email, name='send_candidate_email'),


]
