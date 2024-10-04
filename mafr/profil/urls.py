from django.urls import path
from . import views

# Used to access views of profil from other apps
# app_name = 'profil'

urlpatterns = [
    # Auth urls
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logout_view, name='logout'),

    # Profile completion after registration
    path('ct_profile', views.complete_talent_profile, name='complete_talent_profile'),
    path('ce_profile', views.complete_employer_profile, name='complete_employer_profile'),
    
    # Home page
    path('', views.home, name='home'),

    # User profile
    path('profile/<int:user_id>', views.visit_profile, name='visit_profile'),
    path('myprofile', views.myprofile, name='myprofile'),
    # path('myprofile/update', views.update_profile, name='update_profile'),

]
