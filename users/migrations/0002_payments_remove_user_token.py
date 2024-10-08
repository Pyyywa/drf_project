# Generated by Django 4.2.8 on 2024-09-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_sum",
                    models.PositiveIntegerField(verbose_name="Cумма платежа"),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CASH", "Наличными"),
                            ("TRANSFER", "Перевод на счет"),
                        ],
                        max_length=50,
                        verbose_name="Способ оплаты",
                    ),
                ),
            ],
            options={
                "verbose_name": "платеж",
                "verbose_name_plural": "платежи",
            },
        ),
        migrations.RemoveField(
            model_name="user",
            name="token",
        ),
    ]
