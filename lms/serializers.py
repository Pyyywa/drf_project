from rest_framework.serializers import ModelSerializer, URLField, SerializerMethodField
from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    course = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseCountSerializer(ModelSerializer):
    quantity_lesson = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_quantity_lesson(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ["name", "preview", "desc", "owner", "quantity_lesson", "lessons",]

