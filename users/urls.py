from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import (
    PaymentListAPIView,
    PaymentCreateAPIView,
    PaymentSuccessView,
    PaymentCancelView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
    UserRegistrationAPIView,
    SubscriptionAPIView,
)

urlpatterns = [
    # JWT эндпоинты (доступны всем)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Регистрация (доступна всем)
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),

    # CRUD для пользователей (требуют авторизации)
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),

    # Платежи (требуют авторизации)
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payments/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]