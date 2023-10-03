from django.db import models


class Robot(models.Model):
    """
    Класс для представления роботов.

    Метод __str__ возвращает данные о серийном номере и дате производства:
        "R2-D2 (2200-02-20)"

    Сортировка производится по возрастанию ID.

    Атрибуты:
        - model: str
            - название модели робота
        - version: str
            - название версии робота
        - serial: str
            - название серийного номера робота
            - автоматически генерируется из модели и версии
        - created: str
            - дата производства робота
    """
    model = models.CharField(
        max_length=2,
    )
    version = models.CharField(
        max_length=2,
    )
    serial = models.CharField(
        max_length=5,
    )
    created = models.DateTimeField(
    )

    class Meta:
        verbose_name = 'Робот'
        verbose_name_plural = 'Роботы'
        ordering = ('id',)

    def save(self, *args, **kwargs):
        """
        Переопределяет сохранение объекта модели:
            - приводит поля model и version к верхнему регистру
            - на основании полей model и version генерирует значение serial
        """
        self.model = self.model.upper()
        self.version = self.version.upper()
        self.serial = f'{self.model}-{self.version}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.serial} ({self.created})'
