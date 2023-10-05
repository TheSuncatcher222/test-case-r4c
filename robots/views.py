"""
Определяет логику работы эндпоинтов Django приложения 'Robots'.
"""

from datetime import date, datetime, timedelta

from django.http import JsonResponse, FileResponse
from django.db.models import Q, QuerySet
import pandas

from R4C.core import (
    STATUS_CODE_OK, STATUS_CODE_NOT_ALLOWED, SEVEN_DAYS, EXCEL_FULL_PATH)
from .models import Robot


def create_robots_data() -> bool:
    """
    Создает excel файл сводки производства роботов за неделю
    до текущего момента времени включительно."""
    now: datetime = datetime.now()
    passed_week: date = date.today() - timedelta(days=SEVEN_DAYS)
    robots: QuerySet = Robot.objects.filter(
        Q(created__date__gte=passed_week) & # noqa (W504)
        Q(created__lte=now)
    )
    if robots.count() == 0:
        return False
    robots_frame: pandas.DataFrame = pandas.DataFrame(robots.values())
    summary_data: pandas.DataFrame = robots_frame.groupby(
        ['model', 'version']
    )['id'].count()
    with pandas.ExcelWriter(EXCEL_FULL_PATH, engine='openpyxl') as writer:
        for model_name, robot_data in summary_data.groupby(level=0):
            robot_data.reset_index(
            ).rename(
                columns={
                    'model': 'Модель',
                    'version': 'Версия',
                    'id': 'Количество за неделю',
                }
            ).to_excel(
                writer,
                sheet_name=model_name,
                index=False,
            )
    return True


def download_excel(request: dict) -> JsonResponse:
    """
    Формирует Excel файл со сводкой количества произведенных роботов
    за последние 7 дней.
    """
    if request.method != 'GET':
        return JsonResponse(
            data={'error': f'Method {request.method} is not allowed.'},
            status=STATUS_CODE_NOT_ALLOWED,
            content_type='application/json; charset=utf-8',
        )
    else:
        created: bool = create_robots_data
        if created:
            try:
                excel_file = open(EXCEL_FULL_PATH, 'rb')
                return FileResponse(filename=excel_file, status=STATUS_CODE_OK)
            except FileNotFoundError:
                pass
        return JsonResponse(
            data={'error': 'No robots has been produced last week.'},
            status=STATUS_CODE_OK,
            content_type='application/json; charset=utf-8',
        )
