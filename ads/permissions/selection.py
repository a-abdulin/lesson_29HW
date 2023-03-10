from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Изменять selection может собственник.'

    def has_object_permission(self, request, view, selection):
        if request.user != selection.owner:
            return False
        return True

