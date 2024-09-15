from django.core.management import BaseCommand
from users.models import Payments


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = [
            {
                "payment_sum": 35000,
                "payment_method": "cash",
            },
            {
                "payment_sum": 3000,
                "payment_method": "transfer",
            },
            {
                "payment_sum": 45000,
                "payment_method": "transfer",
            },
        ]

        payment_for_create = []
        for payment_item in payment_list:
            payment_for_create.append(Payments(**payment_item))

        Payments.objects.all().delete()
        Payments.objects.bulk_create(payment_for_create)
