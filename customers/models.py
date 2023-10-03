from django.db import models

CUSTOMER_EMAIL_MAX_LEN: int = 50


class Customer(models.Model):
    """
    Класс для представления покупателей.

    Метод __str__ возвращает электронную почту покупателя:
        "some@email.com"

    Сортировка производится по убыванию ID.

    Атрибуты:
        - email: str
            - электронная почта покупателя
            - валидируется на соответствие формата электронной почты
    """
    email = models.EmailField(
        max_length=CUSTOMER_EMAIL_MAX_LEN,
        unique=True,
    )

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ('id',)

    def str(self):
        return self.email
