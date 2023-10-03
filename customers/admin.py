from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Robot.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID (pk)
            - электронная почта (email)
        - search_fields (tuple) - список полей для поиска объектов:
            - электронная почта (email)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'email',
    )
    search_fields = (
        'email',
    )
    list_per_page = 15


admin.site.register(Customer, CustomerAdmin)
