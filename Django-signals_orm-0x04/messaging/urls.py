from django.urls import path
from .views import delete_user
from .views import UnreadMessagesAPIView

urlpatterns = [
    path('delete-account/', delete_user, name='delete_account'),
    path('unread-messages/', UnreadMessagesAPIView.as_view(), name='unread_messages_api'),
]
