from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Права модератора"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsCreator(BasePermission):
    """Права владельца"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        return False
