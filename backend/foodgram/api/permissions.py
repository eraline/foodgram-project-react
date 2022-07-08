from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        cur_user = request.user
        return (cur_user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        cur_user = request.user
        return (obj.author == cur_user or cur_user.is_staff
                or request.method in permissions.SAFE_METHODS)
