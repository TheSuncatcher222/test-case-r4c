"""
Перечень Django-signals приложения Customers.
"""

# INFO: В официальной документации Django указано, что использование сигналов
#       нужно использовать в последнюю очередь, что связано с ухудшением
#       восприятия кода проекта.
#       От себя: использование сигналов для отправки сообщений при большом
#       трафике на сайте и множестве пользователей в принципе не является
#       хорошей практике. Я бы отдал предпочтение Celery. Ввиду этого
#       появится возможность отправлять письма "в фоновом режиме" асинхронно,
#       и повысится отказоустойчивость сайта в целом. При этом вызов Celery
#       сделал бы в методе save() модели.

from django.core.mail import send_mail
from smtplib import SMTPException
from django.db.models import Count, Q, QuerySet
from django.db.models.signals import post_save

from django.dispatch import receiver

from R4C.settings import DEFAULT_FROM_EMAIL
from robots.models import Robot
from orders.models import Order

email_subject: str = 'Робот из вашего списка заказов доступен!'
email_message = (
    'Добрый день!\n'
    'Недавно вы интересовались нашим роботом модели {model}, версии {ver}.\n'
    'Этот робот теперь в наличии. Если вам подходит этот вариант '
    '- пожалуйста, свяжитесь с нами!'
)


def get_customers_list(robot_serial: str) -> tuple[QuerySet, list[str]] | None:
    """
    Получает серийный номер робота и отфильтровывает по нему объекты
    модели Order.

    Возвращает полученный QuerySet, а также список уникальных email
    для отправления почты.

    Возвращает None, если QuerySet не содержит объектов.
    """
    customers: QuerySet = Order.objects.filter(robot_serial=robot_serial)
    if len(customers) == 0:
        return None, None
    unique_customers = customers.values(
        'customer__email'
    ).annotate(
        count=Count('customer__email')
    )
    email_list: list[str] = [None] * len(unique_customers)
    pointer: int = -1
    for customer in unique_customers:
        pointer += 1
        email_list[pointer] = customer['customer__email']
    return customers, email_list


def notify_customers(
        email_list: list[str], model: str, version: str
        ) -> list[str]: # noqa (E123)
    """
    Отправляет письма указанным адресатам в email_list.

    В случае возникновения ошибки smtplib.SMTPException - запишет email,
    на который не получилось отправить сообщение.

    Возвращает список email, на которые не удалось отправить сообщение.
    """
    cannot_send: list[str] = []
    # INFO: Не использую более оптимизированный в плане открытия всего одного
    #       соединения с почтовым сервером send_mass_mail по причине того, что
    #       адресаты из email_list будут видеть все адреса в поле "Кому:".
    for email in email_list:
        try:
            send_mail(
                subject=email_subject,
                message=email_message.format(model=model, ver=version),
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except SMTPException:
            cannot_send.append(email)
            continue
    return cannot_send


@receiver(signal=post_save, sender=Robot)
def robot_post_save_handler(sender, instance, created, **kwargs):
    """
    Сигнал будет вызываться по окончании выполнения метода save модели Robot.

    Принимает созданный объект модели Robot.
    На основании поля serial фильтрует покупателей Customers,
    которые оставляли заказ на робота именно с этим серийным номером.
    Отсылает уведомляющее сообщение о том, что робот появился в продаже.

    # INFO: бизнес-логика не была указана, текущая приведена в качестве
    #       примера и требует доработок при написания production-кода!
    После этого удаляет объекты заказов во избежание повторной отправки
    сообщений (спама), если сразу несколько роботов с одинаковым серийным
    номером будут доступны для заказа.
    """
    # INFO: при создании модели через Django Admin - будет дополнительно
    #       создан объект LogEntry, строковое значение которого будет:
    #       Добавлено “R2-D2 (2023-20-20 20:20:20+00:00)“
    if not isinstance(instance, Robot):
        return
    customers, email_list = get_customers_list(robot_serial=instance.serial)
    if not email_list:
        return
    cannot_send = notify_customers(
        email_list=email_list,
        model=instance.model,
        version=instance.version
    )
    if cannot_send:
        customers = customers.filter(~Q(serial__in=cannot_send))
    # INFO: Бизнес-логика не указана.
    #       Удаляю записи для исключения спама пользователям.
    customers.delete()
    return
