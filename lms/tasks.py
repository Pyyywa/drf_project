from celery import shared_task
from django.utils import timezone
from celery.utils.log import get_task_logger
from config.celery import app
from lms.models import Course, Subscription
from lms.services import send_mail_course
from users.models import User

logger = get_task_logger(__name__)


@shared_task
def send_mail_course_update(date_update_course, name, recipient_list, course_id):
    """
    Отправка электронного письма об обновлении курса, если с момента обновления курса прошло более 4-х часов.
    Асинхронная задача. Запускается во время обновления курса.
    """
    if date_update_course < timezone.localtime(timezone.now()) - timezone.timedelta(
        hours=4
    ):

        send_mail_course(
            subject=f'Обновление курса "{name}"',
            message=f'Курс "{name}", на который Вы подписаны, обновлён!',
            recipient_list=recipient_list,
            course_id=course_id,
        )
    else:
        logger.info(f"Рассылка не проходила. Обновление: {date_update_course}.")


@app.task
def send_mail_course_monitoring(*args, **kwargs):
    """
    Отправка электронного письма об обновлении курса, если с момента обновления курса прошло более 4-х часов.
    Периодическая задача. Запускается при помощи планировщика.
    """

    courses = Course.objects.filter(
        date_update__lt=(
            timezone.localtime(timezone.now()) - timezone.timedelta(hours=4)
        ),
        is_mailing=False,
    )

    if courses.exists():
        for course in courses:
            subscribers = Subscription.objects.filter(course=course.pk)
            recipient_list = []
            for subscriber in subscribers:
                users = User.objects.filter(id=subscriber.subscriber_id)
                for user in users:
                    recipient_list.append(user.email)
            # Отправка писем
            send_mail_course(
                subject=f'Обновление курса "{course.name}"',
                message=f'Курс "{course.name}" обновлён!',
                recipient_list=recipient_list,
                course_id=course.pk,
            )
    else:
        logger.info("Рассылка не проходила. Обновлений не найдено.")
