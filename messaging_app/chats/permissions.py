from rest_framework import permissions

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
