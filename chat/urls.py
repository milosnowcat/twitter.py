from django.urls import path
from .views import InboxView, UserListsView, MessagesListView, report

app_name = 'chat'

urlpatterns = [
    path('', MessagesListView.as_view(), name='message_list'),
    path('u/', UserListsView.as_view(), name='users_list'),
    path('u/<str:username>/', InboxView.as_view(), name='inbox'),
    path('u/<str:username>/report/', report, name='report'),
]
