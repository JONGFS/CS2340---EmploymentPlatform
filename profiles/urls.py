from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("applications/", views.my_applications, name="my_applications"),
    path("candidates/", views.candidate_search, name="candidate_search"),
]
