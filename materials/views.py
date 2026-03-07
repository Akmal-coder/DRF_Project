from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner, IsOwnerOrStaff
from materials.paginators import MaterialsPagination


def api_root(request):
    """Корневая страница API"""
    return JsonResponse({
        'message': 'Добро пожаловать в API DRF Project',
        'endpoints': {
            'admin': '/admin/',
            'api_root': '/api/',
            'courses': '/api/courses/',
            'lessons': '/api/lessons/',
        }
    })


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса с разграничением прав"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination  # Добавляем пагинацию

    def get_queryset(self):
        """Фильтруем queryset в зависимости от прав пользователя"""
        user = self.request.user

        # Модераторы и админы видят все курсы
        if user.groups.filter(name='Модераторы').exists() or user.is_staff:
            return Course.objects.all()

        # Обычные пользователи видят только свои курсы
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        # Действия, доступные всем авторизованным пользователям
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]

        # Создание курса - только не модераторы (обычные пользователи)
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]

        # Обновление курса - модераторы или владелец
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]

        # Удаление курса - только владелец (не модератор)
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator & IsOwner]

        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """При создании курса назначаем владельца"""
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    """Generic view для получения списка уроков и создания нового"""
    serializer_class = LessonSerializer
    pagination_class = MaterialsPagination  # Добавляем пагинацию

    def get_queryset(self):
        """Фильтруем queryset в зависимости от прав пользователя"""
        user = self.request.user


        if user.groups.filter(name='Модераторы').exists() or user.is_staff:
            return Lesson.objects.all()


        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """Разные права для разных методов"""
        if self.request.method == 'GET':

            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == 'POST':
            # Создание урока - только не модераторы
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        return super().get_permissions()

    def perform_create(self, serializer):
        """При создании урока назначаем владельца"""
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Generic view для получения, обновления и удаления урока"""
    serializer_class = LessonSerializer

    def get_queryset(self):
        """Фильтруем queryset в зависимости от прав пользователя"""
        user = self.request.user

        # Модераторы и админы видят все уроки
        if user.groups.filter(name='Модераторы').exists() or user.is_staff:
            return Lesson.objects.all()

        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """Разные права для разных методов"""
        if self.request.method == 'GET':
            # Просмотр урока - всем авторизованным
            self.permission_classes = [permissions.IsAuthenticated]

        elif self.request.method in ['PUT', 'PATCH']:
            # Обновление урока - модераторы или владелец
            self.permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]

        elif self.request.method == 'DELETE':
            # Удаление урока - только владелец (не модератор)
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator & IsOwner]

        return super().get_permissions()