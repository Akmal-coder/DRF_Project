from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверка, является ли пользователь модератором"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь авторизован
        if not request.user.is_authenticated:
            return False

        # Проверяем, состоит ли пользователь в группе "Модераторы"
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь авторизован
        if not request.user.is_authenticated:
            return False

        # Проверяем, что у объекта есть поле owner и оно совпадает с текущим пользователем
        return hasattr(obj, 'owner') and obj.owner == request.user


class IsOwnerOrStaff(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем объекта или админом"""

    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь авторизован
        if not request.user.is_authenticated:
            return False

        # Разрешаем доступ админам
        if request.user.is_staff:
            return True

        # Для курсов и уроков проверяем владельца
        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        return False


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Модераторы могут редактировать, обычные пользователи только читать свои объекты.
    Используется в сочетании с другими permissions.
    """

    def has_permission(self, request, view):
        # Все авторизованные пользователи имеют доступ
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем изменение модераторам
        if request.user.groups.filter(name='Модераторы').exists():
            return True

        # Разрешаем изменение владельцам
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True

        # В остальных случаях запрещаем
        return False