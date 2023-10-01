from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('@<str:username>/', views.bus, name='bus'),
    path('u/<str:username>/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('@<str:username>/follow/', views.follow, name='follow'),
    path('about/start/register/', views.registerb, name='registerb'),
    path('about/start/', views.startb, name='startb'),
    path('@<str:username>/report/', views.report, name='report'),
    path('about/staff/', views.staff, name='staff'),
    path('@<str:username>/block/', views.block, name='block'),
    path('about/', views.about, name='about'),
]
