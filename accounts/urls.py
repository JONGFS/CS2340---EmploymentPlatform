from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path("login/", views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('privacy/', views.privacy_settings, name='accounts.privacy'),
    # User management moved to Django admin for platform administrators
    # Deprecated: staff-facing manage-users endpoints removed in favor of admin
]
