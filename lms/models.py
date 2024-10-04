from django.db import models
import config.settings
from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="lms/courses/previews", verbose_name="превью", **NULLABLE
    )
    description = models.TextField(
        verbose_name="описание", help_text="Добавьте описание к курсу"
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор"
    )
    price = models.PositiveIntegerField(default=1100, **NULLABLE, verbose_name="цена")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="lms/lessons/previews", verbose_name="превью", **NULLABLE
    )
    description = models.TextField(
        verbose_name="описание", help_text="Добавьте описание к уроку"
    )
    link = models.URLField(
        verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lesson", verbose_name="курс"
    )
    creator = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="создатель",
    )
    price = models.PositiveIntegerField(default=1100, **NULLABLE, verbose_name="цена")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки "


class Subscription(models.Model):
    """Модель подписки пользователя на курс"""

    subscriber = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="подписчик",
        related_name="subscriber",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
        **NULLABLE,
        related_name="subscription",
    )

    def __str__(self):
        return f"{self.subscriber}: {self.course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
