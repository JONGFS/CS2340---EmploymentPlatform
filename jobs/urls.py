from django.urls import path 
from . import views
urlpatterns = [
    path('', views.index, name = 'jobs.index'),
    path('<int:id>/edit/', views.edit_job, name = 'jobs.edit_job'),
    path('<int:id>/apply/', views.apply_job, name='jobs.apply_job'),
    path('map/', views.jobs_map_view, name='jobs.map'),
    path('api/', views.jobs_api_view, name='jobs.api'),
    path('hiring-stages/', views.hiring_stages_view, name='jobs.hiring_stages'),
    path('application/<int:application_id>/update-stage/', views.update_application_stage, name='jobs.update_application_stage'),
    path('application/<int:application_id>/details/', views.application_details, name='jobs.application_details'),
]