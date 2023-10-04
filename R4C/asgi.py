# INFO: Для полного перехода на асинхронный код необходимо также
#       подключить иную базу данных, которая допускает асинхронные обращения
#       (например, MySQL ии PostgreSQL).

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R4C.settings')

application = get_asgi_application()
