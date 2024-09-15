from django.urls import path
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from users.views import PaymentsListAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
                  path('user/payment/', PaymentsListAPIView.as_view(), name='user_payment'),
              ] + router.urls
