from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers  # Добавлено для ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from users.models import Payment, User, Subscription
from materials.models import Course
from users.serializers import PaymentSerializer, UserSerializer, UserRegistrationSerializer, PaymentCreateSerializer

# Импорты для документации
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

# Импорты для Stripe
from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_checkout_session
)


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


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа через Stripe"""
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        """Создает платеж и получает ссылку на оплату"""
        user = self.request.user

        # Получаем курс или урок для оплаты
        course = serializer.validated_data.get('paid_course')
        lesson = serializer.validated_data.get('paid_lesson')

        # Определяем сумму и название
        if course:
            amount = 1000  # TODO: взять из модели курса
            # Создаем продукт в Stripe
            product_id = create_stripe_product(course.title, course.description or "")
        else:
            amount = 500  # TODO: взять из модели урока
            # Создаем продукт в Stripe
            product_id = create_stripe_product(lesson.title, lesson.description or "")

        if not product_id:
            raise serializers.ValidationError("Ошибка создания продукта в Stripe")

        # Создаем цену в Stripe
        price_id = create_stripe_price(amount, product_id)
        if not price_id:
            raise serializers.ValidationError("Ошибка создания цены в Stripe")

        # Создаем сессию для оплаты
        success_url = "http://localhost:8000/api/payments/success/"
        cancel_url = "http://localhost:8000/api/payments/cancel/"

        payment_url, session_id = create_stripe_checkout_session(
            price_id, success_url, cancel_url
        )

        if not payment_url:
            raise serializers.ValidationError("Ошибка создания сессии оплаты")

        # Сохраняем платеж
        payment = serializer.save(
            user=user,
            amount=amount,
            payment_method='transfer',  # Stripe - это перевод
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_session_id=session_id,
            stripe_payment_url=payment_url,
            payment_status='pending'
        )

        # Добавляем ссылку на оплату в ответ
        self.payment_url = payment_url
        self.session_id = session_id

    def create(self, request, *args, **kwargs):
        """Переопределяем create для возврата ссылки на оплату"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'payment': serializer.data,
                'payment_url': getattr(self, 'payment_url', None),
                'session_id': getattr(self, 'session_id', None),
                'message': 'Платеж создан, перейдите по ссылке для оплаты'
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PaymentSuccessView(APIView):
    """View для успешной оплаты"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Оплата прошла успешно!"})


class PaymentCancelView(APIView):
    """View для отмены оплаты"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Оплата отменена"})


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


@extend_schema(
    request=OpenApiExample(
        'Пример запроса',
        value={'course_id': 1},
        request_only=True
    ),
    responses={
        201: OpenApiExample(
            'Подписка добавлена',
            value={'message': 'Подписка добавлена'},
            response_only=True
        ),
        200: OpenApiExample(
            'Подписка удалена',
            value={'message': 'Подписка удалена'},
            response_only=True
        ),
        401: OpenApiExample(
            'Не авторизован',
            value={'error': 'Необходимо авторизоваться'},
            response_only=True
        ),
        400: OpenApiExample(
            'Не указан ID курса',
            value={'error': 'Не указан ID курса'},
            response_only=True
        ),
    },
    description='Управление подпиской на курс. Если подписка есть - удаляет, если нет - создает.',
    summary='Подписка/отписка на курс'
)
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
