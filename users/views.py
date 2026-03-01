from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payment
from users.serializers import PaymentSerializer


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
