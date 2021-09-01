from django.test import TestCase

from accounts.models import Account
from core.accounts.api import get_balance
from core.exceptions import AccountNotFound


class GetBalanceTests(TestCase):
    def test_get_balance_from_account(self):
        account_number = 999
        Account.objects.create(number=account_number, balance=200)

        balance = get_balance(account_number)

        self.assertEqual(200, balance)

    def test_get_balance_from_non_existing_account(self):
        non_existing_account_number = 999

        with self.assertRaises(AccountNotFound) as context:
            get_balance(non_existing_account_number)

        self.assertEqual('Account 999 not found.', str(context.exception))
