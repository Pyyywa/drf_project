from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from users.models import Payments, User
from lms.models import Course
from users.services import StripeAPI
from users.serializers import PaymentsSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Хеширование пароля при создании пользователя"""
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = (
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("date_payment",)


class StripeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        course_id = kwargs.get("pk")
        course = generics.get_object_or_404(Course, id=course_id)
        user = self.request.user
        stripe_API = StripeAPI()
        # Если записи не существует, то её нужно добавить
        if not Payments.objects.filter(course_pay=course.pk, payer=user.pk).exists():
            price = stripe_API.create_product(course.title, course.price)
            payment = Payments.objects.create(
                payer=user,
                course_pay=course,
                price_id=price["id"],
                product_id=price["product"],
                amount_pay=price["unit_amount"] // 100,
            )
            payment.save()
            session = stripe_API.create_session(payment.price_id)
            print(f"session: {session}")
            Payments.objects.filter(course_pay=course.pk, payer=user.pk).update(
                currency=session["currency"], session_id=session["id"]
            )
            return Response({"url": session.url})
        else:
            # Иначе выводим информацию о существующем платеже
            payment = Payments.objects.get(course_pay=course.pk, payer=user.pk)
            return Response(
                {
                    "message": f"Пользователь {payment.payer} уже оплатил курс "
                    f'"{payment.course_pay}".',
                    "date_pay": payment.date_pay,
                    "amount_pay": payment.amount_pay,
                    "method_pay": payment.method_pay,
                }
            )
