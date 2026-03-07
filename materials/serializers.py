from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import validate_youtube_link
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""

    # поле с валидатором
    video_link = serializers.URLField(
        validators=[validate_youtube_link],
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)  # Новое поле

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False