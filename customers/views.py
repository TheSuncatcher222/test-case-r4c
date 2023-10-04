"""
Определяет логику работы эндпоинтов Django приложения 'Customers'.
"""

from django.middleware import csrf
from django.http import JsonResponse

from R4C.core import STATUS_CODE_OK, STATUS_CODE_NOT_ALLOWED


def get_csrf_token(request):
    if request.method != 'GET':
        data: dict[str, str] = {
            'error': f'Method {request.method} is not allowed.'
        }
        status = STATUS_CODE_NOT_ALLOWED
    else:
        csrf_token = csrf.get_token(request)
        data = {'csrf_token': csrf_token}
        status = STATUS_CODE_OK
    return JsonResponse(
        data=data,
        status=status,
    )
