from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                         # Home page
    path('register/', views.register_view, name='register'),   # Registration page
    path('login/', views.login_view, name='login'),           # Login page
    path('profile/', views.profile_view, name='profile'),     # Profile page
    path('card-generation/', views.generate_card, name='card_generation'),
    path('generate-card/', views.generate_card_view, name='generate_card'),  # Card Generation page
    path('schedule/', views.schedule_view, name='schedule'),
    path('staff-info/', views.staff_info_view, name='staff_info'),  # Staff/Faculty info
    path('admin-users/', views.view_registered_users, name='admin_users'),  # Custom admin view
    path('logout/', views.logout_view, name='logout_user'),    # Logout URL
]
