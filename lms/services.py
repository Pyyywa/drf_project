import os
from django.core.mail import send_mail, BadHeaderError
from dotenv import load_dotenv, find_dotenv
from celery.utils.log import get_task_logger
from lms.models import Course


load_dotenv(find_dotenv())
logger = get_task_logger(__name__)


def send_mail_course(subject, message, recipient_list, course_id: int):
    """
    Отправка электронного письма.
    :object subject: Тема письма, str.
    :object message: Текст письма, str.
    :object recipient_list: Список адресов электронной почты клиентов, list[str].
    :object course_id: id курса, int.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            from_email=os.getenv("EMAIL_HOST_USER"),
            fail_silently=False,
        )
        Course.objects.filter(id=course_id).update(is_mailing=True)
        logger.info("status_attempt: 200, server_response: OK")
    except BadHeaderError as err:
        logger.info(f"status_attempt: 500, server_response: {str(err)}")
    except ValueError as err:
        logger.info(f"status_attempt: 400, server_response: {str(err)}")
