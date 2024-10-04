from django.urls import path
from users.apps import UsersConfig

from users.views import (
    UserListAPIView,
    UserRetrieveAPIView,
    UserCreateAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentsListAPIView,
    StripeAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("user/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_get"),
    path("user/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("user/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_retrieve"),
    path("user/payment/", PaymentsListAPIView.as_view(), name="user_payment"),
    path("user/payment/<int:pk>/", StripeAPIView.as_view(), name="course_payment"),
]
