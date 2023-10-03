from django.contrib import admin

from .models import Robot


class RobotAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Robot.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID робота (pk)
            - модель робота (model)
            - версия робота (version)
            - серия робота (serial)
            - дата производства робота (created)
        - readonly_fields (tuple) - список полей только на отображение:
            - серия робота (serial)
        - list_filter (tuple) - список полей для фильтрации объектов:
            - модель робота (model)
            - версия робота (version)
            - серия робота (serial)
            - дата производства робота (created)
        - search_fields (tuple) - список полей для поиска объектов:
            - модель робота (model)
            - версия робота (version)
            - серия робота (serial)
            - дата производства робота (created)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'pk',
        'model',
        'version',
        'serial',
        'created',
    )
    readonly_fields = (
        'serial',
    )
    list_filter = (
        'model',
        'version',
        'serial',
        'created',
    )
    search_fields = (
        'model',
        'version',
        'serial',
        'created',
    )
    list_per_page = 15


admin.site.register(Robot, RobotAdmin)
