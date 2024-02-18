from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('social/', views.social, name='social'),
    path('feed/<int:offer_id>/delete/', views.odelete, name='odelete'),
    path('social/<int:post_id>/delete/', views.delete, name='delete'),
    path('feed/<int:pk>/like/', views.olike, name='olike'),
    path('social/<int:pk>/like/', views.like, name='like'),
    path('feed/<int:pk>/', views.offer, name='offer'),
    path('social/<int:pk>/', views.post, name='post'),
    path('social/topic/<str:name>', views.topics, name='topic'),
    path('feed/topic/<str:name>', views.otopics, name='otopic'),
    path('social/<int:pk>/report/', views.report, name='report'),
    path('feed/<int:pk>/report/', views.oreport, name='oreport'),
    path('feed/<int:pk>/apply/', views.apply, name='apply'),
]
