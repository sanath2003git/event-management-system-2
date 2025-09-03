from django.urls import path
from . import views

urlpatterns = [
     path('signup/', views.signup_view, name='signup'),
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('organizer-dashboard/', views.organizer_dashboard_view, name='organizer_dashboard'),
     path('attendee-dashboard/', views.attendee_dashboard_view, name='attendee_dashboard'),
     path('profile/', views.user_profile, name='profile'),
]