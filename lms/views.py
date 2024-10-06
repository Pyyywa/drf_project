from rest_framework import viewsets, generics
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, CourseCountSerializer
from lms.permissions import IsModerator, IsCreator
from lms.paginators import LmsPaginator
from lms.tasks import send_mail_course_update
from icecream import ic
from users.models import User

ic.disable()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LmsPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseCountSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """Привязка пользователя к курсу"""
        new_course = serializer.save()
        new_course.creator = self.request.user
        new_course.save()

    def get_permissions(self):
        """Ограничения"""
        if self.action in (
            "list",
            "retrieve",
            "update",
            "partial_update",
        ):
            self.permission_classes = [IsCreator | IsModerator]
        if self.action in ("create",):
            self.permission_classes = [~IsModerator]
        if self.action in ("destroy",):
            self.permission_classes = [IsCreator | ~IsModerator]
        return super().get_permissions()

    def perform_update(self, serializer):
        """Отправка сообщений при обновлении курса"""
        update_course = serializer.save()
        update_course.is_mailing = False
        date_update_course = timezone.localtime(update_course.date_update)
        course_id = update_course.pk
        name = update_course.name
        subscribers = Subscription.objects.filter(course=course_id)
        recipient_list = []
        for subscriber in subscribers:
            users = User.objects.filter(id=subscriber.subscriber_id)
            for user in users:
                recipient_list.append(user.email)
        # Отправка письма
        send_mail_course_update.delay(
            date_update_course=date_update_course,
            name=name,
            recipient_list=recipient_list,
            course_id=course_id,
        )
        update_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        course = get_object_or_404(Course, pk=new_lesson.course.pk)
        new_lesson.owner = self.request.user
        course.date_update = timezone.localtime(timezone.now())
        course.is_mailing = False
        course.save()
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsCreator]
    pagination_class = LmsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsCreator | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsCreator | IsModerator]

    def perform_update(self, serializer):
        update_lesson = serializer.save()
        course = get_object_or_404(Course, pk=update_lesson.course.pk)
        course.date_update = timezone.localtime(timezone.now())
        course.is_mailing = False
        course.save()
        update_lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsCreator | ~IsModerator]


class SubscriptionAPIView(APIView):
    """Подписка пользователя на курс"""

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        # Пользователь
        user = self.request.user
        # id курса
        course_id = self.request.data.get("course_id")
        print(course_id)
        # Объект курса из базы
        course_item = generics.get_object_or_404(Course, id=course_id)
        # Объекты подписок по текущему пользователю и курса
        subs_item = Subscription.objects.filter(subscriber=user, course=course_id)
        # Если подписка у пользователя на этот курс есть, то удаляем её.
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет, то создаём её.
        else:
            Subscription.objects.create(subscriber=user, course=course_item)
            message = "подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})
