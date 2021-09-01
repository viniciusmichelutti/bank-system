from decimal import Decimal
from unittest import TestCase

from core.utils.decimal import precision_decimal


class PrecisionDecimalTests(TestCase):
    def test_precision_decimal(self):
        incorrect_number = 20 - 12.37

        exact_number = precision_decimal(incorrect_number)

        self.assertEqual(exact_number, Decimal('7.63'))
