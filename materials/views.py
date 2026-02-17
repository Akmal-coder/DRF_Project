from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from django.http import JsonResponse
from django.shortcuts import redirect

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
    """ViewSet для курса (полный CRUD)"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """Generic view для получения списка уроков и создания нового"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Generic view для получения, обновления и удаления урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
