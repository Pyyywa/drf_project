from django.core.management import BaseCommand

from lms.models import Course
from users.models import Payments, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        paid_course = Course.objects.get(pk=3)
        payment = Payments.objects.create(
            user=user,
            paid_course=paid_course,
            payment_sum=4500,
            payment_method='CASHLESS'
        )
        payment.save()
