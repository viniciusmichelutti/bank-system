from django.test import TestCase

from accounts.account_gateway import create_account, get_account_by_number, update_account
from accounts.models import Account


class CreateAccountTests(TestCase):
    def test_create_an_account_and_return_as_dict(self):
        number = 200
        balance = 55

        account = create_account(number=number, balance=balance)

        self.assertEqual(number, account['number'])
        self.assertEqual(balance, account['balance'])


class GetAccountByNumberTests(TestCase):
    def test_return_account_found_by_number(self):
        account_number = 99
        account = create_account(number=account_number, balance=33)

        account_found = get_account_by_number(account_number)

        self.assertEqual(account, account_found)

    def test_return_none_if_no_account_found(self):
        account_found = get_account_by_number(99)

        self.assertIsNone(account_found)


class UpdateAccountTests(TestCase):
    def test_update_account(self):
        account_id = create_account(number=123, balance=30)['id']
        new_balance = 99

        updated_rows = update_account(account_id, balance=new_balance)

        self.assertEqual(1, updated_rows)
        updated_account = Account.objects.get(id=account_id)
        self.assertEqual(new_balance, updated_account.balance)
