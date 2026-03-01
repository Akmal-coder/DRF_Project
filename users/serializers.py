from rest_framework import serializers
from users.models import Payment
from materials.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = '__all__'