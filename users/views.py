from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payment, User
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
