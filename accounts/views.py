from http import HTTPStatus

import ujson
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from bank.api_treating_errors import api_treating_errors
from core.accounts.api import get_balance


class BalanceAPIView(View):
    @method_decorator(api_treating_errors)
    def get(self, request):
        balance = get_balance(request.GET.get('account_id'))
        return HttpResponse(status=HTTPStatus.OK, content=ujson.dumps(balance), content_type='application/json')
