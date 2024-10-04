from django.contrib import admin
from users.models import Payments


@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payer",
        "paid_course",
        "date_payment",
        "payment_sum",
        "payment_method",
    )

    search_fields = (
        "payer",
        "paid_course",
    )
