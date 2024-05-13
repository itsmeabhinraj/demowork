from django.urls import path
from . import views

app_name = 'regapp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.login, name='login'),  # Corrected login URL
    path('login/', views.login, name='login'),  # Corrected login URL
    path('logout/', views.logout, name='logout'),  # Corrected login URL

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
