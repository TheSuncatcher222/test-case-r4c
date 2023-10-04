import json
from datetime import datetime
from django.test import TestCase, RequestFactory
from ..models import Robot
from ..views import (
    robots_post, robots_view, validate_robot_model_version,
    validate_robot_created
)


class RobotsPostTestCase(TestCase):
    """
    Производит тестирование POST запроса на эндпоинт robots_view.
    Проверяет, что при валидных данных происходит создание робота,
    при невалидных - возвращается соответствующий статус-код.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.MODEL: str = 'R2'
        self.VERSION: str = 'D2'
        self.CREATED: str = '2023-01-01 00:00:01'
        self.VALID_DATA: dict[str, str] = {
            'model': self.MODEL,
            'version': self.VERSION,
            'created': self.CREATED
        }

    def _send_request(self, data: dict, type: str = 'application/json'):
        """
        Посылает POST запрос на эндпоинт /robots/, возвращает ответ сервера.
        """
        json_data: json = json.dumps(data)
        request = self.factory.post(
            '/robots/',
            json_data,
            content_type=type,
        )
        return robots_view(request)

    def test_robot_creation_valid_data(self):
        """
        Проверяет, что при сообщении на эндпоинт валидного JSON происходит
        создание ровного одного объекта модели Robots.
        """
        self.assertFalse(
            Robot.objects.filter(
                model=self.MODEL,
                version=self.VERSION,
                created=self.CREATED,
            ).exists()
        )
        response = self._send_request(self.VALID_DATA)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            1 == Robot.objects.filter(
                model=self.MODEL,
                version=self.VERSION,
                created=self.CREATED,
            ).count()
        )
        return

    def test_robot_creation_invalid_data(self):
        """
        Проверяет, что при сообщении на эндпоинт валидного JSON, но
        некорректного типа content_type возвращается ответ со статусом 400
        и не происходит создания объекта модели Robots.
        """
        self.assertFalse(
            Robot.objects.filter(
                model=self.MODEL,
                version=self.VERSION,
                created=self.CREATED,
            ).exists()
        )
        response = response = self._send_request(
            data=self.VALID_DATA,
            type='application/text',
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Robot.objects.filter(
                model=self.MODEL,
                version=self.VERSION,
                created=self.CREATED,
            ).exists()
        )
        return

    def test_robot_creation_null_data(self):
        """
        Проверяет, что при сообщении на эндпоинт пустого JSON возвращается
        ответ со статусом 400 и не происходит создания объекта модели Robots.
        """
        self.assertFalse(
            Robot.objects.filter(
                model=self.MODEL,
                version=self.VERSION,
                created=self.CREATED,
            ).exists()
        )
        response = self._send_request(data={})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Robot.objects.filter(
                model=self.MODEL,
                version=self.VERSION,
                created=self.CREATED,
            ).exists()
        )
        return

    def test_robot_creation_invalid_model(self):
        """
        Проверяет, что при сообщении на эндпоинт JSON c невалидным полем
        model возвращается ответ со статусом 400 и не происходит создания
        объекта модели Robots.
        """
        invalid_data_model = self.VALID_DATA.copy()
        for model in ('DD2', 'd2', 11, 1):
            invalid_data_model['model'] = model
            Robot.objects.filter(
                model=model,
                version=self.VERSION,
                created=self.CREATED,
            ).exists()
            response = self._send_request(data=invalid_data_model)
            self.assertEqual(response.status_code, 400)
            self.assertFalse(
                Robot.objects.filter(
                    model=model,
                    version=self.VERSION,
                    created=self.CREATED,
                ).exists()
            )
        return

    def test_robot_creation_invalid_version(self):
        """
        Проверяет, что при сообщении на эндпоинт JSON c невалидным полем
        version возвращается ответ со статусом 400 и не происходит создания
        объекта модели Robots.
        """
        invalid_data_version = self.VALID_DATA.copy()
        for version in ('DD2', 'd2', 11, 1):
            invalid_data_version['version'] = version
            Robot.objects.filter(
                model=self.MODEL,
                version=version,
                created=self.CREATED,
            ).exists()
            response = self._send_request(data=invalid_data_version)
            self.assertEqual(response.status_code, 400)
            self.assertFalse(
                Robot.objects.filter(
                    model=self.MODEL,
                    version=version,
                    created=self.CREATED,
                ).exists()
            )
        return

    def test_validate_robot_created(self):
        """
        Проверяет, что при сообщении на эндпоинт JSON c невалидным полем
        created возвращается ответ со статусом 400 и не происходит создания
        объекта модели Robots.
        """
        invalid_data_created = self.VALID_DATA.copy()
        for created in ('InvalidDate', '2023-01-01', '00:00:01', 1):
            invalid_data_created['created'] = created
            json_data = json.dumps(invalid_data_created)
            request = self.factory.post(
                '/robots/',
                json_data,
                content_type='application/json',
            )
            response = robots_view(request)
            self.assertEqual(response.status_code, 400)
        return
