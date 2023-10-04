"""
Определяет логику работы эндпоинтов Django приложения 'Robots'.
"""

from datetime import datetime
import json
import re

from django.http import JsonResponse

from R4C.core import (
    ROBOT_MODEL_PATTERN,
    STATUS_CODE_CREATED, STATUS_CODE_BAD_REQUEST, STATUS_CODE_NOT_ALLOWED,
)
from .models import Robot


def validate_robot_model_version(value: str) -> str | None:
    """
    Производит валидацию модели или версии робота.

    В случае корректности данных возвращает str объект.
    Иначе - возвращает None."""
    if value is None or not re.fullmatch(ROBOT_MODEL_PATTERN, value):
        return None
    return value


def validate_robot_created(value: str) -> datetime | None:
    """
    Производит валидацию даты создания робота.

    В случае корректности данных возвращает datetime объект.
    Иначе - возвращает None.
    """
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except (TypeError, ValueError):
        return None


def robots_post(request: dict) -> tuple[dict[str, str], int]:
    """
    Принимает файл JSON, который содержит словарь с данными об одном роботе:
        - model
        - version
        - created.
    Проверяет валидность данных и сохраняет объект в базу данных.

    Возвращает: data, status.
    """
    content_type: str = request.META.get('CONTENT_TYPE', '')
    if content_type != 'application/json' or not request.body:
        return (
            {'Invalid Content-Type': 'Expected application/json.'},
            STATUS_CODE_BAD_REQUEST
        )
    robot_data: dict = json.loads(request.body)
    model: str = validate_robot_model_version(robot_data.get('model'))
    version: str = validate_robot_model_version(robot_data.get('version'))
    created: datetime = validate_robot_created(robot_data.get('created'))
    if not all((model, version, created)):
        return (
            {'Bad Request': 'Invalid robot data.'},
            STATUS_CODE_BAD_REQUEST
        )
    # TODO: стоит добавить в модели unique_together = [['model', 'version']],
    #       если роботы не могут быть произведены одновременно
    #       (допускается при существовании параллельного производства),
    #       так как появляется уязвимость DDOS атаки, или вероятность
    #       ошибочного задвоения данных.
    new_robot: Robot = Robot.objects.create(
        model=model,
        version=version,
        created=created,
    )
    return (
        {
            "Succeed": (
                f'Robot {new_robot.serial} ({new_robot.created}) '
                'has been successfully added to the database.')
        },
        STATUS_CODE_CREATED,
    )


def robots_view(request: dict) -> JsonResponse:
    """
    Принимает объект request и передает запрос в нужную
    функцию-обработчик на основание типа HTTP-запроса.

    Возвращает ошибку 405, если метод не разрешен.
    """
    if request.method != 'POST':
        status: int = STATUS_CODE_NOT_ALLOWED
        data: dict[str, str] = {
            'error': f'Method {request.method} is not allowed.'
        }
    else:
        data, status = robots_post(request=request)
    return JsonResponse(
        data=data,
        status=status,
        content_type='application/json; charset=utf-8',
    )
