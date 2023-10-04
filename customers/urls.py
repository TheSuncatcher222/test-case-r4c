"""
Добавляет эндпоинты приложения Customers:
    - get_csrf_token: при GET запросе отправляет JsonResponse c CSRF токеном
"""

from django.urls import path

from .views import get_csrf_token

urlpatterns = [
    # INFO: При запросе осуществления небезопасной операции (POST запрос на
    #       добавление робота) клиенту необходимо иметь CSRF токен.
    #       В отличие от использования Django форм, у которых CSRF проверка
    #       внедряется в HTML-форму ({% csrf_token %}) и сохраняется в cookies
    #       при отправке формы на сайт, пользователям REST клиентов необходимо
    #       получать токен вручную.
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
]
