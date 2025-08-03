from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Prefetch
from .models import Message
from .serializers import UnreadMessageSerializer
from rest_framework.response import Response
from django.views.decorators.cache import cache_page




@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log out the user before deleting
    user.delete()
    return redirect('home')  # or another landing page


def get_threaded_conversation(user):
    messages = Message.objects.filter(receiver=user, parent_message__isnull=True).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))

    )
    return messages


@login_required
def user_sent_messages_view(request):
    messages = Message.objects.filter(
        sender=request.user
    ).select_related(
        'receiver'
    ).prefetch_related(
        'replies'
    )

    return render(request, 'messaging/user_sent_messages.html', {'messages': messages})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_messages = Message.unread.for_user(request.user).only('id', 'sender', 'content', 'timestamp')
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)


@method_decorator(cache_page(60), name='dispatch')
class ConversationMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)