import re

from django.core import exceptions
from django.db import models

from customers.models import Customer

SERIAL_PATTERN: str = r'^[0-9A-Z]{2}-[0-9A-Z]{2}$'


def robot_serial_validator(value: str):
    """Производит валидацию серийного номера робота."""
    if not re.fullmatch(pattern=SERIAL_PATTERN, string=value):
        raise exceptions.ValidationError(
            'Укажите корректный серийный номер робота в формате MODEL-SERIAL '
            '(например, R2-D2).'
        )
    return value


class Order(models.Model):
    """
    Класс для представления заказов.

    Метод __str__ возвращает пояснение заказа:
        "Заказ на R2-D2 от some@email.com"

    Сортировка производится по убыванию ID.

    Атрибуты:
        - customer: FK
            - внешний ключ к модели Customer
        - robot_serial: str
            - название серийного номера робота
            - осуществляется валидация по формату записи
    """
    customer = models.ForeignKey(
        Customer,
        related_name='order',
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
    )
    robot_serial = models.CharField(
        verbose_name='Серийный номер робота',
        max_length=5,
        validators=(
            robot_serial_validator,
        ),
    )

    class Meta:
        verbose_name = 'Заказ пользователя'
        verbose_name_plural = 'Заказы пользователей'
        ordering = ('id',)

    def __str__(self):
        return f'Заказ на {self.robot_serial} от {self.customer}'
