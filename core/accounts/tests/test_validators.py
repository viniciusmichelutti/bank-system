from unittest import TestCase

from core.accounts.validators import validate_account
from core.exceptions import AccountNotFound


class ValidateAccountTests(TestCase):
    def test_raise_exception_if_non_existing_account(self):
        non_existing_account_number = 999

        with self.assertRaises(AccountNotFound) as context:
            validate_account(None, non_existing_account_number)

        self.assertEqual('Account 999 not found.', str(context.exception))
