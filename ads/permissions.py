from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    message = "Вы не можете редактировать чужие элементы"

    def has_object_permission(self, request, view, obj):



        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "author"):
            owner = obj.author
        else:
            raise Exception('Не подходящие данные')
        return owner == request.user

class IsStaff(BasePermission):
    message = "Вы не админ/модератор"

    def has_object_permission(self, request, view, obj):
        return request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]