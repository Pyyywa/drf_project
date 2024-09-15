from django.contrib.auth.models import AbstractUser
from django.db import models
from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")

    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="avatar", **NULLABLE
    )
    phone = models.CharField(
        max_length=10,
        verbose_name="phone number",
        **NULLABLE,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=50, verbose_name="country", help_text="Введите страну", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    method_choices = [
        ("CASH", "Наличными"),
        ("TRANSFER", "Перевод на счет"),
    ]

    user = (
        models.ForeignKey(User, on_delete=models.CASCADE, related_name="Пользователь"),
    )
    date_payment = (
        models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты"),
    )
    paid_course = (
        models.ForeignKey(
            Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
        ),
    )
    paid_lesson = (
        models.ForeignKey(
            Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
        ),
    )
    payment_sum = models.PositiveIntegerField(verbose_name="Cумма платежа")
    payment_method = models.CharField(
        max_length=50, choices=method_choices, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

    def __str__(self):
        return (
            f"{self.user}: {self.paid_course if self.paid_course else self.paid_lesson}"
        )
