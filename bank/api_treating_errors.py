from http import HTTPStatus

from django.db import transaction
from django.http import HttpResponse

from core.exceptions import EntityNotFound


def api_treating_errors(funct):
    def api_treating_errors_wrapper(*args, **kwargs):
        try:
            with transaction.atomic():
                return funct(*args, **kwargs)
        except EntityNotFound:
            return HttpResponse(status=HTTPStatus.NOT_FOUND, content=0, content_type='application/json')
    return api_treating_errors_wrapper
