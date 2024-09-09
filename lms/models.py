from django.db import models
from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="lms/preview", verbose_name="превью", **NULLABLE
    )
    desc = models.TextField(
        *NULLABLE, help_text="Добавьте описание к курсу"
    )
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название урока",
        help_text="Введите название урока",
    )
    view = models.ImageField(upload_to="lms/view", verbose_name="превью", **NULLABLE)
    description = models.TextField(
        *NULLABLE, help_text="Добавьте описание к уроку"
    )
    link = models.URLField(**NULLABLE, verbose_name='Ссылка на видео', help_text='Укажите ссылку на видео')
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="курс", verbose_name="курс"
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки "
