from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile/<slug:profile_slug>/', views.profile_detail, name='profile_detail'),
    path('follow/', views.follow, name='follow'),
    path('registration/', views.registration, name='registration'),
    path('get_csrf/', views.get_csrf)
]
