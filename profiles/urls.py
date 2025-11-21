from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("applications/", views.my_applications, name="my_applications"),
    path("candidates/", views.candidate_search, name="candidate_search"),
    path("messages/", views.inbox, name="inbox"),
    path("messages/compose/", views.compose_message, name="compose_message"),
    path("messages/compose/<int:recipient_id>/", views.compose_message, name="compose_message_to"),
    path("messages/email/compose/", views.compose_email, name="compose_email"),
    path("messages/email/compose/<int:recipient_id>/", views.compose_email, name="compose_email_to"),
]
