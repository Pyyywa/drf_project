import os
from rest_framework.test import APITestCase
from rest_framework import status
from django.forms.models import model_to_dict
from users.models import User
from lms.models import Course, Lesson, Subscription


class LmsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@test.ru")
        self.course = Course.objects.create(
            name="course_name",
            description="course_description",
            preview=os.path.join("lms", "courses", "previews", "shutterstock.webp"),
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            name="lesson_name",
            description="lesson_description",
            link="http://youtube.com/test_lesson.mp4",
            preview=os.path.join("lms", "lessons", "previews", "shutterstock.webp"),
            course=self.course,
            creator=self.user,
        )
        self.subscription = Subscription.objects.create(
            subscriber=self.user, course=self.course
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тестирование создания курса"""
        response = self.client.post("/lms/course/", data=model_to_dict(self.course))
        # Проверяем создание записи
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем содержимое созданной записи
        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "lesson_count": 0,
                "lesson": [],
                "subscription": False,
                "name": "course_name",
                "description": "course_description",
                "preview": response.json()["preview"],
                "owner": self.user.pk,
            },
        )
        # Проверяем наличие записи в базе данных
        self.assertTrue(Course.objects.all().exists())

    def test_list_course(self):
        """Тестирование вывода списка"""
        response = self.client.get("/lms/course/")
        # Проверяем вывод списка записей
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем содержимое выводимой записи
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": response.json()["results"][0]["id"],
                        "lesson_count": response.json()["results"][0]["lesson_count"],
                        "lesson": [
                            {
                                "id": response.json()["results"][0]["lesson"][0]["id"],
                                "name": "lesson_name",
                                "description": "lesson_description",
                                "preview": response.json()["results"][0]["lesson"][0][
                                    "preview"
                                ],
                                "link": "http://youtube.com/test_lesson.mp4",
                                "creator": self.user.pk,
                                "course": response.json()["results"][0]["lesson"][0][
                                    "course"
                                ],
                            }
                        ],
                        "subscription": True,
                        "name": "course_name",
                        "description": "course_description",
                        "preview": response.json()["results"][0]["preview"],
                        "creator": self.user.pk,
                    }
                ],
            },
        )

    def test_detail_course(self):
        """Тестирование вывода курса"""
        response_create = self.client.post(
            "/lms/course/", data=model_to_dict(self.course)
        )
        response_detail = self.client.get(
            f"/lms/course/{response_create.json()['id']}/"
        )
        # Проверяем вывод одной записи
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        # Проверяем содержимое выводимой записи
        self.assertEqual(
            response_detail.json(),
            {
                "id": response_create.json()["id"],
                "lesson_count": response_detail.json()["lesson_count"],
                "lesson": [],
                "subscription": False,
                "name": "course_name",
                "description": "course_description",
                "preview": response_detail.json()["preview"],
                "creator": self.user.pk,
            },
        )

    def test_update_course(self):
        """Тестирование редактирования курса"""
        response_create = self.client.post(
            "/lms/course/", data=model_to_dict(self.course)
        )
        response_patch = self.client.patch(
            f"/lms/course/{response_create.json()['id']}/",
            {
                "name": "course_name_patch",
                "description": "course_description_patch",
            },
        )
        # Проверяем вывод одной записи
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        # Проверяем содержимое редактированной записи
        self.assertEqual(
            response_patch.json(),
            {
                "id": response_patch.json()["id"],
                "lesson_count": response_patch.json()["lesson_count"],
                "lesson": [],
                "subscription": False,
                "name": "course_name_patch",
                "description": "course_description_patch",
                "preview": response_patch.json()["preview"],
                "creator": self.user.pk,
            },
        )

    def test_delete_course(self):
        """Тестирование удаления курса"""
        response_create = self.client.post(
            "/lms/course/", data=model_to_dict(self.course)
        )
        response_delete = self.client.delete(
            f"/lms/course/{response_create.json()['id']}/"
        )
        # Проверяем удаление
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_subscriber(self):
        """Тестирование создания/удаления подписки"""
        response = self.client.post(
            "/lms/subscription/", data={"course_id": self.course.pk}
        )
        # Проверяем создание записи
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем сообщение
        self.assertIn(
            response.json()["message"], ["подписка удалена", "подписка добавлена"]
        )


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create(email="user_1@test.ru")
        self.course_1 = Course.objects.create(
            name="course_name_1",
            description="course_description_1",
            preview=os.path.join("lms", "courses", "previews", "shutterstock.webp"),
            owner=self.user_1,
        )
        self.lesson_1 = Lesson.objects.create(
            name="name_lesson_1",
            description="description_lesson_1",
            link="http://youtube.com/test_lesson.mp4",
            preview=os.path.join("lms", "lessons", "previews", "shutterstock.webp"),
            course=self.course_1,
            creator=self.user_1,
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user_1)

    def test_create_lesson(self):
        """Тестирование создания урока"""

        response = self.client.post(
            "/lms/lesson/create/", data=model_to_dict(self.lesson_1)
        )

        # Проверяем создание записи
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем содержимое созданной записи
        self.assertEqual(
            response.json(),
            {
                "id": response.json()["id"],
                "name": "name_lesson_1",
                "description": "description_lesson_1",
                "preview": response.json()["preview"],
                "link": "http://youtube.com/test_lesson.mp4",
                "creator": self.user_1.pk,
                "course": response.json()["course"],
            },
        )

        # Проверяем наличие записи в базе данных
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lesson(self):
        """Тестирование вывода списка"""

        response = self.client.get("/lms/lesson/")

        # Проверяем вывод списка записей
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем содержимое выводимой записи
        self.assertEqual(
            response.json(),
            {
                "count": response.json()["count"],
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": response.json()["results"][0]["id"],
                        "name": "name_lesson_1",
                        "description": "description_lesson_1",
                        "preview": response.json()["results"][0]["preview"],
                        "link": "http://youtube.com/test_lesson.mp4",
                        "creator": self.user_1.pk,
                        "course": response.json()["results"][0]["course"],
                    }
                ],
            },
        )

    def test_detail_lesson(self):
        """Тестирование вывода урока"""

        response_create = self.client.post(
            "/lms/lesson/create/", data=model_to_dict(self.lesson_1)
        )

        response_detail = self.client.get(
            f"/lms/lesson/{response_create.json()['id']}/"
        )

        # Проверяем вывод одной записи
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)

        # Проверяем содержимое выводимой записи
        self.assertEqual(
            response_detail.json(),
            {
                "id": response_detail.json()["id"],
                "name": "name_lesson_1",
                "description": "description_lesson_1",
                "preview": response_detail.json()["preview"],
                "link": "http://youtube.com/test_lesson.mp4",
                "creator": self.user_1.pk,
                "course": response_detail.json()["course"],
            },
        )

    def test_update_lesson(self):
        """Тестирование редактирования урока"""

        response_create = self.client.post(
            "/lms/lesson/create/", data=model_to_dict(self.lesson_1)
        )

        response_patch = self.client.patch(
            f"/lms/lesson/update/{response_create.json()['id']}/",
            {
                "name": "name_lesson_1_patch",
                "description": "description_lesson_1_patch",
                "link": "http://youtube.com/test_lesson_1_patch.mp4",
            },
        )

        # Проверяем вывод одной записи
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

        # Проверяем содержимое редактированной записи
        self.assertEqual(
            response_patch.json(),
            {
                "id": response_patch.json()["id"],
                "name": "name_lesson_1_patch",
                "description": "description_lesson_1_patch",
                "preview": response_patch.json()["preview"],
                "link": "http://youtube.com/test_lesson_1_patch.mp4",
                "creator": self.user_1.pk,
                "course": response_patch.json()["course"],
            },
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        response_create = self.client.post(
            "/lms/lesson/create/", data=model_to_dict(self.lesson_1)
        )

        response_delete = self.client.delete(
            f"/lms/lesson/delete/{response_create.json()['id']}/"
        )

        # Проверяем удаление
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
