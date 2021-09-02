from http import HTTPStatus

import ujson
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from accounts.apps import AccountsConfig
from accounts.models import Account
from bank.api_treating_errors import api_treating_errors
from core.accounts.api import get_balance
from events.models import Event


class BalanceAPIView(View):
    @method_decorator(api_treating_errors)
    def get(self, request):
        balance = get_balance(request.GET.get('account_id'))
        return HttpResponse(status=HTTPStatus.OK, content=ujson.dumps(balance), content_type='application/json')


class ResetAPIView(View):
    def post(self, request):
        # This view breaks our standard/architecture/pattern, as it is only useful to restart our data source.
        Event.objects.all().delete()
        Account.objects.all().delete()
        return HttpResponse(status=HTTPStatus.OK, content='OK', content_type='application/json')
