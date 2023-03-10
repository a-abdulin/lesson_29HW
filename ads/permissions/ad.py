from rest_framework import permissions

from ads.models import User


class IsADOwner(permissions.BasePermission):
    message = 'Изменять объявление может только собственник, администратор или модератор'

    def has_object_permission(self, request, view, ads):
        if request.user == ads.author_id or request.user.role in (User.ADMIN, User.MODERATOR):
            return True
        return False

