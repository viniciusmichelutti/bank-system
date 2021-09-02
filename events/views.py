from http import HTTPStatus

import ujson
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from bank.api_treating_errors import api_treating_errors
from core.events.api import create_event


class EventAPIView(View):
    @method_decorator(api_treating_errors)
    def post(self, request):
        data = ujson.loads(request.body)
        event = create_event(**data)
        return HttpResponse(status=HTTPStatus.CREATED, content=ujson.dumps(event), content_type='application/json')
