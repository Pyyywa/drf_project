# Generated by Django 4.2.8 on 2024-10-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0006_remove_course_null_remove_lesson_null_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="link",
            field=models.URLField(
                blank=True,
                help_text="Укажите ссылку на видео",
                verbose_name="Ссылка на видео",
            ),
        ),
    ]
