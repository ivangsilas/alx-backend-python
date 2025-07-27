from rest_framework import permissions
from .models import Conversation
class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Only allow the sender of the message to modify/view.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only allow authenticated users
    - Only participants of the conversation can access it
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Handles Conversation and Message objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False

    def has_object_permission(self, request, view, obj):
        # Only allow participants to view or modify
        if request.method in ["GET", "POST"]:
            return request.user in obj.participants.all()

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()

        return False
