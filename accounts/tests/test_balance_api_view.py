import ujson
from django.test import Client
from django.test.testcases import TestCase

from accounts.models import Account


class BalanceAPIViewTests(TestCase):
    def setUp(self):
        self.base_path = '/balance'
        self.client = Client()

    def test_balance_api_view_from_non_existing_account(self):
        non_existing_account_id = 99
        path_with_non_existing_account = f'{self.base_path}?account_id={non_existing_account_id}'

        response = self.client.get(path_with_non_existing_account)

        self.assertEqual(404, response.status_code)

    def test_balance_api_view_from_existing_account(self):
        existing_account_id = 99
        initial_balance = 30
        Account.objects.create(number=existing_account_id, balance=initial_balance)
        path_with_existing_account = f'{self.base_path}?account_id={existing_account_id}'

        response = self.client.get(path_with_existing_account)

        self.assertEqual(200, response.status_code)
        response_balance = ujson.loads(response.content)
        self.assertEqual(30, response_balance)
