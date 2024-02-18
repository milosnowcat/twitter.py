from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('mailverify/', views.mailverify, name='mailverify'),
    path('', views.notifications, name='list'),
    path('strikes/', views.strikes, name='strikes'),
]
