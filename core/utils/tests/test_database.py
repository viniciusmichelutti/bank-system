from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from accounts.models import Account
from core.utils.database import model_as_dict


class ModelAsDictTests(TestCase):
    @patch('django.utils.timezone.now')
    def test_transform_model_object_to_pure_dict(self, mock_now):
        mocked_date = datetime(2020, 10, 10, 10, 10, 10)
        mock_now.return_value = mocked_date
        account = Account.objects.create(number=99, balance=20)

        account_as_dict = model_as_dict(account)

        self.assertEqual({
            'id': 1,
            'number': 99,
            'balance': 20,
            'created_at': mocked_date
        }, account_as_dict)
