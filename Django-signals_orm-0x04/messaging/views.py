from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Prefetch


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
