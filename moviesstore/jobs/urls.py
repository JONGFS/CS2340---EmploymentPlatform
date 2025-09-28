from django.urls import path 
from . import views
urlpatterns = [
    path('', views.index, name = 'jobs.index'),
    path('<int:id>/edit/', views.edit_job, name = 'jobs.edit_job'),
    path('<int:id>/apply/', views.apply_job, name='jobs.apply_job'),
]