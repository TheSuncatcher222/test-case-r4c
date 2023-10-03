from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Robot.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID заказчика (pk)
            - ID заказчика (customer)
            - серийный номер робота (robot_serial)
        - search_fields (tuple) - список полей для поиска объектов:
            - ID заказчика (customer)
            - серийный номер робота (robot_serial)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'customer_email',
        'robot_serial',
    )
    list_filter = (
        'customer',
        'robot_serial',
    )
    search_fields = (
        'customer',
        'robot_serial',
    )
    list_per_page = 15

    def customer_email(self, obj):
        return obj.customer.email

    customer_email.short_description = 'Email заказчика'


admin.site.register(Order, OrderAdmin)
