from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lms.models import Course, Lesson, Subscription
from lms.validators import LinkValidator


class CourseSerializer(ModelSerializer):
    course = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field="link")]


class CourseCountSerializer(ModelSerializer):
    quantity_lesson = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_quantity_lesson(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, obj):
        """Информация о подписке на курс"""
        user = self.context["request"].user.pk
        return bool(Subscription.objects.filter(subscriber_id=user, course_id=obj.pk))

    class Meta:
        model = Course
        fields = "__all__"
