from django.test import TestCase

from accounts.models import Account
from core.events.enums import EventType
from events.event_gateway import create_event


class CreateEventTests(TestCase):
    def test_create_event_and_return_as_dict(self):
        event_type = EventType.TRANSFER
        origin_account = Account.objects.create(number=30)
        destination_account = Account.objects.create(number=31)
        amount = 99

        event = create_event(
            type=event_type,
            origin_id=origin_account.id,
            destination_id=destination_account.id,
            amount=amount
        )

        self.assertEqual(event_type, event['type'])
        self.assertEqual(origin_account.id, event['origin_id'])
        self.assertEqual(destination_account.id, event['destination_id'])
        self.assertEqual(amount, event['amount'])
