from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from users.models import Payment, User, Subscription
from materials.models import Course
from users.serializers import PaymentSerializer, UserSerializer, UserRegistrationSerializer


class PaymentListAPIView(generics.ListAPIView):
    """View для списка платежей с фильтрацией и сортировкой"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Фильтрация по полям
    filterset_fields = {
        'paid_course': ['exact', 'isnull'],
        'paid_lesson': ['exact', 'isnull'],
        'payment_method': ['exact'],
    }

    # Сортировка по дате
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class UserListAPIView(generics.ListAPIView):
    """Список пользователей (только для администраторов)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailAPIView(generics.RetrieveAPIView):
    """Детальная информация о пользователе"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Пользователь может видеть только себя, админ - всех"""
        obj = super().get_object()
        if self.request.user.is_staff or obj == self.request.user:
            return obj
        self.permission_denied(self.request)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Пользователь может редактировать только себя, админ - всех"""
        obj = super().get_object()
        if self.request.user.is_staff or obj == self.request.user:
            return obj
        self.permission_denied(self.request)


class UserDeleteAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Пользователь может удалить только себя, админ - всех"""
        obj = super().get_object()
        if self.request.user.is_staff or obj == self.request.user:
            return obj
        self.permission_denied(self.request)


class UserRegistrationAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Доступно всем

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'user': UserSerializer(user).data,
                    'message': 'Пользователь успешно создан',
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionAPIView(APIView):
    """APIView для управления подпиской на курс"""

    def post(self, request):
        # Получаем пользователя из запроса
        user = request.user

        # Проверяем, что пользователь авторизован
        if not user.is_authenticated:
            return Response(
                {"error": "Необходимо авторизоваться"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Получаем id курса из данных запроса
        course_id = request.data.get('course_id')
        if not course_id:
            return Response(
                {"error": "Не указан ID курса"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем объект курса
        course = get_object_or_404(Course, id=course_id)

        # Получаем подписку пользователя на этот курс
        subscription = Subscription.objects.filter(user=user, course=course)

        # Если подписка есть - удаляем, если нет - создаем
        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
            status_code = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)
