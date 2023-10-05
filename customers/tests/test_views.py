from datetime import datetime

from django.core import mail
from django.test import TestCase

from customers.models import Customer
from customers.signals import notify_customers
from orders.models import Order
from robots.models import Robot


class EmailSendTestCase(TestCase):
    """
    Производит тестирование отправки сообщения пользователям
    при появлении в продаже нового робота с требуемым серийным номером.
    """
    def setUp(self):
        self.serial_1 = 'A1-A1'
        self.serial_2 = 'A2-A2'
        self.serial_3 = 'A3-A3'
        self.serial_4 = 'A3-A3'
        self.created = datetime.strptime(
            '2022-02-20 20:20:20',
            '%Y-%m-%d %H:%M:%S'
        )

        self.customer_1 = Customer.objects.create(email='customer_1@email.com')
        self.customer_2 = Customer.objects.create(email='customer_2@email.com')

        orders_bulk: list[Order] = [
            Order(customer=self.customer_1, robot_serial=self.serial_1),
            Order(customer=self.customer_1, robot_serial=self.serial_2),
            Order(customer=self.customer_2, robot_serial=self.serial_2),
            Order(customer=self.customer_1, robot_serial=self.serial_3),
            Order(customer=self.customer_1, robot_serial=self.serial_3),
        ]
        Order.objects.bulk_create(orders_bulk)

    def test_signal(self):
        """
        Тестирует, что сигнал срабатывает при добавлении объектов модели Robot.

        Внимание! Тестирование отправки непосредственно содержимого сообщения
        проверяется в test_email_local.
        """
        mail.outbox = []
        assert len(mail.outbox) == 0

        assert Order.objects.all().count() == 5
        assert Customer.objects.all().count() == 2

        Robot.objects.create(
            model=self.serial_1[:2],
            version=self.serial_1[:2],
            created=self.created,
        )
        assert Robot.objects.all().count() == 1
        assert Order.objects.all().count() == 4
        assert len(mail.outbox) == 1

        Robot.objects.create(
            model='A4',
            version='A4',
            created=self.created,
        )
        assert Robot.objects.all().count() == 2
        assert Order.objects.all().count() == 4
        assert len(mail.outbox) == 1

        Robot.objects.create(
            model=self.serial_2[:2],
            version=self.serial_2[:2],
            created=self.created,
        )
        assert Robot.objects.all().count() == 3
        assert Order.objects.all().count() == 2
        assert len(mail.outbox) == 3

        Robot.objects.create(
            model=self.serial_3[:2],
            version=self.serial_3[:2],
            created=self.created,
        )
        assert Robot.objects.all().count() == 4
        assert Order.objects.all().count() == 0
        assert len(mail.outbox) == 4

        return

    def test_email_local(self):
        """
        Тестирует, что функция отправки писем работает
        и сохраняет письма в файл (отладочный режим).
        """
        # INFO: Pytest создает изолированную среду для тестирования,
        #       которая не имеет доступа даже к отладочному почтовому серверу.
        #       Все письма содержатся в mail.outbox.
        mail.outbox = []
        assert len(mail.outbox) == 0
        notify_customers(
            email_list=['test_email'],
            model=self.serial_1[:2],
            version=self.serial_2[:2],
        )
        assert len(mail.outbox) == 1
        sent_email = mail.outbox[0]
        assert sent_email.subject == 'Робот из вашего списка заказов доступен!'
        assert sent_email.to == ['test_email']
        assert sent_email.body == (
            'Добрый день!\n'
            'Недавно вы интересовались нашим роботом модели A1, версии A2.\n'
            'Этот робот теперь в наличии. Если вам подходит этот вариант '
            '- пожалуйста, свяжитесь с нами!'
        )
        return
