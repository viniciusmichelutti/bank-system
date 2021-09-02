from decimal import Decimal

from django.test import TestCase

from accounts.models import Account
from core.events.api import create_event
from core.events.enums import EventType
from core.exceptions import AccountNotFound
from events.models import Event


class CreateEventTests(TestCase):
    def test_deposit_event_into_existing_account(self):
        account_number = 20
        initial_balance = 30
        deposit_amount = 20
        destination_account = self._create_account(account_number, initial_balance)

        event = create_event(
            type=EventType.DEPOSIT,
            destination=account_number,
            amount=deposit_amount
        )

        self.assertEqual({"destination": {"id": account_number, "balance": initial_balance + deposit_amount}}, event)
        updated_destination_acc = Account.objects.get(id=destination_account.id)
        self.assertEqual(Decimal('50'), updated_destination_acc.balance)
        self.assertEvent(EventType.DEPOSIT, None, destination_account.id, amount=deposit_amount)

    def test_deposit_event_creating_a_new_account(self):
        account_number = 999
        deposit_amount = 30

        event = create_event(
            type=EventType.DEPOSIT,
            destination=account_number,
            amount=30
        )

        self.assertEqual({"destination": {"id": account_number, "balance": deposit_amount}}, event)

    def test_withdraw_event(self):
        account_number = 1
        origin_account = self._create_account(account_number, balance=20)

        event = create_event(
            type=EventType.WITHDRAW,
            origin=origin_account.number,
            amount=7.39
        )

        self.assertEqual({'origin': {'id': account_number, 'balance': Decimal('12.61')}}, event)
        updated_origin_acc = Account.objects.get(id=origin_account.id)
        self.assertEqual(Decimal('12.61'), updated_origin_acc.balance)
        self.assertEvent(EventType.WITHDRAW, origin_account.id, destination_account_id=None, amount=Decimal('7.39'))

    def test_transfer_event(self):
        origin_account_number = 123
        destination_account_number = 456
        origin_account = self._create_account(origin_account_number, balance=20)
        destination_account = self._create_account(destination_account_number, balance=50)

        event = create_event(
            type=EventType.TRANSFER,
            origin=origin_account_number,
            destination=destination_account_number,
            amount=7.39
        )

        self.assertEqual({
            'origin': {'id': origin_account_number, 'balance': Decimal('12.61')},
            'destination': {'id': destination_account_number, 'balance': Decimal('57.39')}
        }, event)
        updated_origin_acc = Account.objects.get(id=origin_account.id)
        updated_destination_acc = Account.objects.get(id=destination_account.id)
        self.assertEqual(Decimal('12.61'), updated_origin_acc.balance)
        self.assertEqual(Decimal('57.39'), updated_destination_acc.balance)
        self.assertEvent(EventType.TRANSFER, origin_account.id, destination_account.id, Decimal('7.39'))

    def test_transfer_to_non_existing_destination_account_should_create_account(self):
        origin_account = self._create_account(1, 10)
        destination_account_number = 222

        create_event(
            type=EventType.TRANSFER,
            origin=origin_account.number,
            destination=destination_account_number,
            amount=30
        )

        destination_account = Account.objects.get(number=destination_account_number)
        self.assertEqual(30, destination_account.balance)
        self.assertEvent(EventType.TRANSFER, origin_account.id, destination_account.id, 30)

    def test_withdraw_from_non_existing_account_should_raises_exception(self):
        with self.assertRaises(AccountNotFound) as context:
            create_event(
                type=EventType.TRANSFER,
                origin=123,
                amount=30
            )

        self.assertEqual('Account 123 not found.', str(context.exception))

    def test_transfer_from_non_existing_origin_account__should_raises_exception(self):
        destination_account = self._create_account(1, 10)

        with self.assertRaises(AccountNotFound) as context:
            create_event(
                type=EventType.TRANSFER,
                origin=222,
                destination=destination_account.number,
                amount=30
            )

        self.assertEqual('Account 222 not found.', str(context.exception))

    def assertEvent(self, event_type, origin_account_id, destination_account_id, amount):
        event = Event.objects.get(origin_id=origin_account_id, destination_id=destination_account_id)
        self.assertEqual(event_type, event.type)
        self.assertEqual(amount, event.amount)

    def _create_account(self, number, balance):
        return Account.objects.create(number=number, balance=balance)
