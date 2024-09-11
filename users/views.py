from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = (
        "paid_lesson",
        "paid_course",
        "payment_method",
    )
    ordering_fields = ("date_payment",)
