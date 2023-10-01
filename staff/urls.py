from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('feed/<int:pk>/', views.offer, name='offer'),
    path('feed/<int:pk>/save/', views.osave, name='osave'),
    path('feed/<int:pk>/delete/', views.odelete, name='odelete'),
    path('social/', views.social, name='social'),
    path('social/<int:pk>/', views.post, name='post'),
    path('social/<int:pk>/save/', views.psave, name='psave'),
    path('social/<int:pk>/delete/', views.pdelete, name='pdelete'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:pk>/', views.inbox, name='inbox'),
    path('chat/<int:pk>/strike/', views.cstrike, name='cstrike'),
    path('chat/<int:pk>/dismiss/', views.cdismiss, name='cdismiss'),
    path('user/', views.user, name='user'),
    path('user/<int:pk>/', views.bus, name='bus'),
    path('user/<int:pk>/u/', views.profile, name='profile'),
    path('user/<int:pk>/strike/', views.ustrike, name='ustrike'),
    path('user/<int:pk>/dismiss/', views.udismiss, name='udismiss'),
    path('business/', views.blist, name='blist'),
    path('business/<int:pk>/', views.bprofile, name='bprofile'),
    path('business/<int:pk>/accept', views.baccept, name='baccept'),
    path('business/<int:pk>/deny', views.bdeny, name='bdeny'),
    path('staff/', views.slist, name='slist'),
    path('staff/<int:pk>/', views.sprofile, name='sprofile'),
    path('staff/<int:pk>/accept', views.saccept, name='saccept'),
    path('staff/<int:pk>/deny', views.sdeny, name='sdeny'),
]
